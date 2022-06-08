import logging
from datetime import timedelta, datetime
from typing import Any, Optional, Type, TypeVar, Union, Dict, List
from json import JSONDecodeError

from multidict import CIMultiDict
from pydantic import BaseModel, parse_obj_as, SecretStr, validate_arguments
from yarl import URL

from ..errors import HTTPError, ResponseParseError, error_response_mapping, MISSING, AsyncClientError
from ..framework import ClientInit, Response
from ..utils import validate_type
from .utils import chunk_file_reader, merge_params

is_async: bool
try:
    import asyncio
    from aiohttp import ClientSession, ClientTimeout
    from aiolimiter import AsyncLimiter

    is_async = True
except ImportError:
    is_async = False

__all__ = {
    "AsyncClient"
}

_log: logging.Logger = logging.getLogger("arya_api_framework.Async")

MappingOrModel = Union[Dict[str, Union[str, int]], BaseModel]
HttpMapping = Dict[str, Union[str, int, List[Union[str, int]]]]
Parameters = Union[HttpMapping, BaseModel]
Cookies = MappingOrModel
Headers = MappingOrModel
Body = Union[Dict[str, Any], BaseModel]
ErrorResponses = Dict[int, Type[BaseModel]]

ClientSessionT = TypeVar('ClientSessionT', bound='ClientSession')


class AsyncClient(metaclass=ClientInit):
    """The basic Client implementation that all API clients inherit from."""

    _headers: Optional[Headers] = None
    _cookies: Optional[Cookies] = None
    _parameters: Optional[Parameters] = None
    _error_responses: Optional[ErrorResponses] = None
    _rate_limit_interval: Optional[Union[int, float]] = 1
    _rate_limit: Optional[Union[int, float]] = None
    _limiter: Optional[AsyncLimiter] = None
    _last_request_at: Optional[datetime] = None
    _base: Optional[URL] = MISSING
    _session: ClientSessionT

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
            rate_limit_interval: Union[int, float] = MISSING
    ) -> None:
        if not is_async:
            raise AsyncClientError("The async context is unavailable. Try installing with `python -m pip install arya-api-framework[async]`.")

        if uri is not MISSING:
            if not isinstance(uri, str):
                raise ValueError("The uri should be a string.")
            self._base = URL(uri)

        if self.uri is None:
            raise AsyncClientError(
                "The client needs a base uri specified. "
                "This can be done through init parameters, or subclass parameters."
            )

        if bearer_token is not None:
            if isinstance(bearer_token, SecretStr):
                bearer_token = bearer_token.get_secret_value()

            if headers is None or headers is MISSING:
                headers = {}

            headers["Authorization"] = f"Bearer {bearer_token}"

        if headers is not MISSING:
            self._headers = headers or {}
        if cookies is not MISSING:
            self._cookies = cookies or {}
        if parameters is not MISSING:
            self._parameters = parameters or {}

        if error_responses is not MISSING:
            self._error_responses = error_responses

        if rate_limit is not MISSING:
            if validate_type(rate_limit, [int, float]):
                self._rate_limit = rate_limit
        if rate_limit_interval is not MISSING:
            if validate_type(rate_limit_interval, [int, float]):
                self._rate_limit_interval = rate_limit_interval

        if self._rate_limit:
            self._limiter = AsyncLimiter(self._rate_limit, self._rate_limit_interval)

        self._session = ClientSession(
            self.uri_root,
            headers=self.headers or {},
            cookies=self.cookies or {}
        )

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
            if not isinstance(uri, str):
                raise ValueError("The uri should be a string.")
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
    def uri(self) -> Optional[URL]:
        return self._base if self._base is not MISSING else None

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
        self._session._default_headers = CIMultiDict(headers) if headers else CIMultiDict()

    @property
    def cookies(self) -> Optional[Cookies]:
        return self._cookies

    @cookies.setter
    def cookies(self, cookies: Cookies) -> None:
        self._cookies = self._flatten_format(cookies)
        self._session._cookie_jar.update_cookies(self._cookies)

    @property
    def parameters(self) -> Optional[Parameters]:
        return self._parameters

    @parameters.setter
    def parameters(self, params: Parameters) -> None:
        self._parameters = self._flatten_format(params)

    @property
    def rate_limit(self) -> Optional[timedelta]:
        if self._rate_limit:
            return timedelta(seconds=self._rate_limit_interval/self._rate_limit)

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
    async def request(
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
        if self._limiter:
            if not self._limiter.has_capacity():
                _log.info("Waiting for rate limit")
            await self._limiter.acquire()

        path = self.uri_rel + path if self.uri_rel else path
        headers = self._flatten_format(headers)
        cookies = self._flatten_format(cookies)
        parameters = merge_params(self.parameters, self._flatten_format(parameters))
        body = self._flatten_format(body)
        error_responses = error_responses or self.error_responses or {}

        async with self._session.request(
                method,
                path,
                headers=headers,
                cookies=cookies,
                params=parameters,
                json=body,
                data=data,
                timeout=ClientTimeout(total=timeout)
        ) as response:
            _log.info(f"[{method} {response.status}] {path} {URL(response.url).query_string}")

            if response.ok:
                try:
                    response_json = await response.json(content_type=None)
                except JSONDecodeError:
                    response_text = await response.text()
                    raise ResponseParseError(raw_response=response_text)

                if response_format is not None:
                    obj = parse_obj_as(response_format, response_json)
                    obj.request_base_ = response.url
                    return obj

                return response_json

            error_class = error_response_mapping.get(response.status, HTTPError)
            error_response_model = error_responses.get(response.status)

            try:
                response_json = await response.json(content_type=None)
            except JSONDecodeError:
                response_text = await response.text()
                raise ResponseParseError(raw_response=response_text)

            if bool(error_response_model):
                raise error_class(parse_obj_as(error_response_model, response_json))

            raise error_class(response_json)

    @validate_arguments()
    async def upload_file(
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
        return await self.post(
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
    async def stream_file(
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
        return await self.post(
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
    async def get(
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
        return await self.request(
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
    async def post(
            self,
            path: str = None,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            params: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,  # Default in aiohttp
            error_responses: ErrorResponses = None
    ) -> Optional[Response]:
        return await self.request(
            "POST",
            path,
            body=body,
            data=data,
            headers=headers,
            cookies=cookies,
            params=params,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses,
        )

    @validate_arguments()
    async def patch(
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
        return await self.request(
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
    async def put(
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
        return await self.request(
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
    async def delete(
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
        return await self.request(
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

    async def close(self):
        await self._session.close()

    # ---------- Class Methods ----------
    @classmethod
    @validate_arguments()
    def _flatten_format(cls, data: Optional[Parameters]) -> Dict[str, Any]:
        return data.dict(exclude_unset=True) if isinstance(data, BaseModel) else data
