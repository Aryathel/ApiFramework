from typing import Any, Type, Union

from pydantic import validate_arguments

from .errors import ValidationError


@validate_arguments()
def validate_type(param: Any, target: Union[Type, list[Type]], err: bool = True) -> bool:
    if isinstance(target, list):
        for t in target:
            if isinstance(param, t):
                return True
            if type(param) is t:
                return True
            if issubclass(type(param), t):
                return True
    else:
        if isinstance(param, target):
            return True
        if type(param) is target:
            return True
        if issubclass(type(param), target):
            return True

    if err:
        raise ValidationError(f"{param} is not of type {target}.")

    return False
