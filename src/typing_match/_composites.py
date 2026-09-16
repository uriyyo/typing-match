from typing import Any

from typing_inspection.typing_objects import (
    is_concatenate,
    is_literal,
    is_union,
    is_unpack,
)

from ._checks import is_bare_generic_alias, is_generic_alias, is_union_alias
from ._core import Form


class UnionType(Form):
    __args__: tuple[Any, ...]

    __check__ = is_union_alias


class BareUnionType(Form, check=is_union, bare=True): ...


class LiteralType(Form, check=is_literal):
    __args__: tuple[Any, ...]


class BareLiteralType(Form, check=is_literal, bare=True): ...


class GenericType(Form):
    __origin__: Any
    __args__: tuple[Any, ...]

    __check__ = is_generic_alias


class BareGenericType(Form):
    __origin__: Any

    __check__ = is_bare_generic_alias


class ConcatenateType(Form, check=is_concatenate):
    __origin__: Any
    __args__: tuple[Any, ...]


class BareConcatenateType(Form, check=is_concatenate, bare=True): ...


class UnpackType(Form, check=is_unpack):
    __origin__: Any
    __args__: tuple[Any, ...]


class BareUnpackType(Form, check=is_unpack, bare=True): ...


__all__ = [
    "BareConcatenateType",
    "BareGenericType",
    "BareLiteralType",
    "BareUnionType",
    "BareUnpackType",
    "ConcatenateType",
    "GenericType",
    "LiteralType",
    "UnionType",
    "UnpackType",
]
