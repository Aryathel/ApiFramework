import abc
from typing import Any, Optional
from datetime import datetime

from pydantic import BaseModel, Field

from .errors import MISSING


class ClientInit(type):
    def __call__(cls, *args, **kwargs) -> Any:
        uri = kwargs.get('uri', MISSING)
        headers = kwargs.get('headers', MISSING)
        cookies = kwargs.get('cookies', MISSING)
        parameters = kwargs.get('parameters', MISSING)
        error_responses = kwargs.get('error_responses', MISSING)
        bearer_token = kwargs.get('bearer_token', MISSING)

        obj = type.__call__(cls, uri=uri, headers=headers, cookies=cookies, parameters=parameters,
                            error_responses=error_responses, bearer_token=bearer_token)
        if hasattr(obj, '__post_init__'):
            obj.__post_init__(*args, **kwargs)
        return obj


class Response(BaseModel, abc.ABC):
    request_base_: Optional[str] = None
    request_received_at_: Optional[datetime] = Field(default_factory=datetime.utcnow)


class PaginatedResponse(Response, abc.ABC):
    @property
    @abc.abstractmethod
    def is_paginating(self) -> bool:
        return False

    @property
    @abc.abstractmethod
    def next(self) -> Optional[int]:
        return None

    @property
    @abc.abstractmethod
    def end(self) -> Optional[int]:
        return None

    @property
    @abc.abstractmethod
    def back(self) -> Optional[int]:
        return None

    @property
    @abc.abstractmethod
    def start(self) -> Optional[int]:
        return None
