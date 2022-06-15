import asyncio
import logging

from arya_api_framework import AsyncClient


logging.basicConfig(level=logging.INFO)


class MySyncClient(AsyncClient, uri="https://postman-echo.com"):
    api_key: str

    def __post_init__(self, *args, api_key: str = None, **kwargs):
        self.api_key = api_key
        self.parameters['api_key'] = self.api_key


async def main():
    client = MySyncClient(api_key='mysecretkey')

    get = await client.get('/get', parameters={"testing": "param1"})
    post = await client.post('/post', data=b'Testing')
    put = await client.put('/put', data={"form": "args"})
    patch = await client.patch('/patch', data={"patch": ["args1", "args2"]})
    delete = await client.delete('/delete', parameters={"testing": "param2"})
    upload = await client.upload_file('test.txt', '/post')

    await client.close()

    print(get, post, put, patch, delete, sep='\n\n')

if __name__ == "__main__":
    asyncio.run(main())
