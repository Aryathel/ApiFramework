import logging

from arya_api_framework import SyncClient
from arya_api_framework.utils import apiclient, endpoint

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from extensions.test import MySubClient


logging.basicConfig(level=logging.INFO)


@apiclient
class MySyncClient(
    SyncClient,
    uri="https://postman-echo.com",
    extensions=['extensions.test']
):
    testing: 'MySubClient'
    api_key: str

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.parameters['api_key'] = self.api_key

    @endpoint(
        path='/get',
        name='Base Get Test',
        method='GET'
    )
    def get_test(self):
        return self.get('/get')


if __name__ == "__main__":
    client = MySyncClient(api_key='mysecretkey')
    print(client.tree(True, 2))

    get = client.get('/get', parameters={"testing": "param1"})
    post = client.post('/post', data=b'Testing')
    put = client.put('/put', data={"form": "args"})
    patch = client.patch('/patch', data={"patch": ["args1", "args2"]})
    delete = client.delete('/delete', parameters={"testing": "param2"})
    upload = client.upload_file('test.txt', '/post')
    upload = client.stream_file('test2.txt', '/post')
    
    print(get, post, put, patch, delete, sep='\n\n')

    print(client.get_test())
    print(client.testing.get_test())
    print(client.testing.anotherone.get_test())

    client.close()
