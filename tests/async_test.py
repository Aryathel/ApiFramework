import asyncio
import logging
from typing import TYPE_CHECKING

from arya_api_framework import AsyncClient
from arya_api_framework.utils import apiclient, endpoint

if TYPE_CHECKING:
    from extensions.test import MySubClient

logging.basicConfig(level=logging.INFO)


@apiclient
class MyAsyncClient(AsyncClient, uri="https://postman-echo.com", extensions=['extensions.test']):
    testing: 'MySubClient'
    api_key: str

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.parameters['apiKey'] = self.api_key

    @endpoint(
        path='/get',
        name='Base Get Test',
        method='GET'
    )
    def get_test(self):
        return self.get('/get')


async def main():
    client = MyAsyncClient(api_key='mysecretkey')

    get = await client.get('/get', parameters={"testing": "param1"})
    post = await client.post('/post', data=b'Testing')
    put = await client.put('/put', data={"form": "args"})
    patch = await client.patch('/patch', data={"patch": ["args1", "args2"]})
    delete = await client.delete('/delete', parameters={"testing": "param2"})
    upload = await client.upload_file('test.txt', '/post')
    upload = await client.stream_file('test2.txt', '/post')

    print(get, post, put, patch, delete, sep='\n\n')

    print(await client.get_test())
    print(await client.testing.get_test())
    print(await client.testing.anotherone.get_test())

    print(client.tree(True, 2))

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
