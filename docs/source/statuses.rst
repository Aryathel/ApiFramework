.. _web-info:

Web Information
****************

*Source* [RFC9110]_

Alright, let's talk about the interweb. Given that most people seeing this and who are interested in creating an
API client will likely already have some knowledge of most of these things, feel free to skip over it. However,
this page is intended as a comprehensive primer for people of all experience levels into generalized internet
infrastructure.

These sections include:

    * :ref:`http-requests`
    * :ref:`http-status-codes`

However, before getting into that, it is important to clarify some terminology that will be used throughout the
document:

.. _terms:

.. list-table::
    :widths: 15, 85
    :header-rows: 1

    * - Term
      - Definition
    * - HTTP
      - The The HTTP, or Hypertext Transfer Protocol, is an application-level protocol for information systems. The modern HTTP forms the foundation for nearly the entirety of the average users' web experience. This is why you will see many website URLs starting with ``http://`` or ``https://``, as these are the protocols used to communicate with those websites.
    * - Client
      - Some entity that is sending a request to a server.
    * - Header
      - A header is a field in an HTTP request that passes additional context about the request, e.g. media formats, operating system, authorization, and just about anything else. Additionally, a response sent to a request will also include headers from the server.
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
    * - User Agent
      - A ``user agent`` refers to the client program. For example, your browser that you are likely reading this in will set a user agent like ``Chrome/100.0.4896.127`` to refer to a specific version of Google Chrome.
    * - WebSocket
      - An interactive connection that makes consistent two-way communication between a client and a server possible.


.. _http-requests:

HTTP Request Methods
====================
:http:`[RFC9110.9] <section-9>`

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

If a resource is created as a result of a ``POST`` request, it should return a :ref:`201` status code. ``POST`` requests
may return some form of confirmation response, or sometimes include a redirection to the location of a resource where
the ``POST``ed data can be found.

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
This in-between server (a :ref:`proxy <terms>`

.. _options:

OPTIONS
-------
:http:`[RFC9110.9.3.7] <section-9.3.7>`

.. _trace:

TRACE
-----
:http:`[RFC9110.9.3.8] <section-9.3.8>`

.. _patch:

PATCH
-----
`Source <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH>`_

.. _http-status-codes:

HTTP Status Codes
=================
:http:`[RFC9110.15] <section-15>`

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

Arguably the most common/easy-to-understand version of this is when opening a :ref:`WebSocket <terms>` connection, the
client will first send an HTTP GET request with the ``Upgrade`` header set to ``websocket``, and the ``Connection``
header set to ``Upgrade``. If the :ref:`server <terms>`

.. _2xx:

2xx Successful
---------------
:http:`[RFC9110.15.3] <section-15.3>`

.. _200:

200 OK
~~~~~~
:http:`[RFC9110.15.3.1] <section-15.3.1>`

.. _201:

201 Created
~~~~~~~~~~~
:http:`[RFC9110.15.3.2] <section-15.3.2>`

.. _202:

202 Accepted
~~~~~~~~~~~~
:http:`[RFC9110.15.3.3] <section-15.3.3>`

.. _203:

203 Non-Authoritative Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.3.4] <section-15.3.4>`

.. _204:

204 No Content
~~~~~~~~~~~~~~
:http:`[RFC9110.15.3.5] <section-15.3.5>`

.. _205:

205 Reset Content
~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.3.6] <section-15.3.6>`

.. _206:

206 Partial Content
~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.3.7] <section-15.3.7>`

.. _3xx:

3xx Redirect
------------
:http:`[RFC9110.15.4] <section-15.4>`

.. _300:

300 Multiple Choices
~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.4.1] <section-15.4.1>`

.. _301:

301 Moved Permanently
~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.4.2] <section-15.4.2>`

.. _302:

302 Found
~~~~~~~~~
:http:`[RFC9110.15.4.3] <section-15.4.3>`

.. _303:

303 See Other
~~~~~~~~~~~~~
:http:`[RFC9110.15.4.4] <section-15.4.4>`

.. _304:

304 Not Modified
~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.4.5] <section-15.4.5>`

.. _305:

305 Use Proxy
~~~~~~~~~~~~~
:http:`[RFC9110.15.4.6] <section-15.4.6>`

.. _306:

306 (Unused)
~~~~~~~~~~~~
:http:`[RFC9110.15.4.7] <section-15.4.7>`

.. _307:

307 Temporary Redirect
~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.4.8] <section-15.4.8>`

.. _308:

308 Permanent Redirect
~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.4.9] <section-15.4.9>`

.. _4xx:

4xx Client Error
----------------
:http:`[RFC9110.15.5] <section-15.5>`

.. _400:

400 Bad Request
~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.1] <section-15.5.1>`

.. _401:

401 Unauthorized
~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.2] <section-15.5.2>`

.. _402:

402 Payment Required
~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.3] <section-15.5.3>`

.. _403:

403 Forbidden
~~~~~~~~~~~~~
:http:`[RFC9110.15.5.4] <section-15.5.4>`

.. _404:

404 Not Found
~~~~~~~~~~~~~
:http:`[RFC9110.15.5.5] <section-15.5.5>`

.. _405:

405 Method Not Allowed
~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.6] <section-15.5.6>`

.. _406:

406 Not Acceptable
~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.7] <section-15.5.7>`

.. _407:

407 Proxy Authentication Required
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.8] <section-15.5.8>`

.. _408:

408 Request Timeout
~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.9] <section-15.5.9>`

.. _409:

409 Conflict
~~~~~~~~~~~~
:http:`[RFC9110.15.5.10] <section-15.5.10>`

.. _410:

410 Gone
~~~~~~~~
:http:`[RFC9110.15.5.11] <section-15.5.11>`

.. _411:

411 Length Required
~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.12] <section-15.5.12>`

.. _412:

412 Precondition Failed
~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.13] <section-15.5.13>`

.. _413:

413 Content Too Large
~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.14] <section-15.5.14>`

.. _414:

414 URI Too Long
~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.15] <section-15.5.15>`

.. _415:

415 Unsupported Media Type
~~~~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.16] <section-15.5.16>`

.. _416:

416 Range Not Satisfiable
~~~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.17] <section-15.5.17>`

.. _417:

417 Expectation Failed
~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.18] <section-15.5.18>`

.. _418:

418 (Unused)
~~~~~~~~~~~~
:http:`[RFC9110.15.5.19] <section-15.5.19>`

.. _421:

421 Misdirected Request
~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.20] <section-15.5.20>`

.. _422:

422 Unprocessable Content
~~~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.21] <section-15.5.21>`

.. _426:

426 Upgrade Required
~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.5.22] <section-15.5.22>`

.. _5xx:

5xx Server Error
----------------
:http:`[RFC9110.15.6] <section-15.6>`

.. _500:

500 Internal Server Error
~~~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.6.1] <section-15.6.1>`

.. _501:

501 Not Implemented
~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.6.2] <section-15.6.2>`

.. _502:

502 Bad Gateway
~~~~~~~~~~~~~~~
:http:`[RFC9110.15.6.3] <section-15.6.3>`

.. _503:

503 Service Unavailable
~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.6.4] <section-15.6.4>`

.. _504:

504 Gateway Timeout
~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.6.5] <section-15.6.5>`

.. _505:

505 HTTP Version Not Supported
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:http:`[RFC9110.15.6.6] <section-15.6.6>`

Reference
=========

.. [RFC9110] Fielding, R., Ed., Nottingham, M., Ed., and J. Reschke, Ed., "HTTP Semantics", STD 97, RFC 9110,
    DOI 10.17487/RFC9110, June 2022, https://datatracker.ietf.org/doc/html/rfc9110 .