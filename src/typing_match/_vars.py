from typing import Any

from typing_inspection.typing_objects import (
    is_paramspec,
    is_paramspecargs,
    is_paramspeckwargs,
    is_typevartuple,
)

from ._checks import is_typevar
from ._core import Form


class TypeVarType(Form):
    __name__: str
    __bound__: Any
    __constraints__: tuple[Any, ...]
    __covariant__: bool
    __contravariant__: bool
    __default__: Any

    __check__ = is_typevar


class ParamSpecType(Form, check=is_paramspec, bare=True):
    __name__: str
    __bound__: Any
    __covariant__: bool
    __contravariant__: bool
    __default__: Any


class TypeVarTupleType(Form, check=is_typevartuple, bare=True):
    __name__: str
    __default__: Any


class ParamSpecArgsType(Form, check=is_paramspecargs, bare=True):
    __origin__: Any


class ParamSpecKwargsType(Form, check=is_paramspeckwargs, bare=True):
    __origin__: Any


__all__ = [
    "ParamSpecArgsType",
    "ParamSpecKwargsType",
    "ParamSpecType",
    "TypeVarTupleType",
    "TypeVarType",
]
