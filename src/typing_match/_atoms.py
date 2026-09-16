from typing_inspection.typing_objects import (
    is_any,
    is_literalstring,
    is_never,
    is_nodefault,
    is_noreturn,
    is_self,
    is_typealias,
)

from ._checks import is_ellipsis, is_none
from ._core import Form


class AnyType(Form, check=is_any, bare=True): ...


class NeverType(Form, check=is_never, bare=True): ...


class NoReturnType(Form, check=is_noreturn, bare=True): ...


class SelfType(Form, check=is_self, bare=True): ...


class LiteralStringType(Form, check=is_literalstring, bare=True): ...


class TypeAliasType(Form, check=is_typealias, bare=True): ...


class NoDefaultType(Form, check=is_nodefault, bare=True): ...


class NoneType(Form):
    __check__ = is_none


class EllipsisType(Form):
    __check__ = is_ellipsis


__all__ = [
    "AnyType",
    "EllipsisType",
    "LiteralStringType",
    "NeverType",
    "NoDefaultType",
    "NoReturnType",
    "NoneType",
    "SelfType",
    "TypeAliasType",
]
