.. _web-info:

Web Information
****************

*Sources:* [MDNHTTP]_, [RFC9110]_, [RFC9111]_

Alright, let's talk about the interweb. Given that most people seeing this and who are interested in creating an
API client will likely already have some knowledge of most of these things, feel free to skip over it. However,
this page is intended as a comprehensive primer for people of all experience levels into generalized internet
infrastructure.

These sections include:

    * :ref:`http-requests`
    * :ref:`http-status-codes`

.. _terms:

Terminology
===========

Before getting into that, it is important to clarify some terminology that will be used throughout the
document:

.. list-table::
    :widths: 15, 85
    :header-rows: 1

    * - Term
      - Definition
    * - Cache
      - An HTTP "cache" is a local storage of responses that a client will control storage, retrieval, and deletion of data in. Cached data is used to reduce response times and network bandwidth consumption.
    * - Client
      - Some entity that is sending a request to a server.
    * - Cookie
      - An HTTP cookie is a small block of data created by a web server that is left on the client's side after a request is made. These cookies allow server to store client/user specific data on the individual client's end, and keep track of the state of the session. This can include staying logged in to a website, saving items in a shopping cart, and much more.
    * - Header
      - A header is a field in an HTTP request that passes additional context about the request, e.g. media formats, operating system, authorization, and just about anything else. Additionally, a response sent to a request will also include headers from the server.
    * - HTTP
      - The The HTTP, or Hypertext Transfer Protocol, is an application-level protocol for information systems. The modern HTTP forms the foundation for nearly the entirety of the average users' web experience. This is why you will see many website URLs starting with ``http://`` or ``https://``, as these are the protocols used to communicate with those websites.
    * - Proxy
      - A server which provides a gateway between a user/client and the end-server. The client sends requests to the proxy, which forwards them to the end server, and then returns the response back to the client.
    * - Request
      - An HTTP request that is sent from a client, to a server, expecting some form or response/action to be taken upon being received.
    * - Resource
      - The target of an HTTP request is called a resource. This is not limited in any way as to what this resource might be, HTTP merely defines an interaction method for the client to access this resource.
    * - Response
      - A message send from a server, to a client, in response to a received request. This will always include a status code, and usually come content besides that.
    * - Server
      - An entity which can receive requests from a client, and execute some action or send some response (or both) as a result.
    * - URI
      - A URI, or Uniform Resource Identifier, is a unique sequence of characters that defines how to navigate to a web resource. These can include URLs and URNs.
    * - URL
      - A URL, or Uniform Resource Locator, is a type of URI that specifically provides a location on a network and a mechanism for retrieving data from that location.
    * - URN
      - A URN, or Uniform Resource Name, is a type of URI that is a template for parsers to use to find an item. This can be a server namespace and other routing information, but does not inherently give access to any data.
    * - User Agent
      - A ``user agent`` refers to the client program. For example, your browser that you are likely reading this in will set a user agent like ``Chrome/100.0.4896.127`` to refer to a specific version of Google Chrome.
    * - WebSocket
      - An interactive connection that makes consistent two-way communication between a client and a server possible.


.. _http-requests:

HTTP Request Methods
====================
:http:`[RFC9110.9] <section-9>`
`[MDN Methods] <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods>`_

When an HTTP request is made, the first piece of information any server or request-builder will ask you for is the
method. This request method is used as a primary source of how to treat the request. It directly tells the server
what the intention of the client is, and what the server should send to the client as a result. There are currently
9 major request methods, which are as follows:

.. list-table::
    :widths: 15, 85
    :header-rows: 1

    * - Method
      - Description
    * - :ref:`get`
      - The primary method for information retrieval, ``GET`` requests retrieve data specified by the client.
    * - :ref:`head`
      - Identical to the :ref:`get` method, except the server does not send content. This is used primarily for obtaining metadata and resource content types.
    * - :ref:`post`
      - The primary method for giving data to a server. This method requests that the resource processes the request information, and will often send nothing other than a confirmation in response.
    * - :ref:`put`
      - Requests that the target resource is either created or replaced by the data defined by the request.
    * - :ref:`delete`
      - Requests that the server remove the data at the targeted location specified by the request.
    * - :ref:`connect`
      - Requests that the targeted server further connect to another resource defined by the request, and then act purely as transport for data between the original client and the end server.
    * - :ref:`options`
      - Requests information about communication options for the target resource.
    * - :ref:`trace`
      - Intended largely for gathering testing or diagnostic information, the ``TRACE`` method does not see much use. Additionally, due to some security risks, almost all production web environments do not allow this method.
    * - :ref:`patch`
      - Similarly to a :ref:`put` request, a ``PATCH`` request is used to update a resource. However, unlike the ``PUT`` method, which passes a complete representation of the resource, the ``PATCH`` method can give instructions on how to modify an existing resource.

.. _get:

GET
----
:http:`[RFC9110.9.3.1] <section-9.3.1>`

The ``GET`` request method is intended for information retrieval. This method is far and away the most common request
type that most developers will deal with, especilly those building an application on top of an existing API structure.
But even out outside of developers, there are ``GET`` requests everywhere. Every time you open a web page in your
browser? That's a ``GET`` request that your browser makes to the resource at the URL you entered, and the HTML
document that gets displayed is the response to that request.

In many ways, ``GET`` requests can be looked at as database queries. A set of criteria, parameters even, are often
provided to the resource, and the resource takes those criteria and returns a response containing the relevant
information.

.. _head:

HEAD
----
:http:`[RFC9110.9.3.2] <section-9.3.2>`

The ``HEAD`` request method is identical to the :ref:`get` method, except the server will not send any content in the
response. The head method is used for a client to obtain metadata about a resource, rather than directly obtaining
the resource itself.

The response from the server should include all of the headers that the :ref:`get` request would, but simply without
the content itself. However, some headers that are dependent on being set when the content is generated for the response
may not be set, so this is not a guarantee.

.. _post:

POST
----
:http:`[RFC9110.9.3.3] <section-9.3.3>`

The ``POST`` request method requests that the targeted resource processes the data enclosed in the request according to
that resource's implementation. Some common examples of post requests are:

* Submitting a form on a website.
* Posting a message on a forum.
* Creating a new resource.
* Adding data to a resource.

.. note::

    If a resource is created as a result of a ``POST`` request, it should return a :ref:`201` status code. ``POST`` requests
    may return some form of confirmation response, or sometimes include a redirection to the location of a resource where
    the ``POST`` data can be found.

.. _put:

PUT
----
:http:`[RFC9110.9.3.4] <section-9.3.4>`

The ``PUT`` request method requests that the state of the target resource be created or replaced with the data defined
in the request. A successful ``PUT`` request usually means that a followup :ref:`get` request would result in an
equivalent data to the ``PUT`` request being returned.

If a ``PUT`` request creates a resource on the server, the server will return a :ref:`201` status code. Otherwise, if
the ``PUT`` request updates a resource, the server should send a :ref:`200` or a :ref:`201` status code.

A server which receives a ``PUT`` request should validate the enclosed data according to its own methods before
accepting the request.

.. _delete:

DELETE
------
:http:`[RFC9110.9.3.5] <section-9.3.5>`

The ``DELETE`` method requests that the origin server remove a target resource from its functionality. The goal is that
the endpoint specified will delete the resource. For example, if an API request targets an image library website,
a ``DELETE`` request may request the deletion of a specific image.

.. _connect:

CONNECT
-------
:http:`[RFC9110.9.3.6] <section-9.3.6>`

The ``CONNECT`` request method requests that the recipient server establish a tunnel to the destination server.
The in-between server (a :ref:`proxy server <terms>`) will then server purely to facilitate communication between
the client and the server. There can be multiple proxies chained together before reaching the end server.

.. _options:

OPTIONS
-------
:http:`[RFC9110.9.3.7] <section-9.3.7>`

The ``OPTIONS`` request method is used to get information about the general communication options available for the
target resource. This allows a client to determine what options/requirements to associate with a resource endpoint,
without actually interacting with a resource.

For example, an ``OPTIONS`` request to a server endpoint might return a specific header ``allow``, which has a value
of ``GET, HEAD, OPTIONS`` , indicating what request methods are available.

.. note::

    By sending an ``OPTIONS`` request to the ``/*`` resource URL, the generalized request options allowed for the server
    as a whole are returned. However, since many server resources have separately configured enabled methods, this
    feature should probably not be used for anything more than a ping method.

.. _trace:

TRACE
-----
:http:`[RFC9110.9.3.8] <section-9.3.8>`

The ``TRACE`` request method requests a remote loop-back of the request message. This enables a client to see what
information the server receives when the request is received. However, this has previously been used to acquire
sensitive user data, and should make sure that no private/sensitive data is conveyed in the request.

Realistically, the ``TRACE`` method should only be used for debugging/development environments, not in production.

.. _patch:

PATCH
-----
`[MDN Methods PATCH] <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH>`_

The ``PATCH`` method requests partial changes to be made to a resource. Instead of the :ref:`put` or :ref:`post` methods,
where resources are created of overwritten, the ``PATCH`` method is used to modify an existing resource in-place.

This is not a very common feature, but at a general level, can be implemented similarly to ``PUT`` or ``POST`` methods.

.. _http-status-codes:

HTTP Status Codes
=================
:http:`[RFC9110.15] <section-15>`
`[MDN Statuses] <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status>`_

An HTTP status code is 3-digit identifier attached to the response of any request made. Similarly to the request method,
this identifier can be used to direct different actions that can be taken by the clients based on the codes of the
responses received. In this 3-digit code, the first digit defines the category of the response, while the second two
digits have no meaning other than to differentiate themselves from the others within that category.

Before getting into the status codes, however, here are a few terms that I will be using consistently throughout the
document. These are fairly common/easy-to-understand terms, but for the sake of avoiding confusion, I will put these
here anyways:

That being said, the 5 primary status code categories are as follows:

.. list-table::
    :widths: 20, 80
    :header-rows: 1

    * - Category
      - Description
    * - :ref:`1xx`
      - The :ref:`request <terms>` was received, and the process is continuing.
    * - :ref:`2xx`
      - The :ref:`request <terms>` was successfully received, understood, and accepted.
    * - :ref:`3xx`
      - Further action needs to be taken by the :ref:`client <terms>` in order to complete the :ref:`request <terms>`.
    * - :ref:`4xx`
      - The :ref:`request <terms>` contains bad syntax or could not be fulfilled as a result of an error on the requesting :ref:`client <terms>`'s side.
    * - :ref:`5xx`
      - The :ref:`server <terms>` failed to fulfill a :ref:`request <terms>` that seems to be valid.

It is important to note that when looking at these codes, however, that their actual implementations can very heavily
from server to server. Common codes like a :ref:`404` code are all relatively similar, but a :ref:`403` error can be
be caused by an endless number of things. In the end, it is up to each server individually to actually
implement these codes. As such, clients like this framework will often accept all available status codes,
but actually doing something with them requires separate implementation for each server.

The short version of the meaning behind this is: your client should be able to tell the difference between the status
code categories (1xx, 2xx, etc.), but the nuances of each individual error code are not as important on a broad scale.
Additionally, many clients will also use their own status codes outside of the accepted ones in order to internalize
their own response structures.

However, as someone working with an API structure, there are in a broad sense two situations that you need to be aware
of regarding the response to a request:

* The request was received correctly (almost always indicated by :ref:`200`) and the response can be processed.
* Some other status code was received, meaning that the request cannot be processed as though it were the expected response.

Keeping that in mind, if you are still interested in learning about all of the accepted HTTP status codes, I will keep
a glossary of them here.

.. _1xx:

1xx Informational
------------------
:http:`[RFC9110.15.2] <section-15.2>`

Alright, getting started, we have the category of status codes you will likely see the least: the ``1xx`` informational
codes. There are only two standardized codes in this category, and they are interim codes. What this means is that these
codes will never be the end result of a request, but rather just a, well, *informational* piece of data on the status of
the :ref:`request <terms>` while it continues to be processed. Most of the time, these codes get handled behind the scenes while
end-users and high-level developers never touch them.

    * :ref:`100`
    * :ref:`101`

.. _100:

100 Continue
~~~~~~~~~~~~
:http:`[RFC9110.15.2.1] <section-15.2.1>`

The ``100`` status code is sent when the initial part of a request has been received, and it has not been rejected by the
server. The server intends to respond to the :ref:`request <terms>` after fully receiving the request and acting on it. This is an
interim status code that conveys the :ref:`server <terms>`'s intentions to the :ref:`client <terms>`.

When the client makes their request, they might also include an ``Expect`` :ref:`header <terms>` in the request. When this header
is sent, and the value is set to ``100-continue``, the server can then send a :ref:`response <terms>` with the ``100`` status code to indicate
that it has acknowledged the intent of the client to send the request, and is willing to accept it. When the client
receives a ``100`` status code response after sending a request with an ``Expect`` header, the client should continue
sending the main body of the request and discard the ``100`` response.

.. tip::

    If the request that the client sent did *not* include the ``Expect`` header, then any ``100`` status code responses can
    simply be discarded.

.. _101:

101 Switching Protocols
~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.2.2] <section-15.2.2>`

The ``101`` status code indicates that the :ref:`server <terms>` understands and is willing to respond to the
:ref:`client <terms>`'s :ref:`request <terms>`. It does this via a :ref:`header <terms>` in the ``101``
:ref:`response <terms>`, the ``Upgrade`` header. This header carries information on what protocol the server intends
to switch to.

.. tip::

    Arguably the most common/easy-to-understand version of this is when opening a :ref:`WebSocket <terms>` connection, the
    client will first send an HTTP GET request with the ``Upgrade`` header set to ``websocket``, and the ``Connection``
    header set to ``Upgrade``. If the :ref:`server <terms>`

.. _2xx:

2xx Successful
---------------
:http:`[RFC9110.15.3] <section-15.3>`

The ``2xx`` class of status codes indicate that the client's request was successfully received by the server,
understood, and also accepted. In short, a ``2xx`` response means that the request was valid.

.. _200:

200 OK
~~~~~~
:http:`[RFC9110.15.3.1] <section-15.3.1>`

The ``200`` status code indicates that the request has succeeded. The response information contained in a ``200``
response often depends on the method being used. Here are some examples of what a ``200`` code might refer to:

.. list-table::
    :widths: 15, 85
    :header-rows: 1

    * - Method
      - Refers to
    * - :ref:`get`
      - The target resource.
    * - :ref:`head`
      - The target resource, but without the included data.
    * - :ref:`post`
      - The status of, or results of, the action.
    * - :ref:`put`, :ref:`delete`, :ref:`patch`
      - The status of the action.
    * - :ref:`trace`
      - The request message the server received.

.. _201:

201 Created
~~~~~~~~~~~
:http:`[RFC9110.15.3.2] <section-15.3.2>`

The ``201`` status code indicates that the request has been fulfilled and resulted in at least one new resource
being created. The ``201`` response's content usually described how to target these new resource(s).

.. _202:

202 Accepted
~~~~~~~~~~~~
:http:`[RFC9110.15.3.3] <section-15.3.3>`

The ``202`` status code indicates that the request has been received, but the processing has not been completed.
This can be useful for long processing of data, as this simply informs the client that the response is being worked on.

.. _203:

203 Non-Authoritative Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.3.4] <section-15.3.4>`

The ``203`` status code indicates that the request was successful but the information contained within was modified by a
proxy on the way back to the client. This allows a proxy to notify a client when it has modified data.

.. _204:

204 No Content
~~~~~~~~~~~~~~
:http:`[RFC9110.15.3.5] <section-15.3.5>`

The ``204`` status code indicates that the server has successfully filled the request and there is no additional
content to send in the response content. This serves as a confirmation of success to the user without actually sending
any proper data in return.

.. _205:

205 Reset Content
~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.3.6] <section-15.3.6>`

The ``205`` status code indicates that the server has fulfilled the request and desires that the user reset the
"document view" to its original state. This can be received, for example, in response to submitting a form
where the user might want to enter another item into the form. Upon receiving the ``205`` response, the client would
reset the form fields to their defaults without needing to process any data from the response.

.. note::

    A ``205`` response will not contain any content.

.. _206:

206 Partial Content
~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.3.7] <section-15.3.7>`

The ``206`` status code indicates that the server is sending a partial amount of data as a response to a request.
This is usually in relation to range requests, where something like a large file is passed to the client in smaller
chunks over separate requests instead of a single request that may timeout/drop the connection.


.. _3xx:

3xx Redirect
------------
:http:`[RFC9110.15.4] <section-15.4>`

The ``3xx`` class of status codes indicate that further action is needed from the client in order to fulfill the
request. There are 4 main types of redirections:

    #. Redirections that indicate that the resource has been moved to a different location (e.g. :ref:`301`, :ref:`307`).
    #. Redirections that offer a choice among multiple options capable of representing the resource (e.g. :ref:`300`).
    #. Redirection to a different resource (e.g. :ref:`303`).
    #. Redirection to a previously cached result (e.g. :ref:`304`).

For some redirect responses, the client may automatically redirect the request to the provided URI referenced in the
redirect response. However, this should be done with care, and only for requests that are known to be safe, as the user
may not want to redirect an unsafe request.

.. _300:

300 Multiple Choices
~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.4.1] <section-15.4.1>`

The ``300`` status code indicates that the target resource has more than one endpoint to access it from.
In ths case, the server should provide the alternate URIs to target the resource from so that the client/user can select
one.

.. note::

    If any of these choices are preferred over the others by the server, the response should include a ``Location`` header
    which contains the URL for the preferred choice.

.. _301:

301 Moved Permanently
~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.4.2] <section-15.4.2>`

The ``301`` status code indicates that the target resource has been assigned a new URI permanently, and the request
should be re-issued to a new permanent URI. The response should include a ``Location`` header which contains the new
preferred URL for the resource.

.. _302:

302 Found
~~~~~~~~~
:http:`[RFC9110.15.4.3] <section-15.4.3>`

The ``302`` status code indicates that the target resource is temporarily found under a different URI. However, since
the location of the target resource is only temporarily moved, the requests should continue to be sent to the current
URI for future requests. This should include a ``Location`` header in the response with a new URI to direct the request
to.

.. note::

    This is highly similar to :ref:`307`, the only different really being in come client implementations.

.. _303:

303 See Other
~~~~~~~~~~~~~
:http:`[RFC9110.15.4.4] <section-15.4.4>`

The ``303`` status code inficates that the server is redirecting the user to a different resource from the one
requested, indicated by a URL in the ``Location`` header. This is intended to redirect a client to interact with a
a separate URL.

.. _304:

304 Not Modified
~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.4.5] <section-15.4.5>`

The ``304`` status code indicates that a conditional :ref:`get` or :ref:`head` request was received, and would have
returned a :ref:`200` response if not for the condition evaluating to ``False``. This means that the server has no need
to transfer the resource, because the client can use the cached data instead.

.. note::

    See `[RFC9111] <https://www.rfc-editor.org/rfc/rfc9111.html>`_ for information on HTTP caching.

.. _305:

305 Use Proxy
~~~~~~~~~~~~~
:http:`[RFC9110.15.4.6] <section-15.4.6>`

The ``305`` status code has been deprecated in a previous HTTP version and is no longer used.

.. _306:

306 (Unused)
~~~~~~~~~~~~
:http:`[RFC9110.15.4.7] <section-15.4.7>`

The ``306`` status code was previously removed, and is no longer used. However, the response code is still reserved.

.. _307:

307 Temporary Redirect
~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.4.8] <section-15.4.8>`

The ``307`` status code indicates that the target resource is temporarily found under a different URI. However, since
the location of the target resource is only temporarily moved, the requests should continue to be sent to the current
URI for future requests. This should include a ``Location`` header in the response with a new URI to direct the request
to.

.. note::

    This is highly similar to :ref:`302`, the only different really being in come client implementations.

.. _308:

308 Permanent Redirect
~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.4.9] <section-15.4.9>`

The ``308`` status code indicates that the target resource has been assigned a new permanent URI. This means that the
current, and any future requests, should be directed to the URI enclosed in the ``Location`` header, which should be
provided.

.. _4xx:

4xx Client Error
----------------
:http:`[RFC9110.15.5] <section-15.5>`
`[MDN Statuses Client Error] <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#client_error_responses>`_

The ``4xx`` class of status code indicates that the client has made some form of mistake with the request. Unless the
request uses the :ref:`head` method, the server should return content which describes how the client has erred.

.. _400:

400 Bad Request
~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.1] <section-15.5.1>`

The ``400`` status code is used to indicate that the server cannot or will not process the request due to an improper
request. This can be caused by a large variety of things, but some common errors include syntax errors, invalid request
structure, or untrusted request routing.

.. _401:

401 Unauthorized
~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.2] <section-15.5.2>`

The ``401`` status code indicates that the request has not been applied because it does not have valid authentication
credentials for the target resource. This generally means that the ``Authorization`` header was either not provided,
or invalid.

.. _402:

402 Payment Required
~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.3] <section-15.5.3>`

The ``402`` status code is not currently used, but is reserved for future use.

.. _403:

403 Forbidden
~~~~~~~~~~~~~
:http:`[RFC9110.15.5.4] <section-15.5.4>`

The ``403`` status code indicates that the server understood the request but refuses to fulfill it. The server may share
why that request was refused, but also may not. If the ``Authorization`` header was passed with this request, the server
has decided that the credentials provided were valid, but insufficient for accessing the requested resource.

.. _404:

404 Not Found
~~~~~~~~~~~~~
:http:`[RFC9110.15.5.5] <section-15.5.5>`

The ``404`` status code indicates that either the server did not find a resource at the requested target location, or
the server is refusing to disclose that that endpoint exists. This status code does not indicate whether the not found
status is temporary or permanent.

.. _405:

405 Method Not Allowed
~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.6] <section-15.5.6>`

The ``405`` status code indicates that the attempted request method is known by the server, but is not allowed/supported
for the target resource. The response should include an ``Allow`` header which specifies what request methods are
allowed.

.. _406:

406 Not Acceptable
~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.7] <section-15.5.7>`

The ``406`` status code indicates that the target location does not have a resource that is acceptable to the client,
according to the :http:`proactive negotiation [RFC9110.12.1] <section-12.1>` header field. This is a fairly unlikely
response code, given that proactive negotiation can be very inconsistent and is not highly recommended.

.. _407:

407 Proxy Authentication Required
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.8] <section-15.5.8>`

The ``407`` status code is similar to :ref:`401`, except it indicates that the client needs to authenticate itself in
order to use a proxy for the request.

.. _408:

408 Request Timeout
~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.9] <section-15.5.9>`

The ``408`` status code indicates that the server did not receive the full request from the client in a time it was
willing to wait for.

.. _409:

409 Conflict
~~~~~~~~~~~~
:http:`[RFC9110.15.5.10] <section-15.5.10>`

The ``409`` status code indicates that the request could not be completed due to a conflict with the state of the target
resource. This code is used in situations where the client/user can somehow resolve said conflict and resend the
request. For example, if a :ref:`put` request is changing a resource that override changes previously made by another
external user, the ``409`` response code might indicate that the request cannot be completed.

.. _410:

410 Gone
~~~~~~~~
:http:`[RFC9110.15.5.11] <section-15.5.11>`

The ``410`` status code indicates that access to the target resource is no longer available at the target server, and
that this is a permanent condition. If the permanence of the target resource availability is not known, or is not
permanent, a :ref:`404` error will be used instead.

.. _411:

411 Length Required
~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.12] <section-15.5.12>`

The ``411`` status code indicates that the server refuses to accept the request without a defined ``Content-Length``
header.

.. _412:

412 Precondition Failed
~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.13] <section-15.5.13>`

The ``412`` status code indicates that one or more conditions given in the request headers evaluated to ``False`` on the
server side. This response allows the client to apply pre-conditions to accessing a resource, and prevent the request
from being executed if the target resource is in an unexpected state.

.. _413:

413 Content Too Large
~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.14] <section-15.5.14>`

The ``413`` status code indicates that the server is refusing to process a request because the content is larger than
the server will process.

.. _414:

414 URI Too Long
~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.15] <section-15.5.15>`

The ``414`` status code indicates that the server is refusing the request because the target URI is longer than the
server will allow. This is a very rare status code that is only likely if a client converts a :ref:`post` request
to a :ref:`get` request accidentally, resulting in an infinite redirection.

.. _415:

415 Unsupported Media Type
~~~~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.16] <section-15.5.16>`

The ``415`` status code indicates the origin server is refusing to accept the request because the content type is not
in a format supported by the resource. This is usually due to a mistake in the ``Content-Type`` or ``Content-Encoding``
headers. The response may also include a ``Accept-Encoding`` or ``Accept`` header to specify what valid options are.

.. _416:

416 Range Not Satisfiable
~~~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.17] <section-15.5.17>`

The ``416`` status code indicates that the set of ranges in the ``Range`` header field have been rejected.

.. _417:

417 Expectation Failed
~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.18] <section-15.5.18>`

The ``417`` status code indicates that the expectation given in the ``Expect`` header field could not be met.

.. _418:

418 (Unused)
~~~~~~~~~~~~
:http:`[RFC9110.15.5.19] <section-15.5.19>`

Now unused, the ``418`` status code was originally created/reserved as an April Fools joke.

.. _421:

421 Misdirected Request
~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.20] <section-15.5.20>`

The ``421`` status code indicates that the request was directed at a server that is unable to produce a response for the
target URI. An server might return a ``421`` status code for a request that has an invalid origin URI.

.. _422:

422 Unprocessable Content
~~~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.21] <section-15.5.21>`

The ``422`` status code indicates that the server understands the content type of the request, and the syntax of the
request is correct, but it was unable to process the contained data. This might include a JSON request body which
is valid syntactically, but contains invalid/missing fields.

.. _424:

424 Object Required
~~~~~~~~~~~~~~~~~~~
`[MS object-required-error-424] <https://docs.microsoft.com/en-us/office/vba/language/reference/user-interface-help/object-required-error-424>`_

The ``424`` status code indicates that the provided object data in the request are invalid for the resource requested.
This might be a result of no providing and object, providing an object that isn't recognized, or providing an invalid
object altogether.

.. _425:

425 Too Early
~~~~~~~~~~~~~
`[MDN Status 425] <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/425>`_

The ``425`` status code indicates that the server is unwilling to risk processing a request which might be replayed,
which has a potential for a `replay attack <https://en.wikipedia.org/wiki/Replay_attack>`_.

.. _426:

426 Upgrade Required
~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.22] <section-15.5.22>`

The ``426`` status code indicates that the server refused to perform the request using the current protocol, but might
be willing to do so after the client switches to a different protocol. The server will provide an ``Upgrade`` header
in the response to indicate the required protocols.

.. _428:

428 Precondition Required
~~~~~~~~~~~~~~~~~~~~~~~~~
`[MDN Status 428] <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/428>`_

The ``428`` status code indicates that the server requires the request to be conditional. This usually means that a
required precondition header is missing, like ``If-Match``.

.. note::

    When a precondition does not match the server-side accepted conditions, a :ref:`412` error should be raised. The
    ``428`` code is reserved for a *missing* precondition.

.. _429:

429 Too Many Requests
~~~~~~~~~~~~~~~~~~~~~
`[MDN Status 429] <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429>`_

The ``429`` status code indicates that the user has sent too many requests in a given amount of time. This is commonly
referred to as hitting a "rate limit".

.. note::

    A ``429`` response may include a ``Retry-After`` header which indicates how long to wait before retrying the
    request.

.. _431:

431 Request header Fields Too Large
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`[MDN Status 431] <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/431>`_

The ``431`` status code indicates that the server will not process the request because the requests headers are too
long. This can refer to both the entirety of the headers being too long, or the length of an individual header
being too long.

.. note::

    Servers should implement some sort of content in a ``431`` response that explains how or what headers are too large.
    However, some common occurrences are if:

        * The ``Referer`` URL header is too long.
        * There are too many cookies in the request.

.. _451:

451 Unavailable for Legal Reasons
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`[MDN Status 451] <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/451>`_

The ``451`` status code indicates that the user requested a resource that is not available due to legal reasons. This
might be because the web page has has legal action taken against it.

.. _5xx:

5xx Server Error
----------------
:http:`[RFC9110.15.6] <section-15.6>`
`[MDN Statuses Server Error] <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#server_error_responses>`_

The ``5xx`` class of status codes refer to errors that occur on the side of the server. The server should include
some information about the error in the response content, unless the request is made with the :ref:`get` method, in
which case no content will be sent.

.. _500:

500 Internal Server Error
~~~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.6.1] <section-15.6.1>`

The ``500`` status code indicates that the server encounter an unexpected error preventing it from completing the
request. This is a very broad error case.

.. _501:

501 Not Implemented
~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.6.2] <section-15.6.2>`

The ``501`` status code indicates that the server does not support the requirements for fulfilling a request.

.. _502:

502 Bad Gateway
~~~~~~~~~~~~~~~
:http:`[RFC9110.15.6.3] <section-15.6.3>`

The ``502`` status code indicates that the server received an invalid response from an inbound server it accessed
while attempting to fulfill the request. This often occurs in the case of a proxy server receiving an invalid
response.

.. _503:

503 Service Unavailable
~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.6.4] <section-15.6.4>`

The ``503`` status code indicates that the server is currently unable to handle the request due to a temporary
overload or maintenance.

.. _504:

504 Gateway Timeout
~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.6.5] <section-15.6.5>`

The ``504`` status code indicates that the server did not receive a response, within the time it was willing to wait,
from another server.

.. _505:

505 HTTP Version Not Supported
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.6.6] <section-15.6.6>`

The ``505`` status code indicates that the server does not support the major HTTP version that the request was made
with.

.. _506:

506 Variant Also Negotiates
~~~~~~~~~~~~~~~~~~~~~~~~~~~
`[MDN Status 506] <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/506>`_

Honestly, I don't know how to explain this one and I have never seen it before. Take a look at the source link
`here <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/506>`_ if you want to learn more.

.. _507:

507 Insufficient Storage
~~~~~~~~~~~~~~~~~~~~~~~~
`[MDN Status 507] <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/507>`_

Status code ``507`` indicates that the request could not be completed because the server could not store the data needed
to complete the request.

.. _508:

508 Loop Detected
~~~~~~~~~~~~~~~~~
`[MDN Status 508] <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/508>`_

The ``508`` status code indicates that the server terminated an operation because it encountered an infinite loop while
processing a request.

.. _510:

510 Not Extended
~~~~~~~~~~~~~~~~
`[MDN Status 510] <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/510>`_

The ``510`` status code indicates that the server could not use a specified extension that the client's request
incorporated.

.. _511:

511 Network Authentication Required
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`[MDN Status 511] <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/511>`_

The ``511`` status code indicates that the client needs to authenticate to gain network access. This status is generated
by proxies that control access to a network rather than the network server itself.

Reference
=========

.. [MDNHTTP] HTTP | MDN. (2022, May 13). MDN Web Docs. Retrieved June 13, 2022,
    from https://developer.mozilla.org/en-US/docs/Web/HTTP .

.. [RFC9110] Fielding, R., Ed., Nottingham, M., Ed., and J. Reschke, Ed., "HTTP Semantics", STD 97, RFC 9110,
    DOI 10.17487/RFC9110, June 2022, https://datatracker.ietf.org/doc/html/rfc9110 .

.. [RFC9111] Fielding, R., Ed., Nottingham, M., Ed., and J. Reschke, Ed., "HTTP Caching", STD 98, RFC 9111,
    DOI 10.17487/RFC9111, June 2022, https://www.rfc-editor.org/info/rfc9111 .