from typing import Union, Dict, Any

from arya_api_framework import SubClient, SyncClient, AsyncClient
from arya_api_framework.utils import apiclient, endpoint
from arya_api_framework.constants import HTTPMethod

DictStrSubClient = Dict[str, SubClient]


@apiclient
class MySubClient(SubClient, name='testing', relative_path='get'):
    anotherone: 'OtherSubClient'

    def on_loaded(self) -> None:
        print(f"Loaded {self.qualified_name}.")

    def on_unloaded(self) -> None:
        print(f"Unloaded {self.name}.")

    @endpoint(
        path='/get?showcontext=True',
        name='Testing',
        href='https://postman-echo.com/get#documentation-link',
        methods=[HTTPMethod.GET, HTTPMethod.POST]
    )
    def get_test(self) -> Any:
        return self.get(parameters={'arg1': True, 'arg2': 123})


@apiclient
class OtherSubClient(SubClient, name='anotherone'):
    @endpoint(
        path='/get?other=',
        href='https://postman-echo.com/get#documentation-link'
    )
    def get_test(self) -> Any:
        return self.get()


def setup(client: Union[SyncClient, AsyncClient]) -> None:
    other = OtherSubClient()

    testing = MySubClient()
    testing.add_subclient(other)

    client.add_subclient(testing)
