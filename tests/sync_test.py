import logging

from arya_api_framework import SyncClient


logging.basicConfig(level=logging.INFO)


class MySyncClient(SyncClient, uri="https://postman-echo.com"):
    api_key: str

    def __post_init__(self, *args, api_key: str = None, **kwargs):
        self.api_key = api_key
        self.parameters['api_key'] = self.api_key


if __name__ == "__main__":
    client = MySyncClient(api_key='mysecretkey')

    get = client.get('/get', parameters={"testing": "param1"})
    post = client.post('/post', data=b'Testing')
    put = client.put('/put', data={"form": "args"})
    patch = client.patch('/patch', data={"patch": ["args1", "args2"]})
    delete = client.delete('/delete', parameters={"testing": "param2"})
    upload = client.upload_file('test.txt', '/post')
    upload = client.stream_file('test2.txt', '/post')

    client.close()

    print(get, post, put, patch, delete, sep='\n\n')
