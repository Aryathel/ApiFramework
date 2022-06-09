from typing import Any, Union, List, Type

from pydantic import validate_arguments

from .errors import ValidationError


@validate_arguments()
def validate_type(obj: Any, target: Union[Type, List[Type]], err: bool = True) -> bool:
    """Validates that a given parameter is of a type, or is one of a collection of types.

    Parameters
    ----------
    obj: Any
        A variable to validate the type of.
    target: Union[Type, List[Type]]
        A type, or list of types, to check if the :paramref:`.param` is an instance of.
    err: :py:class:`bool`
        Whether or not to throw an error if a type is not validated.

    Returns
    -------
    :py:class:`bool`
        A boolean representing whether the type was validated.
    """
    if isinstance(target, list):
        for t in target:
            if isinstance(obj, t):
                return True
            if type(obj) is t:
                return True
            if issubclass(type(obj), t):
                return True
    else:
        if isinstance(obj, target):
            return True
        if type(obj) is target:
            return True
        if issubclass(type(obj), target):
            return True

    if err:
        raise ValidationError(f"{obj} is not of type {target}.")

    return False
