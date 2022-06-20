Arya's API Framework
====================

.. only:: html

    .. list-table::
        :stub-columns: 1
        :widths: 10 90

        * - Docs
          - |docs|
        * - PyPI
          - |pypi-version| |supported-versions| |supported-implementations| |wheel|
        * - Activity
          - |commits-latest| |maintained| |pypi-downloads|
        * - QA
          - |codefactor|
        * - Other
          - |license| |language|

.. |docs| image:: https://img.shields.io/readthedocs/apiframework/latest?logo=read-the-docs&color=8566D9&logoColor=white
    :class: shield
    :target: https://apiframework.readthedocs.io/en/latest/
    :alt: RTFD - Docs Build Status

.. |pypi-version| image:: https://img.shields.io/pypi/v/arya-api-framework?color=8566D9
    :class: shield
    :target: https://pypi.org/project/arya-api-framework/
    :alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/arya-api-framework?logo=python&logoColor=white&color=8566D9
    :class: shield
    :target: https://pypi.org/project/arya-api-framework/
    :alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/arya-api-framework?color=8566D9
    :class: shield
    :target: https://pypi.org/project/arya-api-framework/
    :alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/arya-api-framework?color=8566D9
    :class: shield
    :target: https://pypi.org/project/arya-api-framework/
    :alt: PyPI - Wheel

.. |commits-latest| image:: https://img.shields.io/github/last-commit/Aryathel/ApiFramework/main?color=8566D9
    :class: shield
    :target: https://github.com/Aryathel/APIFramework
    :alt: Github - Last Commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2022?color=8566D9
    :class: shield
    :target: https://github.com/Aryathel/APIFramework/commit/main
    :alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/arya-api-framework?color=8566D9
    :class: shield
    :target: https://pypistats.org/packages/arya-api-framework
    :alt: PyPI - Downloads

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/Aryathel/ApiFramework?logo=codefactor&color=8566D9&logoColor=white
    :class: shield
    :target: https://www.codefactor.io/repository/github/Aryathel/ApiFramework
    :alt: CodeFactor - Grade

.. |license| image:: https://img.shields.io/github/license/Aryathel/ApiFramework?color=8566D9
    :class: shield
    :target: https://github.com/Aryathel/ApiFramework/blob/main/LICENSE
    :alt: GitHub - License

.. |language| image:: https://img.shields.io/github/languages/top/Aryathel/ApiFramework?color=8566D9
    :class: shield
    :target: https://github.com/Aryathel/ApiFramework
    :alt: GitHub - Top Language

This module is designed to be a base for the creation of clients that interact with RESTful web APIs.

**Features:**
   - Synchronous branch utilizing :resource:`requests <requests>`.
   - Asynchronous branch utilizing :resource:`aiohttp <aiohttp>`.
   - Integrated with :resource:`pydantic <pydantic>` for strict typing.

.. admonition:: Disclaimer

    This library is not intended for fast, performant code. It is instead optimized for user-friendliness and strict
    data typing. While this will likely not be a noticeable issue for many users, please keep this in mind.


Installation
------------

To install the sync branch:

.. code-block:: sh

   pip install arya-api-framework[sync]

To install the async branch:

.. code-block:: sh

   pip install arya-api-framework[async]

Getting Started
---------------

This example is a minimal example. However, it is still much more than most libraries have
for a getting started page. This is because of this modules usage of :resource:`Pydantic <pydantic>`
for data validation from API responses. If you would like a breakdown of this, please see the
:ref:`quickstart-breakdown` section, or take a look at the available :ref:`guides`.

.. code-block:: python
    :caption: models.py
    :linenos:

    from arya_api_framework import BaseModel, Response

    # Data models
    class Geo(BaseModel):
        lat: float
        lng: float

    class Address(BaseModel):
        street: str
        suite: str
        city: str
        zipcode: str
        geo: Geo

    class Company(BaseModel):
        name: str
        catchPhrase: str
        bs: str

    class User(Response):
        id: int
        name: str
        email: str
        address: Address
        phone: str
        website: str
        company: Company

    # Query models
    class AddressQuery(BaseModel):
        city: Optional[str]

    class UserQuery(BaseModel):
        username: Optional[str]
        address: Optional[AddressQuery]

.. code-block:: python
    :caption: api.py
    :linenos:

    from arya_api_framework import SyncClient
    from pydantic import validate_arguments

    from models import User, UserQuery, AddressQuery

    class PlaceholderClient(SyncClient, uri="https://jsonplaceholder.typicode.com"):
        def get_users(self):
            # https://jsonplaceholder.typicode.com/users
            return self.get('/users', response_format=User)

        @validate_arguments()
        def get_user_by_id(self, id: int):
            # https://jsonplaceholder.typicode.com/users/<id>
            return self.get(f'/users/{id}', response_format=User)

        @validate_arguments()
        def search_user_by_username(self, name: str):
            # https://jsonplaceholder.typicode.com/users?username=<name>
            query = UserQuery(username=name)

            return self.get('/users', parameters=query, response_format=User)

        @validate_arguments()
        def search_user_by_city(self, city: str):
            # https://jsonplaceholder.typicode.com/users?address.city=<city>
            query = UserQuery(address=AddressQuery(city=city))

            return self.get('/users', parameters=query, response_format=User)

        @validate_arguments()
        def search_user_by_username_and_city(self, name: str, city: str):
            # https://jsonplaceholder.typicode.com/users?username=<name>&address.city=<city>
            query = UserQuery(username=name, address=AddressQuery(city=city))

            return self.get('/users', parameters=query, response_format=User)

.. code-block:: python
    :caption: main.py
    :linenos:

    from api import PlaceholderClient

    if __name__ == "__main__":
        client = PlaceholderClient()

        users = client.get_users()
        print(users)

        user = client.get_user_by_id(3)
        print(user)

        lookup = client.search_user_by_username("Bret")
        print(lookup)

        lookup = client.search_user_by_city("Gwenborough")
        print(lookup)

        lookup = client.search_user_by_username_and_city("Bret", "Gwenborough")
        print(lookup)

.. _guides:

Guides
------
These guides are intended to be a place where those looking to really take advantage
of the features this system has can get started.

.. toctree::
    :maxdepth: 1

    guides/quickstart
    guides/logging
    guides/subclients

.. _api_reference:

API Reference
--------------
.. toctree::
    :maxdepth: 2

    framework
    exceptions

Information
-----------
Here lies a bunch of random information related to the project at least a little bit.

.. toctree::
    :maxdepth: 2

    info/statuses

Glossary
--------
If you are struggling to find specific information, see these references:

    * `Search <search.html>`_
    * `Glossary <genindex.html>`_

TODO Features
-------------

.. checklist::
    :check:`Rate Limits (Allow rate limit application for limited APIs.)`
    :uncheck:`Response Caching (Reduce processing times/network load.)`
    :uncheck:`Sub-Clients (For creating API category modules.)`
