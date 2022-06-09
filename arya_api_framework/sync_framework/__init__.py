from datetime import datetime, timedelta
import logging
from json import JSONDecodeError
from typing import Any, Optional, Type, TypeVar, Union, Dict, List
import time

from pydantic import BaseModel, parse_obj_as, SecretStr, validate_arguments
from yarl import URL

from .utils import chunk_file_reader, sleep_and_retry
from ..errors import HTTPError, ResponseParseError, error_response_mapping, MISSING, SyncClientError
from ..framework import ClientInit, Response
from ..utils import validate_type

is_sync: bool
try:
    from requests import Session
    from requests.cookies import cookiejar_from_dict
    from ratelimit import limits

    is_sync = True
except ImportError:
    is_sync = False

__all__ = [
    "SyncClient"
]

_log: logging.Logger = logging.getLogger("arya_api_framework.Sync")

MappingOrModel = Union[Dict[str, Union[str, int]], BaseModel]
HttpMapping = Dict[str, Union[str, int, List[Union[str, int]]]]
Parameters = Union[HttpMapping, BaseModel]
Cookies = MappingOrModel
Headers = MappingOrModel
Body = Union[Dict[str, Any], BaseModel]
ErrorResponses = Dict[int, Type[BaseModel]]

SessionT = TypeVar('SessionT', bound='Session')


class SyncClient(metaclass=ClientInit):

    _headers: Optional[Headers] = None
    _cookies: Optional[Cookies] = None
    _parameters: Optional[Parameters] = None
    _error_responses: Optional[ErrorResponses] = None
    _rate_limit_interval: Optional[Union[int, float]] = 1
    _rate_limit: Optional[Union[int, float]] = None
    _rate_limited = False
    _last_request_at: Optional[datetime] = None
    _base: Optional[URL] = MISSING
    _session: SessionT

    # ---------- Initialization Methods ----------
    def __init__(
            self,
            /,
            uri: str = MISSING,
            headers: Headers = MISSING,
            cookies: Cookies = MISSING,
            parameters: Parameters = MISSING,
            error_responses: ErrorResponses = MISSING,
            bearer_token: Union[str, SecretStr] = MISSING,
            rate_limit: Union[int, float] = MISSING,
            rate_limit_interval: Union[int, float] = MISSING,
    ) -> None:
        if not is_sync:
            raise SyncClientError(
                "The sync context is unavailable. Try installing with `python -m pip install arya-api-framework[sync]`.")

        if uri is not MISSING:
            if validate_type(uri, str):
                self._base = URL(uri)

        if self.uri is None:
            raise SyncClientError(
                "The client needs a base uri specified. "
                "This can be done through init parameters, or subclass parameters."
            )

        if cookies is not MISSING:
            self._cookies = cookies or {}
        if parameters is not MISSING:
            self._parameters = parameters or {}

        if bearer_token is not None:
            if validate_type(bearer_token, SecretStr, err=False):
                bearer_token = bearer_token.get_secret_value()

            if headers is None or headers is MISSING:
                headers = {}

            headers["Authorization"] = f"Bearer {bearer_token}"

        if headers is not MISSING:
            self._headers = headers or {}

        if error_responses is not MISSING:
            self.error_responses = error_responses

        if rate_limit is not MISSING:
            if validate_type(rate_limit, [int, float]):
                self._rate_limit = rate_limit
        if rate_limit_interval is not MISSING:
            if validate_type(rate_limit_interval, [int, float]):
                print("setting interval")
                self._rate_limit_interval = rate_limit_interval

        if self._rate_limit:
            self.request = sleep_and_retry(
                limits(calls=self._rate_limit, period=self._rate_limit_interval)(self.request)
            )
            self._rate_limited = True

        self._session = Session()
        self._session.headers = self.headers
        self._session.cookies = cookiejar_from_dict(self.cookies or {})
        self._session.params = self.parameters

    def __post_init__(self, *args, **kwargs) -> None:
        pass

    def __init_subclass__(
            cls,
            uri: str = MISSING,
            headers: Headers = MISSING,
            cookies: Cookies = MISSING,
            parameters: Parameters = MISSING,
            error_responses: ErrorResponses = MISSING,
            rate_limit: Union[int, float] = MISSING,
            rate_limit_interval: Union[int, float] = MISSING
    ) -> None:
        if uri is not MISSING:
            if validate_type(uri, str):
                cls._base = URL(uri)
        if headers is not MISSING:
            cls._headers = headers
        if cookies is not MISSING:
            cls._cookies = cookies or {}
        if parameters is not MISSING:
            cls._parameters = parameters or {}
        if error_responses is not MISSING:
            cls._error_responses = error_responses
        if rate_limit is not MISSING:
            if validate_type(rate_limit, [int, float]):
                cls._rate_limit = rate_limit
        if rate_limit_interval is not MISSING:
            if validate_type(rate_limit_interval, [int, float]):
                cls._rate_limit_interval = rate_limit_interval

    # ---------- URI Options ----------
    @property
    def uri(self) -> Optional[str]:
        return str(self._base) if self._base is not MISSING else None

    @property
    def uri_root(self) -> Optional[str]:
        return str(self._base.origin()) if self._base is not MISSING else None

    @property
    def uri_rel(self) -> Optional[str]:
        return str(self._base.relative()) if self._base is not MISSING else None

    # ---------- Default Request Settings ----------
    @property
    def headers(self) -> Optional[Headers]:
        return self._headers

    @headers.setter
    def headers(self, headers: Headers) -> None:
        self._headers = self._flatten_format(headers)
        self._session.headers = self._headers

    @property
    def cookies(self) -> Optional[Cookies]:
        return self._cookies

    @cookies.setter
    def cookies(self, cookies: Cookies) -> None:
        self._cookies = self._flatten_format(cookies)
        self._session.cookies = self._cookies

    @property
    def parameters(self) -> Optional[Parameters]:
        return self._parameters

    @parameters.setter
    def parameters(self, params: Parameters) -> None:
        self._parameters = self._flatten_format(params)
        self._session.params = self._parameters

    @property
    def error_responses(self) -> Optional[ErrorResponses]:
        return self._error_responses

    @error_responses.setter
    @validate_arguments()
    def error_responses(self, error_responses: ErrorResponses) -> None:
        if error_responses is not MISSING:
            self._error_responses = error_responses

    # ---------- Request Methods ----------
    @validate_arguments()
    def request(
            self,
            method: str,
            path: str = None,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[Response]:
        path = self.uri + path if path else self.uri
        headers = self._flatten_format(headers)
        cookies = self._flatten_format(cookies)
        parameters = self._flatten_format(parameters)
        body = self._flatten_format(body)
        error_responses = error_responses or self.error_responses or {}

        with self._session.request(
                method,
                path,
                headers=headers,
                cookies=cookies,
                params=parameters,
                json=body,
                data=data,
                timeout=timeout
        ) as response:
            _log.info(f"[{method} {response.status_code}] {path} {URL(response.request.url).query_string}")

            if response.ok:
                try:
                    response_json = response.json()
                except JSONDecodeError:
                    raise ResponseParseError(raw_response=response.text)

                if response_format is not None:
                    obj = parse_obj_as(response_format, response_json)
                    obj.request_base_ = response.request.url
                    return obj

                return response_json

            error_class = error_response_mapping.get(response.status_code, HTTPError)
            error_response_model = error_responses.get(response.status_code)

            try:
                response_json = response.json()
            except JSONDecodeError:
                raise ResponseParseError(raw_response=response.text)

            if bool(error_response_model):
                raise error_class(parse_obj_as(error_response_model, response_json))

            raise error_class(response_json)

    @validate_arguments()
    def upload_file(
            self,
            path: str,
            file: str,
            *,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[Response]:
        return self.post(
            path,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            data={'file': open(file, 'rb')},
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses,
        )

    @validate_arguments()
    def stream_file(
            self,
            path: str,
            file: str,
            *,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,  # Default in aiohttp
            error_responses: ErrorResponses = None
    ) -> Optional[Response]:
        return self.post(
            path,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            data=chunk_file_reader(file),
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses
        )

    @validate_arguments()
    def get(
            self,
            path: str = None,
            *,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,  # Default in aiohttp
            error_responses: ErrorResponses = None
    ) -> Optional[Response]:
        return self.request(
            "GET",
            path,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses,
        )

    @validate_arguments()
    def post(
            self,
            path: str = None,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,  # Default in aiohttp
            error_responses: ErrorResponses = None
    ) -> Optional[Response]:
        return self.request(
            "POST",
            path,
            body=body,
            data=data,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses,
        )

    @validate_arguments()
    def patch(
            self,
            path: str = None,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,  # Default in aiohttp
            error_responses: ErrorResponses = None
    ) -> Optional[Response]:
        return self.request(
            "PATCH",
            path,
            body=body,
            data=data,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses,
        )

    @validate_arguments()
    def put(
            self,
            path: str = None,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,  # Default in aiohttp
            error_responses: ErrorResponses = None
    ) -> Optional[Response]:
        return self.request(
            "PUT",
            path,
            body=body,
            data=data,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses,
        )

    @validate_arguments()
    def delete(
            self,
            path: str = None,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,  # Default in aiohttp
            error_responses: ErrorResponses = None
    ) -> Optional[Response]:
        return self.request(
            "DELETE",
            path,
            body=body,
            data=data,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses,
        )

    def close(self):
        self._session.close()

    # ---------- Class Methods ----------
    @classmethod
    @validate_arguments()
    def _flatten_format(cls, data: Optional[Parameters]) -> Dict[str, Any]:
        return data.dict(exclude_unset=True) if isinstance(data, BaseModel) else data
