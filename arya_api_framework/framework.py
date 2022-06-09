import abc
from typing import Any, Optional, Union, AbstractSet, Mapping, Dict, Callable, Type
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel as PydBaseModel, Field, Protocol

from .errors import MISSING


__all__ = [
    'Response',
    'PaginatedResponse'
]

StrBytes = Union[str, bytes]
IntStr = Union[int, str]
AbstractSetIntStr = AbstractSet[IntStr]
MappingIntStrAny = Mapping[IntStr, Any]
DictStrAny = Dict[str, Any]


class ClientInit(type):
    def __call__(cls, *args, **kwargs) -> Any:
        uri = kwargs.get('uri', MISSING)
        headers = kwargs.get('headers', MISSING)
        cookies = kwargs.get('cookies', MISSING)
        parameters = kwargs.get('parameters', MISSING)
        error_responses = kwargs.get('error_responses', MISSING)
        bearer_token = kwargs.get('bearer_token', MISSING)
        rate_limit = kwargs.get('rate_limit', MISSING)
        rate_limit_interval = kwargs.get('rate_limit_interval', MISSING)

        obj = type.__call__(
            cls, uri=uri, headers=headers, cookies=cookies, parameters=parameters,
            error_responses=error_responses, bearer_token=bearer_token, rate_limit=rate_limit,
            rate_limit_interval=rate_limit_interval
        )
        if hasattr(obj, '__post_init__'):
            obj.__post_init__(*args, **kwargs)
        return obj


class BaseModel(PydBaseModel):
    """
    .. external_inherits_from:: class, pydantic, usage/models/#basic-model-usage, pydantic.BaseModel

    These models include data validation on the attributes given to them, and allow for very
    direct control over response formats. Additionally, they allow to easily creating database-like
    structures, and outputting the data ina variety of formats.
    """

    def dict(
            self,
            *,
            include: Union[AbstractSetIntStr, MappingIntStrAny] = None,
            exclude: Union[AbstractSetIntStr, MappingIntStrAny] = None,
            by_alias: bool = False,
            skip_defaults: bool = None,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
    ) -> DictStrAny:
        """
        .. external_inherits_from::
            method,
            pydantic,
            https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeldict,
            pydantic.BaseModel.dict

        Generate a :py:class:`dict` representation of the model, optionally specifying
        which fields to include or exclude. Look to the
        :pydantic:`pydantic documentation<usage/exporting_models/#modeldict>` for further details.

        Keyword Args
        ------------
            include: Optional[Union[Set[:py:class:`str`]], :py:class:`dict`]]
                Fields to include in the returned dictionary. See this
                :pydantic:`example <usage/exporting_models/#advanced-include-and-exclude>`.
            exclude: Optional[Union[Set[:py:class:`str`]], :py:class:`dict`]]
                Fields to exclude from the returned dictionary. See this
                :pydantic:`example <usage/exporting_models/#advanced-include-and-exclude>`.
            by_alias: Optional[:py:class:`bool`]
                Whether field aliases should be used as keys in the resulting dictionary.
                Defaults to ``False``
            exclude_unset: Optional[:py:class:`bool`]
                Whether or not fields that were not specifically set upon creation of the model
                should be included in the dictionary. Defaults to ``False``.

                Warning
                -------
                    This was previously referred to as ``skip_defaults``. This parameter is still accepted,
                    but has been deprecated and is not recommended.

            exclude_defaults: Optional[:py:class:`bool`]
                Whether or not to include fields that are set to their default values. Even if a field is given a
                value when the model is instanced, if that value is equivalent to the default, it will not be included.
                Defaults to ``False``.
            exclude_none: Optional[:py:class:`bool`]
                Whether of not to include fields which are equal to ``None``. Defaults to ``False``.

        Returns
        -------
            :py:class:`dict`
                A mapping of :py:class:`str` field names to their values.

        |inherited|
        """
        return super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none
        )

    def json(
        self,
        *,
        include: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        exclude: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        encoder: Optional[Callable[[Any], Any]] = None,
        models_as_dict: bool = True,
        **dumps_kwargs: Any,
    ) -> str:
        """
        .. external_inherits_from::
            method,
            pydantic,
            usage/exporting_models/#modeljson,
            pydantic.BaseModel.json

        Serializes the model to a JSON string. Typically will call :meth:`dict` and then
        serialize the result. As such, the parameters are very similar, except for a few extra
        options.

        Tip
        ----
            You can set the :paramref:`models_as_dict` option to ``False`` to implement custom serialization for a
            model. See this :pydantic:`example <usage/exporting_models/#serialising-self-reference-or-other-models>`
            for more info.

        Tip
        ----
            It is possible to implement custom encoders for specific types within an individual model.
            This is helpful to avoid having to create an entire encoder for the :paramref:`encoder` argument.
            See this :pydantic:`example <usage/exporting_models/#serialising-self-reference-or-other-models>`
            for more info.

        Keyword Args
        ------------
            include: Optional[Union[Set[:py:class:`str`]], :py:class:`dict`]]
                Fields to include in the returned dictionary. See this
                :pydantic:`example <usage/exporting_models/#advanced-include-and-exclude>`.
            exclude: Optional[Union[Set[:py:class:`str`]], :py:class:`dict`]]
                Fields to exclude from the returned dictionary. See this
                :pydantic:`example <usage/exporting_models/#advanced-include-and-exclude>`.
            by_alias: Optional[:py:class:`bool`]
                Whether field aliases should be used as keys in the resulting dictionary.
                Defaults to ``False``
            exclude_unset: Optional[:py:class:`bool`]
                Whether or not fields that were not specifically set upon creation of the model
                should be included in the dictionary. Defaults to ``False``.

                Warning
                -------
                    This was previously referred to as ``skip_defaults``. This parameter is still accepted,
                    but has been deprecated and is not recommended.

            exclude_defaults: Optional[:py:class:`bool`]
                Whether or not to include fields that are set to their default values. Even if a field is given a
                value when the model is instanced, if that value is equivalent to the default, it will not be included.
                Defaults to ``False``.
            exclude_none: Optional[:py:class:`bool`]
                Whether of not to include fields which are equal to ``None``. Defaults to ``False``.
            encoder: Optional[Callable[Any, Any]]
                A custom encoder function that is given to :py:func:`json.dumps`. By default, a custom
                :resource:`pydantic <pydantic>` encoder is used, which can serialize many common types
                that the default :py:mod:`json` cannot normally handle, like a :py:class:`datetime <datetime.datetime>`.

            models_as_dict: Optional[:py:class:`bool`]
                Whether or not to serialize other models that are contained within the fields of the target model
                to json. This defaults to ``True``.

            **dumps_kwargs:
                Any extra keyword arguments are passed to :py:func:`json.dumps` directly, such as
                the ``indent`` argument, which will pretty-print the resulting :py:class:`str`,
                using indentations of ``indent`` spaces.

        Returns
        -------
            :py:class:`str`
                A JSON serialized string.

        |inherited|
        """
        return super().json(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exlclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            encoder=encoder,
            models_as_dict=models_as_dict,
            **dumps_kwargs
        )

    def copy(
        self: PydBaseModel,
        *,
        include: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        exclude: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        update: DictStrAny = None,
        deep: bool = False,
    ) -> PydBaseModel:
        """
        .. external_inherits_from::
            method,
            pydantic,
            usage/exporting_models/#modelcopy,
            pydantic.BaseModel.copy

        Returns a duplicate of the model. This is very handy for use with immutable models.

        Keyword Args
        ------------
            include: Optional[Union[Set[:py:class:`str`]], :py:class:`dict`]]
                Fields to include in the returned dictionary. See this
                :pydantic:`example <usage/exporting_models/#advanced-include-and-exclude>`.
            exclude: Optional[Union[Set[:py:class:`str`]], :py:class:`dict`]]
                Fields to exclude from the returned dictionary. See this
                :pydantic:`example <usage/exporting_models/#advanced-include-and-exclude>`.
            update: Optional[:py:class:`dict`]
                A dictionary of values to update when creating the copied model. Very similar in
                concept to :py:meth:`dict.update`.
            deep: Optional[:py:class:`bool`]
                Whether to make a deep copy of the object, or a shallow copy. Defaults to ``False``.

        Returns
        -------
            :class:`BaseModel`
                A copied instance of the model.

        |inherited|
        """

        return super().copy(
            include=include,
            exclude=exclude,
            update=update,
            deep=deep
        )

    @classmethod
    def parse_obj(cls: Type[PydBaseModel], obj: Any) -> PydBaseModel:
        """
        .. external_inherits_from::
            classmethod,
            pydantic,
            usage/models/#helper-functions,
            pydantic.BaseModel.parse_obj

        |inherited|
        """
        return super().parse_obj(obj=obj)

    @classmethod
    def parse_raw(
        cls: Type[PydBaseModel],
        b: StrBytes,
        *,
        content_type: str = None,
        encoding: str = 'utf8',
        proto: Protocol = None,
        allow_pickle: bool = False,
    ) -> PydBaseModel:
        """
        .. external_inherits_from::
            classmethod,
            pydantic,
            usage/models/#helper-functions,
            pydantic.BaseModel.parse_raw

        |inherited|
        """
        return super().parse_raw(
            b=b,
            content_type=content_type,
            encoding=encoding,
            proto=proto,
            allow_pickle=allow_pickle
        )

    @classmethod
    def parse_file(
        cls: Type[PydBaseModel],
        path: Union[str, Path],
        *,
        content_type: str = None,
        encoding: str = 'utf8',
        proto: Protocol = None,
        allow_pickle: bool = False,
    ) -> PydBaseModel:
        """
        .. external_inherits_from::
            classmethod
            pydantic
            usage/models/#helper-functions
            pydantic.BaseModel.parse_file

        |inherited|
        """
        return super().parse_file(
            path=path,
            content_type=content_type,
            encoding=encoding,
            proto=proto,
            allow_pickle=allow_pickle
        )


class Response(BaseModel, abc.ABC):
    """
    .. inherits_from:: BaseModel

    The basic class that all response models for a request should subclass.
    This class provides a few basic fields that are used in recording
    request responses.

    Example
    --------
        .. code-block:: python

            # Create your response structure:
            class MyAPIResponse(Response):
                index: int
                first_name: str
                last_name: str

            # Pass this into your requests:
            response = my_client.get(..., response_model=MyAPIResponse)       # Sync
            response = await my_client.get(..., response_mode=MyApiResponse)  # Async

            # >>> response.dict()
            {
                "request_base_": "url",
                "request_received_at_": datetime.datetime(...),
                "id": 123,
                "first_name": "First",
                "last_name": "Last"
            }

    Attributes
    -----------
        request_base_: Optional[:py:class:`str`]
            The url of the original request this is holding the response to.
        request_received_at_: Optional[:py:class:`datetime.datetime`] = :py:meth:`datetime.datetime.utcnow`
            The datetime that the response was received at.

    Note
    ----
        The :paramref:`request_received_at_ <Request.request_received_at_>` attribute is set by default when a Response is created.
        The default implementation is a timezone-aware UTC datetime.
    """

    request_base_: Optional[str] = None
    request_received_at_: Optional[datetime] = Field(default_factory=datetime.utcnow)


class PaginatedResponse(Response, abc.ABC):
    """
    .. inherits_from:: Response

    This offers a few extra options for a request response to enable easier response pagination.

    Often times when receiving a response for an API query which might include a significant amount of data
    (such as a list of products from an online shop), the API will limit the response to a set number of items.
    Taking this into account, this class can take advantage of the data structure to automatically give the necessary
    information about navigating this pagination.

    Warning
    -------
        This is an :py:class:`abstract <abc.ABC>` class, which means that any subclasses `must` implement
        all methods from this class.
    """

    @abc.abstractmethod
    def is_paginating(self) -> bool:
        """A method that is intended to determine whether any given response is paginated or not.

        If your response is `always` paginating, this should simply return ``True``. Likewise, if the response
        is never paginating, return ``False``. Otherwise, some logic should be implemented to determine
        whether the response is paginated.

        Returns
        -------
            :py:class:`bool`:
                Whether the response is paginated.
        """
        return False

    @abc.abstractmethod
    def next(self) -> Optional[Any]:
        """This will return an identifier for how to navigate to the next page in the paginated response.

        For example, if a response has a ``page_number`` field, you would return ``self.page_number + 1``.
        However, this can also be any return type, to allow for URLs to be returned directly, or some other
        implementation.

        Tip
        ----
            This method, as well as :meth:`previous <previous>`, :meth:`end <end>`, and
            :meth:`start <start>` for navigating pagination, should call :meth:`is_paginating` and return
            ``None`` if the response is not paginating.

            .. code-block:: python

                if not self.is_paginating():
                    return

        Returns
        -------
            Optional[Any]:
                Some identifier for navigating to the next page in the pagination.
        """
        return None

    @abc.abstractmethod
    def previous(self) -> Optional[Any]:
        """This will return an identifier for how to navigate to the previous page in the paginated response.

        For example, if a response has a ``page_number`` field, you would return ``self.page_number - 1``.
        However, this can also be any return type, to allow for URLs to be returned directly, or some other
        implementation.

        Returns
        -------
            Optional[Any]:
                Some identifier for navigating to the previous page in the pagination.
        """
        return None

    @abc.abstractmethod
    def end(self) -> Optional[Any]:
        """This will return an identifier for how to navigate to the last page in the paginated response.

        For example, if a response has a ``page_count`` field, you would want to return ``self.page_count``.
        However, this can also be any return type, to allow for URLs to be returned directly, or some other
        implementation.

        Returns
        -------
            Optional[Any]:
                Some identifier for navigating to the last page in the pagination.
        """
        return None

    @abc.abstractmethod
    def start(self) -> Optional[Any]:
        """This will return an identifier for how to navigate to the first page in the paginated response.

        For example, if you were tracking pagination by numbering each page, you would simply return ``1`` for the
        first page.

        Returns
        -------
            Optional[Any]:
                Some identifier for navigating to the first page in the pagination.
        """
        return None
