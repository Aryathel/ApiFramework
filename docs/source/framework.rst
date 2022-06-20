.. currentmodule:: arya_api_framework

API Reference
=====================
These are the most common structures that will be included in nearly every project.

Sync Client
-----------

.. attributetable:: SyncClient

.. autoclass:: SyncClient
    :inherited-members:

Async Client
------------

.. attributetable:: AsyncClient

.. autoclass:: AsyncClient
    :inherited-members:

Sub Client
----------

.. attributetable:: SubClient

.. autoclass:: SubClient
    :members:

Data Models
-----------

Here are a collection of basic data structures to be used when making requests with the API clients.

Basic Models
~~~~~~~~~~~~

The basic :resource:`pydantic <pydantic>` model that incorporates data validation.
This usage of this model for requests is one of the reasons why this library is useful.

.. attributetable:: BaseModel
    :inherited: all

.. autoclass:: BaseModel
    :members:


Response Models
~~~~~~~~~~~~~~~

These models are used to define what a response that you receive is expected to look like.

.. attributetable:: Response, BaseModel

.. autoclass:: Response
    :members:

.. attributetable:: PaginatedResponse, Response, BaseModel

.. autoclass:: PaginatedResponse
    :members:


.. currentmodule:: arya_api_framework.constants

Enums
-----

.. autoenum:: HTTPMethod


.. currentmodule:: arya_api_framework.utils

Utility Functions
-----------------

.. autofunction:: flatten_obj

.. autofunction:: merge_dicts

.. autofunction:: validate_type

.. autodecorator:: apiclient

.. autodecorator:: endpoint
