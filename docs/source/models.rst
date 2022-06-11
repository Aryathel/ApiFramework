.. currentmodule:: arya_api_framework

Data Models
===========

Here are a collection of basic data structures to be used when making requests with the API clients.

Basic Models
------------

.. attributetable:: BaseModel
    :inherited: all

.. autoclass:: BaseModel
    :members:


Response Models
---------------

These models are used to define what a response that you receive is expected to look like.

Response
~~~~~~~~

.. attributetable:: Response, BaseModel

.. autoclass:: Response
    :members:

Paginated Response
~~~~~~~~~~~~~~~~~~

.. attributetable:: PaginatedResponse, Response, BaseModel

.. autoclass:: PaginatedResponse
    :members:
