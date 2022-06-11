from datetime import datetime, timedelta
import logging
from json import JSONDecodeError
from typing import Any, Optional, Type, TypeVar, Union, Dict, List
import time

from pydantic import BaseModel, parse_obj_as, SecretStr, validate_arguments
from yarl import URL

from .utils import chunk_file_reader, sleep_and_retry
from ..errors import HTTPError, ResponseParseError, error_response_mapping, MISSING, SyncClientError
from ..framework import Response
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


class SyncClient:
    """ The synchronous API client class. Utilizes the :resource:`requests <requests>` module.

    Arguments
    ---------
        uri: Optional[:py:class:`str`]
            The base URI that will prepend all requests made using the client.

            Warning
            -------
                This should always either be passed as an argument here or as a subclass argument. If neither are given,
                an :class:`errors.SyncClientError` exception will be raised.

    Keyword Args
    ------------
        headers: Optional[Union[:py:class:`dict`, :class:`BaseModel`]
            The default headers to pass with every request. Can be overridden by individual requests.
            Defaults to ``None``.
        cookies: Optional[Union[:py:class:`dict`, :class:`BaseModel`]
            The default cookies to pass with every request. Can be overridden by individual requests.
            Defaults to ``None``.
        parameters: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
            The default parameters to pass with every request. Can be overridden by individual requests.
            Defaults to ``None``.
        error_responses: Optional[:py:class:`dict`]
            A mapping of :py:class:`int` error codes to :class:`BaseModel` models to use when that error code is
            received. Defaults to ``None`` and raises default exceptions for error codes.
        bearer_token: Optional[:py:class:`str`, :pydantic:`pydantic.SecretStr <usage/types/#secret-types>`
            A ``bearer_token`` that will be sent with requests in the ``Authorization`` header. Defaults to ``None``
        rate_limit: Optional[:py:class:`int`]
            The number of requests to allow over :paramref:`rate_limit_interval` seconds. Defaults to ``None``
        rate_limit_interval: Optional[:py:class:`int`]
            The period of time, in seconds, over which to apply the rate limit per every :paramref:`rate_limi` requests.
            Defaults to ``1`` second.

    Attributes
    ----------
        uri: :py:class:`str`
            The base URI that will prepend all requests made using the client.
    """

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
            uri: Optional[str] = None,
            *args,
            headers: Optional[Headers] = None,
            cookies: Optional[Cookies] = None,
            parameters: Optional[Parameters] = None,
            error_responses: Optional[ErrorResponses] = None,
            bearer_token: Optional[Union[str, SecretStr]] = None,
            rate_limit: Optional[Union[int, float]] = None,
            rate_limit_interval: Optional[Union[int, float]] = None,
            **kwargs
    ) -> None:
        if not is_sync:
            raise SyncClientError(
                "The sync context is unavailable. Try installing with `python -m pip install arya-api-framework[sync]`.")

        if uri:
            if validate_type(uri, str):
                self._base = URL(uri)

        if not self.uri:
            raise SyncClientError(
                "The client needs a base uri specified. "
                "This can be done through init parameters, or subclass parameters."
            )

        if cookies:
            self._cookies = cookies or {}
        if parameters:
            self._parameters = parameters or {}

        if bearer_token:
            if validate_type(bearer_token, SecretStr, err=False):
                bearer_token = bearer_token.get_secret_value()

            if not headers:
                headers = {}

            headers["Authorization"] = f"Bearer {bearer_token}"

        if headers:
            self._headers = headers or {}

        if error_responses:
            self.error_responses = error_responses

        if rate_limit:
            if validate_type(rate_limit, [int, float]):
                self._rate_limit = rate_limit
        if rate_limit_interval:
            if validate_type(rate_limit_interval, [int, float]):
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

        if hasattr(self, '__post_init__'):
            self.__post_init__(*args, **kwargs)

    def __post_init__(self, *args, **kwargs) -> None:
        """This method is run after the ``__init__`` method is called, and is passed any extra arguments or
        keyword arguments that the regular init method did not recognize.

        """
        pass

    def __init_subclass__(
            cls,
            uri: Optional[str] = None,
            headers: Optional[Headers] = None,
            cookies: Optional[Cookies] = None,
            parameters: Optional[Parameters] = None,
            error_responses: Optional[ErrorResponses] = None,
            rate_limit: Optional[Union[int, float]] = None,
            rate_limit_interval: Optional[Union[int, float]] = None
    ) -> None:
        if uri:
            if validate_type(uri, str):
                cls._base = URL(uri)
        if headers:
            cls._headers = headers
        if cookies:
            cls._cookies = cookies or {}
        if parameters:
            cls._parameters = parameters or {}
        if error_responses:
            cls._error_responses = error_responses
        if rate_limit:
            if validate_type(rate_limit, [int, float]):
                cls._rate_limit = rate_limit
        if rate_limit_interval:
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
