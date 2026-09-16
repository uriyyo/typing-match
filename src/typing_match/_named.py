from typing import Any

from typing_extensions import is_protocol, is_typeddict
from typing_inspection.typing_objects import (
    is_forwardref,
    is_namedtuple,
    is_newtype,
    is_typealiastype,
)

from ._core import Form


class NewTypeType(Form, check=is_newtype, bare=True):
    __name__: str
    __supertype__: Any


class AliasType(Form, check=is_typealiastype, bare=True):
    __name__: str
    __value__: Any
    __type_params__: tuple[Any, ...]


class ForwardRefType(Form, check=is_forwardref, bare=True):
    __forward_arg__: str


class ProtocolType(Form, check=is_protocol, bare=True):
    __name__: str


class TypedDictType(Form, check=is_typeddict, bare=True):
    __annotations__: dict[str, Any]
    __required_keys__: frozenset[str]
    __optional_keys__: frozenset[str]
    __total__: bool


class NamedTupleType(Form, check=is_namedtuple, bare=True):
    _fields: tuple[str, ...]
    __annotations__: dict[str, Any]


__all__ = [
    "AliasType",
    "ForwardRefType",
    "NamedTupleType",
    "NewTypeType",
    "ProtocolType",
    "TypedDictType",
]
