.. currentmodule:: arya_api_framework.errors

Exceptions
==========

General Exceptions
------------------

.. autoexception:: FrameworkException
.. autoexception:: MISSING
.. autoexception:: ValidationError

Extension Exceptions
--------------------

.. autoexception:: ExtensionError
.. attributetable:: ExtensionError
.. autoexception:: ExtensionNotFound
.. attributetable:: ExtensionNotFound, ExtensionError
.. autoexception:: ExtensionAlreadyLoaded
.. attributetable:: ExtensionAlreadyLoaded, ExtensionError
.. autoexception:: ExtensionNotLoaded
.. attributetable:: ExtensionNotLoaded, ExtensionError
.. autoexception:: ExtensionEntryPointError
.. attributetable:: ExtensionEntryPointError, ExtensionError
.. autoexception:: ExtensionFailed
.. attributetable:: ExtensionFailed, ExtensionError

Client Exceptions
-----------------

.. autoexception:: ClientError
.. autoexception:: AsyncClientError
.. autoexception:: SyncClientError

Request Exceptions
------------------

.. autoexception:: ResponseParseError
.. attributetable:: ResponseParseError

.. autoexception:: HTTPError
.. attributetable:: HTTPError

.. autoexception:: HTTPRedirect
.. attributetable:: HTTPRedirect, HTTPError

.. autoexception:: HTTPClientError
.. attributetable:: HTTPClientError, HTTPError

.. autoexception:: HTTPServerError
.. attributetable:: HTTPServerError, HTTPError

300 Errors
~~~~~~~~~~

.. autoexception:: HTTPMultipleChoices
.. attributetable:: HTTPMultipleChoices, HTTPRedirect, HTTPError

.. autoexception:: HTTPMovedPermanently
.. attributetable:: HTTPMovedPermanently, HTTPRedirect, HTTPError

.. autoexception:: HTTPFound
.. attributetable:: HTTPFound, HTTPRedirect, HTTPError

.. autoexception:: HTTPSeeOther
.. attributetable:: HTTPSeeOther, HTTPRedirect, HTTPError

.. autoexception:: HTTPNotModified
.. attributetable:: HTTPNotModified, HTTPRedirect, HTTPError

.. autoexception:: HTTPUseProxy
.. attributetable:: HTTPUseProxy, HTTPRedirect, HTTPError

.. autoexception:: HTTPReserved
.. attributetable:: HTTPReserved, HTTPRedirect, HTTPError

.. autoexception:: HTTPTemporaryRedirect
.. attributetable:: HTTPTemporaryRedirect, HTTPRedirect, HTTPError

.. autoexception:: HTTPPermanentRedirect
.. attributetable:: HTTPPermanentRedirect, HTTPRedirect, HTTPError

400 Errors
~~~~~~~~~~

.. autoexception:: HTTPBadRequest
.. attributetable:: HTTPBadRequest, HTTPClientError, HTTPError

.. autoexception:: HTTPUnauthorized
.. attributetable:: HTTPUnauthorized, HTTPClientError, HTTPError

.. autoexception:: HTTPPaymentRequired
.. attributetable:: HTTPPaymentRequired, HTTPClientError, HTTPError

.. autoexception:: HTTPForbidden
.. attributetable:: HTTPForbidden, HTTPClientError, HTTPError

.. autoexception:: HTTPNotFound
.. attributetable:: HTTPNotFound, HTTPClientError, HTTPError

.. autoexception:: HTTPMethodNotAllowed
.. attributetable:: HTTPMethodNotAllowed, HTTPClientError, HTTPError

.. autoexception:: HTTPNotAcceptable
.. attributetable:: HTTPNotAcceptable, HTTPClientError, HTTPError

.. autoexception:: HTTPProxyAuthenticationRequired
.. attributetable:: HTTPProxyAuthenticationRequired, HTTPClientError, HTTPError

.. autoexception:: HTTPRequestTimeout
.. attributetable:: HTTPRequestTimeout, HTTPClientError, HTTPError

.. autoexception:: HTTPConflict
.. attributetable:: HTTPConflict, HTTPClientError, HTTPError

.. autoexception:: HTTPGone
.. attributetable:: HTTPGone, HTTPClientError, HTTPError

.. autoexception:: HTTPLengthRequired
.. attributetable:: HTTPLengthRequired, HTTPClientError, HTTPError

.. autoexception:: HTTPPreconditionFailed
.. attributetable:: HTTPPreconditionFailed, HTTPClientError, HTTPError

.. autoexception:: HTTPRequestEntityTooLarge
.. attributetable:: HTTPRequestEntityTooLarge, HTTPClientError, HTTPError

.. autoexception:: HTTPRequestUriTooLong
.. attributetable:: HTTPRequestUriTooLong, HTTPClientError, HTTPError

.. autoexception:: HTTPUnsupportedMediaType
.. attributetable:: HTTPUnsupportedMediaType, HTTPClientError, HTTPError

.. autoexception:: HTTPRequestedRangeNotSatisfiable
.. attributetable:: HTTPRequestedRangeNotSatisfiable, HTTPClientError, HTTPError

.. autoexception:: HTTPExpectationFailed
.. attributetable:: HTTPExpectationFailed, HTTPClientError, HTTPError

.. autoexception:: HTTPImATeapot
.. attributetable:: HTTPImATeapot, HTTPClientError, HTTPError

.. autoexception:: HTTPMisdirectedRequest
.. attributetable:: HTTPMisdirectedRequest, HTTPClientError, HTTPError

.. autoexception:: HTTPUnprocessableEntity
.. attributetable:: HTTPUnprocessableEntity, HTTPClientError, HTTPError

.. autoexception:: HTTPFailedDependency
.. attributetable:: HTTPFailedDependency, HTTPClientError, HTTPError

.. autoexception:: HTTPTooEarly
.. attributetable:: HTTPTooEarly, HTTPClientError, HTTPError

.. autoexception:: HTTPUpgradeRequired
.. attributetable:: HTTPUpgradeRequired, HTTPClientError, HTTPError

.. autoexception:: HTTPPreconditionRequired
.. attributetable:: HTTPPreconditionRequired, HTTPClientError, HTTPError

.. autoexception:: HTTPTooManyRequests
.. attributetable:: HTTPTooManyRequests, HTTPClientError, HTTPError

.. autoexception:: HTTPRequestHeaderFieldsTooLarge
.. attributetable:: HTTPRequestHeaderFieldsTooLarge, HTTPClientError, HTTPError

.. autoexception:: HTTPUnavailableForLegalReasons
.. attributetable:: HTTPUnavailableForLegalReasons, HTTPClientError, HTTPError

500 Errors
~~~~~~~~~~

.. autoexception:: HTTPInternalServerError
.. attributetable:: HTTPInternalServerError, HTTPServerError, HTTPError

.. autoexception:: HTTPNotImplemented
.. attributetable:: HTTPNotImplemented, HTTPServerError, HTTPError

.. autoexception:: HTTPBadGateway
.. attributetable:: HTTPBadGateway, HTTPServerError, HTTPError

.. autoexception:: HTTPServiceUnavailable
.. attributetable:: HTTPServiceUnavailable, HTTPServerError, HTTPError

.. autoexception:: HTTPGatewayTimeout
.. attributetable:: HTTPGatewayTimeout, HTTPServerError, HTTPError

.. autoexception:: HTTPHttpServerVersionNotSupported
.. attributetable:: HTTPHttpServerVersionNotSupported, HTTPServerError, HTTPError

.. autoexception:: HTTPVariantAlsoNegotiates
.. attributetable:: HTTPVariantAlsoNegotiates, HTTPServerError, HTTPError

.. autoexception:: HTTPInsufficientStorage
.. attributetable:: HTTPInsufficientStorage, HTTPServerError, HTTPError

.. autoexception:: HTTPLoopDetected
.. attributetable:: HTTPLoopDetected, HTTPServerError, HTTPError

.. autoexception:: HTTPNotExtended
.. attributetable:: HTTPNotExtended, HTTPServerError, HTTPError

.. autoexception:: HTTPNetworkAuthenticationRequired
.. attributetable:: HTTPNetworkAuthenticationRequired, HTTPServerError, HTTPError

.. _exceptions:

Exception Hierarchy
-------------------

.. exception_hierarchy::
    - :exc:`Exception`
        - :exc:`FrameworkException`
            - :exc:`MISSING`
            - :exc:`ValidationError`
            - :exc:`ExtensionError`
                - :exc:`ExtensionNotFound`
                - :exc:`ExtensionAlreadyLoaded`
                - :exc:`ExtensionNotLoaded`
                - :exc:`ExtensionEntryPointError`
                - :exc:`ExtensionFailed`
            - :exc:`ClientError`
                - :exc:`AsyncClientError`
                - :exc:`SyncClientError`
                - :exc:`ResponseParseError`
            - :exc:`HTTPError`
                - :exc:`HTTPRedirect`
                    - :exc:`HTTPMultipleChoices`
                    - :exc:`HTTPMovedPermanently`
                    - :exc:`HTTPFound`
                    - :exc:`HTTPSeeOther`
                    - :exc:`HTTPNotModified`
                    - :exc:`HTTPUseProxy`
                    - :exc:`HTTPReserved`
                    - :exc:`HTTPTemporaryRedirect`
                    - :exc:`HTTPPermanentRedirect`
                - :exc:`HTTPClientError`
                    - :exc:`HTTPBadRequest`
                    - :exc:`HTTPUnauthorized`
                    - :exc:`HTTPPaymentRequired`
                    - :exc:`HTTPForbidden`
                    - :exc:`HTTPNotFound`
                    - :exc:`HTTPMethodNotAllowed`
                    - :exc:`HTTPNotAcceptable`
                    - :exc:`HTTPProxyAuthenticationRequired`
                    - :exc:`HTTPRequestTimeout`
                    - :exc:`HTTPConflict`
                    - :exc:`HTTPGone`
                    - :exc:`HTTPLengthRequired`
                    - :exc:`HTTPPreconditionFailed`
                    - :exc:`HTTPRequestEntityTooLarge`
                    - :exc:`HTTPRequestUriTooLong`
                    - :exc:`HTTPUnsupportedMediaType`
                    - :exc:`HTTPRequestedRangeNotSatisfiable`
                    - :exc:`HTTPExpectationFailed`
                    - :exc:`HTTPImATeapot`
                    - :exc:`HTTPMisdirectedRequest`
                    - :exc:`HTTPUnprocessableEntity`
                    - :exc:`HTTPFailedDependency`
                    - :exc:`HTTPTooEarly`
                    - :exc:`HTTPUpgradeRequired`
                    - :exc:`HTTPPreconditionRequired`
                    - :exc:`HTTPTooManyRequests`
                    - :exc:`HTTPRequestHeaderFieldsTooLarge`
                    - :exc:`HTTPUnavailableForLegalReasons`
                - :exc:`HTTPServerError`
                    - :exc:`HTTPInternalServerError`
                    - :exc:`HTTPNotImplemented`
                    - :exc:`HTTPBadGateway`
                    - :exc:`HTTPServiceUnavailable`
                    - :exc:`HTTPGatewayTimeout`
                    - :exc:`HTTPHttpServerVersionNotSupported`
                    - :exc:`HTTPVariantAlsoNegotiates`
                    - :exc:`HTTPInsufficientStorage`
                    - :exc:`HTTPLoopDetected`
                    - :exc:`HTTPNotExtended`
                    - :exc:`HTTPNetworkAuthenticationRequired`