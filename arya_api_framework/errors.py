"""
Author: Arya Mayfield
Date: June 2022
Description: Various exceptions for use throughout the module.
"""

# Stdlib modules
from typing import Union

# 3rd party modules
from pydantic import BaseModel

# Local modules
from .statuses import *

# Define exposed objects
__all__ = [
    # General
    "MISSING",
    "ValidationError",
    # Client
    "ClientError",
    "AsyncClientError",
    "SyncClientError",
    # Requests
    "ResponseParseError",
    'HTTPError',
    'HTTPRedirect',
    'HTTPClientError',
    'HTTPServerError',
    # 300
    'HTTPMultipleChoices',
    'HTTPMovedPermanently',
    'HTTPFound',
    'HTTPSeeOther',
    'HTTPNotModified',
    'HTTPUseProxy',
    'HTTPReserved',
    'HTTPTemporaryRedirect',
    'HTTPPermanentRedirect',
    # 400
    'HTTPBadRequest',
    'HTTPUnauthorized',
    'HTTPPaymentRequired',
    'HTTPForbidden',
    'HTTPNotFound',
    'HTTPMethodNotAllowed',
    'HTTPNotAcceptable',
    'HTTPProxyAuthenticationRequired',
    'HTTPRequestTimeout',
    'HTTPConflict',
    'HTTPGone',
    'HTTPLengthRequired',
    'HTTPPreconditionFailed',
    'HTTPRequestEntityTooLarge',
    'HTTPRequestUriTooLong',
    'HTTPUnsupportedMediaType',
    'HTTPRequestedRangeNotSatisfiable',
    'HTTPExpectationFailed',
    'HTTPImATeapot',
    'HTTPMisdirectedRequest',
    'HTTPUnprocessableEntity',
    'HTTPLocked',
    'HTTPFailedDependency',
    'HTTPTooEarly',
    'HTTPUpgradeRequired',
    'HTTPPreconditionRequired',
    'HTTPTooManyRequests',
    'HTTPRequestHeaderFieldsTooLarge',
    'HTTPUnavailableForLegalReasons',
    # 500
    'HTTPInternalServerError',
    'HTTPNotImplemented',
    'HTTPBadGateway',
    'HTTPServiceUnavailable',
    'HTTPGatewayTimeout',
    'HTTPHttpServerVersionNotSupported',
    'HTTPVariantAlsoNegotiates',
    'HTTPInsufficientStorage',
    'HTTPLoopDetected',
    'HTTPNotExtended',
    'HTTPNetworkAuthenticationRequired',
    # Definitions
    'ERROR_RESPONSE_MAPPING',
]

# ======================
#        Typing
# ======================
Response = Union[str, bytes, dict, list, BaseModel]
RawResponse = Union[str, bytes]


# ======================
#   Generalized Errors
# ======================
class FrameworkException(Exception):
    """The core exception for all exceptions used in the API framework."""
    pass


class MISSING(FrameworkException):
    """Raised when something is missing.

    This often serves as an alternative to a ``None`` value when that may actually
    carry meaning.
    """
    pass


class ValidationError(FrameworkException):
    """Raised when validating a variable's type."""
    pass


# ======================
#    Client Errors
# ======================
class ClientError(FrameworkException):
    """The parent exception for any client-specific errors."""
    pass


class AsyncClientError(ClientError):
    """
    .. inherits_from:: ClientError

    The parent exception for any async client-specific errors.
    """
    pass


class SyncClientError(ClientError):
    """
    .. inherits_from:: ClientError

    The parent exception for any sync client-specific errors.
    """
    pass


# ======================
#    Request Errors
# ======================
class ResponseParseError(ClientError):
    """
    .. inherits_from:: ClientError

    The exception for failure to parse the response to request.

    This is usually raised if the response body was not readable by :py:func:`json.loads`.

    Attributes
    ----------
        raw_response: Union[:py:class:`str`, :py:class:`bytes`]
            The raw response that was unable to be parsed.
    """
    raw_response: RawResponse

    def __init__(self, raw_response: RawResponse):
        self.raw_response = raw_response


class HTTPError(FrameworkException):
    """The base exception for any request errors.

    See :httpcode:`this resource <name-status-codes>` for information about HTTP protocols.

    Attributes
    ----------
        status_code: :py:class:`int`
            The status code of the error.
        response: Union[:py:class:`str`, :py:class:`bytes`, :py:class:`dict`, :py:class:`list`, :class:`BaseModel`]
            The response that was received that raised the error.
    """
    status_code: int = None
    response: Response = None

    def __init__(self, response: Response):
        self.response = response


class HTTPRedirect(HTTPError):
    """
    .. inherits_from:: HTTPError

    Raised for any ``3xx Redirection`` responses.

    These codes indicate that further action needs to be taken by the user in order to fulfill the request.

    See :httpcode:`this resource <status.3xx>` for information about ``3xx HTTP`` responses.
    """
    pass


class HTTPClientError(HTTPError):
    """
    .. inherits_from:: HTTPError

    Raised for any ``4xx Client Error`` responses.

    These codes occur when an error has occurred as a result of the client application or user input,
    such as a malformed request.

    See :httpcode:`this resource <status.4xx>` for information about ``4xx HTTP`` responses.
    """
    pass


class HTTPServerError(HTTPError):
    """
    .. inherits_from:: HTTPError

    Raised for any ``5xx Server Error`` responses.

    These codes occur when the server is aware that is has made an error, or is incapable of performing the request.

    See :httpcode:`this resource <status.5xx>` for information about ``5xx HTTP`` responses.
    """
    pass


# 300
class HTTPMultipleChoices(HTTPRedirect):
    """
    .. inherits_from:: HTTPRedirect

    :httpcode:`300: Multiple Choices <status.300>`

    Raised when a 300 error is received, meaning that the request has more than one possible response,
    and the request needs to be more specific.
    """
    status_code = HTTP_300_MULTIPLE_CHOICES


class HTTPMovedPermanently(HTTPRedirect):
    """
    .. inherits_from:: HTTPRedirect

    :httpcode:`301: Moved Permanently <status.301>`

    Raised when a 301 error is received, meaning that the requested resource has been permanently
    moved to a different URL.
    """
    status_code = HTTP_301_MOVED_PERMANENTLY


class HTTPFound(HTTPRedirect):
    """
    .. inherits_from:: HTTPRedirect

    :httpcode:`302: Found <status.302>`

    Raised when a 302 error is received, meaning that the request resource has been temporarily moved to a
    different URL.
    """
    status_code = HTTP_302_FOUND


class HTTPSeeOther(HTTPRedirect):
    """
    .. inherits_from:: HTTPRedirect

    :httpcode:`303: See Other <status.303>`

    Raised when a 303 error is received, meaning that the request has linked to another page instead of responding.

    This is usually raised by ``PUT`` or ``POST`` requests, because the redirected page must always be displayed with
    a ``GET`` request.
    """
    status_code = HTTP_303_SEE_OTHER


class HTTPNotModified(HTTPRedirect):
    """"
    .. inherits_from:: HTTPRedirect

    :httpcode:`304: Not Modified <status.304>`

    Raised when a 304 error is received, meaning that the requested resource does not need to be transmitted again,
    as it is simply a redirection to a cached resource.
    """
    status_code = HTTP_304_NOT_MODIFIED


class HTTPUseProxy(HTTPRedirect):
    """
    .. inherits_from:: HTTPRedirect

    :httpcode:`305: Use Proxy <status.305>`

    Raised when a 305 error is received, meaning that the resource requested is only available through a proxy.
    """
    status_code = HTTP_305_USE_PROXY


class HTTPReserved(HTTPRedirect):
    """
    .. inherits_from:: HTTPRedirect

    :httpcode:`306: (Unused) <status.306>`
    """
    status_code = HTTP_306_RESERVED


class HTTPTemporaryRedirect(HTTPRedirect):
    """
    .. inherits_from:: HTTPRedirect

    :httpcode:`307: Temporary Redirect <status.307>`
    """
    status_code = HTTP_307_TEMPORARY_REDIRECT


class HTTPPermanentRedirect(HTTPRedirect):
    """
    .. inherits_from:: HTTPRedirect

    :httpcode:`308: Permanent Redirect <status.308>`
    """

    status_code = HTTP_308_PERMANENT_REDIRECT


# 400
class HTTPBadRequest(HTTPClientError):
    status_code = HTTP_400_BAD_REQUEST


class HTTPUnauthorized(HTTPClientError):
    status_code = HTTP_401_UNAUTHORIZED


class HTTPPaymentRequired(HTTPClientError):
    status_code = HTTP_402_PAYMENT_REQUIRED


class HTTPForbidden(HTTPClientError):
    status_code = HTTP_403_FORBIDDEN


class HTTPNotFound(HTTPClientError):
    status_code = HTTP_404_NOT_FOUND


class HTTPMethodNotAllowed(HTTPClientError):
    status_code = HTTP_405_METHOD_NOT_ALLOWED


class HTTPNotAcceptable(HTTPClientError):
    status_code = HTTP_406_NOT_ACCEPTABLE


class HTTPProxyAuthenticationRequired(HTTPClientError):
    status_code = HTTP_407_PROXY_AUTHENTICATION_REQUIRED


class HTTPRequestTimeout(HTTPClientError):
    status_code = HTTP_408_REQUEST_TIMEOUT


class HTTPConflict(HTTPClientError):
    status_code = HTTP_409_CONFLICT


class HTTPGone(HTTPClientError):
    status_code = HTTP_410_GONE


class HTTPLengthRequired(HTTPClientError):
    status_code = HTTP_411_LENGTH_REQUIRED


class HTTPPreconditionFailed(HTTPClientError):
    status_code = HTTP_412_PRECONDITION_FAILED


class HTTPRequestEntityTooLarge(HTTPClientError):
    status_code = HTTP_413_REQUEST_ENTITY_TOO_LARGE


class HTTPRequestUriTooLong(HTTPClientError):
    status_code = HTTP_414_REQUEST_URI_TOO_LONG


class HTTPUnsupportedMediaType(HTTPClientError):
    status_code = HTTP_415_UNSUPPORTED_MEDIA_TYPE


class HTTPRequestedRangeNotSatisfiable(HTTPClientError):
    status_code = HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE


class HTTPExpectationFailed(HTTPClientError):
    status_code = HTTP_417_EXPECTATION_FAILED


class HTTPImATeapot(HTTPClientError):
    status_code = HTTP_418_IM_A_TEAPOT


class HTTPMisdirectedRequest(HTTPClientError):
    status_code = HTTP_421_MISDIRECTED_REQUEST


class HTTPUnprocessableEntity(HTTPClientError):
    status_code = HTTP_422_UNPROCESSABLE_ENTITY


class HTTPLocked(HTTPClientError):
    status_code = HTTP_423_LOCKED


class HTTPFailedDependency(HTTPClientError):
    status_code = HTTP_424_FAILED_DEPENDENCY


class HTTPTooEarly(HTTPClientError):
    status_code = HTTP_425_TOO_EARLY


class HTTPUpgradeRequired(HTTPClientError):
    status_code = HTTP_426_UPGRADE_REQUIRED


class HTTPPreconditionRequired(HTTPClientError):
    status_code = HTTP_428_PRECONDITION_REQUIRED


class HTTPTooManyRequests(HTTPClientError):
    status_code = HTTP_429_TOO_MANY_REQUESTS


class HTTPRequestHeaderFieldsTooLarge(HTTPClientError):
    status_code = HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE


class HTTPUnavailableForLegalReasons(HTTPClientError):
    status_code = HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS


# 500
class HTTPInternalServerError(HTTPServerError):
    status_code = HTTP_500_INTERNAL_SERVER_ERROR


class HTTPNotImplemented(HTTPServerError):
    status_code = HTTP_501_NOT_IMPLEMENTED


class HTTPBadGateway(HTTPServerError):
    status_code = HTTP_502_BAD_GATEWAY


class HTTPServiceUnavailable(HTTPServerError):
    status_code = HTTP_503_SERVICE_UNAVAILABLE


class HTTPGatewayTimeout(HTTPServerError):
    status_code = HTTP_504_GATEWAY_TIMEOUT


class HTTPHttpServerVersionNotSupported(HTTPServerError):
    status_code = HTTP_505_HTTP_VERSION_NOT_SUPPORTED


class HTTPVariantAlsoNegotiates(HTTPServerError):
    status_code = HTTP_506_VARIANT_ALSO_NEGOTIATES


class HTTPInsufficientStorage(HTTPServerError):
    status_code = HTTP_507_INSUFFICIENT_STORAGE


class HTTPLoopDetected(HTTPServerError):
    status_code = HTTP_508_LOOP_DETECTED


class HTTPNotExtended(HTTPServerError):
    status_code = HTTP_510_NOT_EXTENDED


class HTTPNetworkAuthenticationRequired(HTTPServerError):
    status_code = HTTP_511_NETWORK_AUTHENTICATION_REQUIRED


# Map errors codes to their related exception classes.
ERROR_RESPONSE_MAPPING = {
    # 300
    HTTP_300_MULTIPLE_CHOICES: HTTPMultipleChoices,
    HTTP_301_MOVED_PERMANENTLY: HTTPMovedPermanently,
    HTTP_302_FOUND: HTTPFound,
    HTTP_303_SEE_OTHER: HTTPSeeOther,
    HTTP_304_NOT_MODIFIED: HTTPNotModified,
    HTTP_305_USE_PROXY: HTTPUseProxy,
    HTTP_306_RESERVED: HTTPReserved,
    HTTP_307_TEMPORARY_REDIRECT: HTTPTemporaryRedirect,
    HTTP_308_PERMANENT_REDIRECT: HTTPPermanentRedirect,
    # 400
    HTTP_400_BAD_REQUEST: HTTPBadRequest,
    HTTP_401_UNAUTHORIZED: HTTPUnauthorized,
    HTTP_402_PAYMENT_REQUIRED: HTTPPaymentRequired,
    HTTP_403_FORBIDDEN: HTTPForbidden,
    HTTP_404_NOT_FOUND: HTTPNotFound,
    HTTP_405_METHOD_NOT_ALLOWED: HTTPMethodNotAllowed,
    HTTP_406_NOT_ACCEPTABLE: HTTPNotAcceptable,
    HTTP_407_PROXY_AUTHENTICATION_REQUIRED: HTTPProxyAuthenticationRequired,
    HTTP_408_REQUEST_TIMEOUT: HTTPRequestTimeout,
    HTTP_409_CONFLICT: HTTPConflict,
    HTTP_410_GONE: HTTPGone,
    HTTP_411_LENGTH_REQUIRED: HTTPLengthRequired,
    HTTP_412_PRECONDITION_FAILED: HTTPPreconditionFailed,
    HTTP_413_REQUEST_ENTITY_TOO_LARGE: HTTPRequestEntityTooLarge,
    HTTP_414_REQUEST_URI_TOO_LONG: HTTPRequestUriTooLong,
    HTTP_415_UNSUPPORTED_MEDIA_TYPE: HTTPUnsupportedMediaType,
    HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE: HTTPRequestedRangeNotSatisfiable,
    HTTP_417_EXPECTATION_FAILED: HTTPExpectationFailed,
    HTTP_418_IM_A_TEAPOT: HTTPImATeapot,
    HTTP_421_MISDIRECTED_REQUEST: HTTPMisdirectedRequest,
    HTTP_422_UNPROCESSABLE_ENTITY: HTTPUnprocessableEntity,
    HTTP_423_LOCKED: HTTPLocked,
    HTTP_424_FAILED_DEPENDENCY: HTTPFailedDependency,
    HTTP_425_TOO_EARLY: HTTPTooEarly,
    HTTP_426_UPGRADE_REQUIRED: HTTPUpgradeRequired,
    HTTP_428_PRECONDITION_REQUIRED: HTTPPreconditionRequired,
    HTTP_429_TOO_MANY_REQUESTS: HTTPTooManyRequests,
    HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE: HTTPRequestHeaderFieldsTooLarge,
    HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS: HTTPUnavailableForLegalReasons,
    # 500
    HTTP_500_INTERNAL_SERVER_ERROR: HTTPInternalServerError,
    HTTP_501_NOT_IMPLEMENTED: HTTPNotImplemented,
    HTTP_502_BAD_GATEWAY: HTTPBadGateway,
    HTTP_503_SERVICE_UNAVAILABLE: HTTPServiceUnavailable,
    HTTP_504_GATEWAY_TIMEOUT: HTTPGatewayTimeout,
    HTTP_505_HTTP_VERSION_NOT_SUPPORTED: HTTPHttpServerVersionNotSupported,
    HTTP_506_VARIANT_ALSO_NEGOTIATES: HTTPVariantAlsoNegotiates,
    HTTP_507_INSUFFICIENT_STORAGE: HTTPInsufficientStorage,
    HTTP_508_LOOP_DETECTED: HTTPLoopDetected,
    HTTP_510_NOT_EXTENDED: HTTPNotExtended,
    HTTP_511_NETWORK_AUTHENTICATION_REQUIRED: HTTPNetworkAuthenticationRequired,
}

