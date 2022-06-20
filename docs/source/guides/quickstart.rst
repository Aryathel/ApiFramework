.. currentmodule:: arya_api_framework

.. _quickstart:

Quickstart
==========
Welcome to Arya's API Framework!

I am Arya, the creator and maintainer of this project. To get started, this guide will show you how
to create a basic API client using `{JSON} Placeholder <https://jsonplaceholder.typicode.com/>`_. This is is a very
simple set of API endpoints that allows you to test various RESTful API request methods. For this example, the
``sync`` branch will be used, but the same process applies to the ``async`` branch as well.

A final note before I begin, but this quickstart might be a little longer than most people are familiar with.
This is because this library is intended for building other libraries that are API wrappers, not to be used
directly on its own.

Full Example
~~~~~~~~~~~~

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

.. _quickstart-breakdown:

Breakdown
~~~~~~~~~

Breaking down the above example, this is how the general development process of this example would progress.

Create a Client
---------------

First, we have to create the client class. This class is going to be the primary interface between the developer and the
API:

.. code-block:: python
    :caption: api.py
    :linenos:

    from arya_api_framework import SyncClient

    class PlaceholderClient(SyncClient, uri="https://jsonplaceholder.typicode.com"):
        pass

To initialize this, the :paramref:`SyncClient.uri` subclass parameter will be used. Right away, this is already
a usable client for making requests with:

.. code-block:: python
    :caption: main.py
    :linenos:

    from api import PlaceholderClient

    if __name__ == "__main__":
        client = PlaceholderClient()

        users = client.get('/users')
        print(users)
        # [{"id": 1, ...}, {"id": 2, ...}, ...]

        user = client.get('/users/1')
        print(user)
        # {"id": 1, ...}

This will access https://jsonplaceholder.typicode.com/users and get the JSON data from that endpoint.

Creating API Request Methods
----------------------------

Now that the client exists, we can create wrapper methods to provide a simpler interface for users to query API
endpoints easier. At the same, the :pydantic:`@validate_arguments() <usage/validation_decorator/>` decorator is
used in order to enforce ``Pydantic`` type validations.

.. code-block:: python
    :caption: api.py
    :linenos:
    :emphasize-lines: 2, 5-12

    from arya_api_framework import SyncClient
    from pydantic import validate_arguments

    class PlaceholderClient(SyncClient, uri="https://jsonplaceholder.typicode.com"):
        def get_users(self):
            # Get a list of all users.
            return self.get('/users')

        @validate_arguments()
        def get_user_by_id(self, user_id: int):
            # Get a single user by their ID.
            return self.get(f'/users/{user_id}')

.. code-block:: python
    :caption: main.py
    :linenos:
    :emphasize-lines: 6, 8, 10, 12

    from api import PlaceholderClient

    if __name__ == "__main__":
        client = PlaceholderClient()

        users = client.get_users()
        print(users)
        # [{"id": 1, ...}, {"id": 2, ...}, ...]

        user = client.get_user_by_id(1)
        print(user)
        # {"id": 1, ...}

This can be expanded to other endpoints as well, but currently, data is only retrieved in a JSON :py:class:`dict`
format.

Creating Data Models
--------------------

The real strength of this framework comes into play when we start integrating :resource:`pydantic <pydantic>` models.
This models allow for direct data validation and returning request responses as an object. To do this, let's model the
``user`` element from the placeholder API. You can see an example of this structure
`here <https://jsonplaceholder.typicode.com/users/1>`_.

.. code-block::
    :caption: models.py
    :linenos:

    from arya_api_framework import Response

    class User(Response):
        id: int
        name: str
        username: str
        email: str
        address: dict
        phone: str
        website: str
        company: dict

The :class:`Response` is a direct subclass of the standard pydantic
:pydantic:`BaseModel <usage/models/#basic-model-usage>`. By creating your own custom response format from this model,
we gain access to more information about the request, such as the base URI of the request, and the time at which the
request was received.

.. code-block:: python
    :caption: api.py
    :linenos:
    :emphasize-lines: 4, 9, 14

    from arya_api_framework import SyncClient
    from pydantic import validate_arguments

    from models import User

    class PlaceholderClient(SyncClient, uri="https://jsonplaceholder.typicode.com"):
        def get_users(self):
            # Get a list of all users.
            return self.get('/users', response_format=User)

        @validate_arguments()
        def get_user_by_id(self, user_id: int):
            # Get a single user by their ID.
            return self.get(f'/users/{user_id}', response_format=User)

By passing the ``User`` response model into the :paramref:`response_format <SyncClass.get.response_format>` parameter,
the client will automatically attempt to load the request's response into the ``User`` model.

.. code-block:: python
    :caption: main.py
    :linenos:
    :emphasize-lines: 8, 12

    from api import PlaceholderClient

    if __name__ == "__main__":
        client = PlaceholderClient()

        users = client.get_users()
        print(users)
        # [User(id=1 ...), User(id=2 ...), ...]

        user = client.get_user_by_id(1)
        print(user)
        # User(id=1 ...)

However, in this case, if you try to access the ``address`` field of the ``User`` model, you will just receive a
raw :py:class:`dict` in return.

Complete Data Models
--------------------

If you want full object-oriented representation of your response, you can do so by creating further models and marking
the related fields as being of that data type:

.. code-block::
    :caption: models.py
    :linenos:
    :emphasize-lines: 1, 3-17, 23, 26

    from arya_api_framework import Response, BaseModel

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

Note here that models which are not going to be direct responses from the api are :class:`BaseModel` subclasses, while
the actual responses are :class:`Response` subclasses. With this, the same previous example will retrieve complete
object-oriented representation for the data responses.

Model Queries
-------------

While it is not necessary to do so, you can also use data models as arguments when making a request.

.. code-block::
    :caption: queries.py
    :linenos:

    from typing import Optional

    from arya_api_framework import BaseModel

    class AddressQuery(BaseModel):
        city: Optional[str]

    class UserQuery(BaseModel):
        username: Optional[str]
        address: Optional[AddressQuery]

By doing so, you now have the option to search by those fields provided in the query.

.. note::

    As an alternative to creating separate classes specifically for the queries, you could also mark the fields of
    the standard data models as ``Optional[<type>]`` instead, and then use those models for the queries.

.. code-block:: python
    :caption: api.py
    :linenos:
    :emphasize-lines: 5, 17-45

    from arya_api_framework import SyncClient
    from pydantic import validate_arguments

    from models import User
    from queries import UserQuery, AddressQuery

    class PlaceholderClient(SyncClient, uri="https://jsonplaceholder.typicode.com"):
        def get_users(self):
            # Get a list of all users.
            return self.get('/users', response_format=User)

        @validate_arguments()
        def get_user_by_id(self, user_id: int):
            # Get a single user by their ID.
            return self.get(f'/users/{user_id}', response_format=User)

        @validate_arguments()
        def search_user_by_username(self, name: str):
            # Get a list of users with the given username.
            query = UserQuery(username=name)

            return self.get('/users', parameters=query, response_format=User)

        @validate_arguments()
        def search_user_by_city(self, city: str):
            # Get a list of users with an address in the given city.
            query = UserQuery(
                address=AddressQuery(
                    city=city
                )
            )

            return self.get('/users', parameters=query, response_format=User)

        @validate_arguments()
        def search_user_by_username_and_city(self, name: str, city: str):
            # Get a list of users with a given username and an address in the given city.
            query = UserQuery(
                username=name,
                address=AddressQuery(
                    city=city
                )
            )

            return self.get('/users', parameters=query, response_format=User)

.. code-block:: python
    :caption: main.py
    :linenos:
    :emphasize-lines: 14-24

    from api import PlaceholderClient

    if __name__ == "__main__":
        client = PlaceholderClient()

        users = client.get_users()
        print(users)
        # [User(id=1 ...), User(id=2 ...), ...]

        user = client.get_user_by_id(1)
        print(user)
        # User(id=1 ...)

        lookup = client.search_user_by_username("Samantha")
        print(lookup)
        # [User(id=3 ...)]

        lookup = client.search_user_by_city("McKenziehaven")
        print(lookup)
        # [User(id=3 ...)]

        lookup = client.search_user_by_username_and_city("Bret", "Gwenborough")
        print(lookup)
        # [User(id=1 ...)]

Closing Thoughts
~~~~~~~~~~~~~~~~

From here on out, it's up to you! This library is left very open-ended for a reason. This is intended to be utilized
as a generalized base for crafting API libraries, so the implementation of data validation, individual request methods,
rate limits, etc. is all up to you. Keep in mind that a complete documentation of all of the features can be found
in the :ref:`API Reference <api_reference>` on the home page.