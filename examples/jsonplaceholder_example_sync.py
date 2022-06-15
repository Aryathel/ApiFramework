import logging
from typing import Optional

from arya_api_framework import SyncClient, Response, BaseModel
from pydantic import validate_arguments


logging.basicConfig(level=logging.INFO)


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


class AddressQuery(BaseModel):
    city: Optional[str]


class UserQuery(BaseModel):
    username: Optional[str]
    address: Optional[AddressQuery]


class PlaceholderClient(SyncClient, uri="https://jsonplaceholder.typicode.com"):
    def get_users(self):
        return self.get('/users', response_format=User)

    @validate_arguments()
    def get_user_by_id(self, id: int):
        return self.get(f'/users/{id}', response_format=User)

    @validate_arguments()
    def search_user_by_username(self, name: str):
        query = UserQuery(username=name)

        return self.get('/users', parameters=query, response_format=User)

    @validate_arguments()
    def search_user_by_city(self, city: str):
        query = UserQuery(address=AddressQuery(city=city))

        return self.get('/users', parameters=query, response_format=User)

    @validate_arguments()
    def search_user_by_username_and_city(self, name: str, city: str):
        query = UserQuery(username=name, address=AddressQuery(city=city))

        return self.get('/users', parameters=query, response_format=User)


if __name__ == "__main__":
    client = PlaceholderClient()

    users = client.get_users()
    print(users)

    user = client.get_user_by_id(3)
    print(repr(user))

    lookup = client.search_user_by_username("Samantha")
    print(lookup)

    lookup = client.search_user_by_city("McKenziehaven")
    print(lookup)

    lookup = client.search_user_by_username_and_city("Bret", "Gwenborough")
    print(lookup)
