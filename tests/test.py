from arya_api_framework import SyncClient, Response, BaseModel
from typing import Dict

import logging
logging.basicConfig(level=logging.INFO)


class MyArgs(BaseModel):
    api_key: str
    test: str


class MyResponse(Response):
    args: MyArgs
    headers: Dict[str, str]
    url: str


class MySyncClient(SyncClient):
    api_key: str

    def __post_init__(self, *args, api_key: str = None, **kwargs):
        self.api_key = api_key
        self.parameters['api_key'] = self.api_key


if __name__ == "__main__":
    client = MySyncClient('https://postman-echo.com/get', api_key='mysecretkey')
    print(client.get())
    client.parameters['e'] = "test"
    client.close()
    print(client.get())
