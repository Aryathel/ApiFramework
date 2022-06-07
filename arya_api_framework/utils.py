from typing import Any, Type

from pydantic import validate_arguments

from .errors import ValidationError


@validate_arguments()
def validate_type(param: Any, target: Type, err: bool = True) -> bool:
    if isinstance(param, target):
        return True
    if type(param) is target:
        return True
    if issubclass(type(param), target):
        return True

    if err:
        raise ValidationError(f"{param} is not of type {target}.")

    return False
