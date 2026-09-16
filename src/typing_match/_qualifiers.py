from typing import Any

from typing_inspection.typing_objects import (
    is_annotated,
    is_classvar,
    is_final,
    is_notrequired,
    is_readonly,
    is_required,
    is_typeguard,
    is_typeis,
)

from ._checks import is_bare_init_var, is_init_var
from ._core import Form


class AnnotatedType(Form, check=is_annotated):
    __origin__: Any
    __args__: tuple[Any, ...]
    __metadata__: tuple[Any, ...]


class BareAnnotatedType(Form, check=is_annotated, bare=True): ...


class FinalType(Form, check=is_final):
    __origin__: Any
    __args__: tuple[Any, ...]


class BareFinalType(Form, check=is_final, bare=True): ...


class ClassVarType(Form, check=is_classvar):
    __origin__: Any
    __args__: tuple[Any, ...]


class BareClassVarType(Form, check=is_classvar, bare=True): ...


class RequiredType(Form, check=is_required):
    __origin__: Any
    __args__: tuple[Any, ...]


class BareRequiredType(Form, check=is_required, bare=True): ...


class NotRequiredType(Form, check=is_notrequired):
    __origin__: Any
    __args__: tuple[Any, ...]


class BareNotRequiredType(Form, check=is_notrequired, bare=True): ...


class ReadOnlyType(Form, check=is_readonly):
    __origin__: Any
    __args__: tuple[Any, ...]


class BareReadOnlyType(Form, check=is_readonly, bare=True): ...


class TypeGuardType(Form, check=is_typeguard):
    __origin__: Any
    __args__: tuple[Any, ...]


class BareTypeGuardType(Form, check=is_typeguard, bare=True): ...


class TypeIsType(Form, check=is_typeis):
    __origin__: Any
    __args__: tuple[Any, ...]


class BareTypeIsType(Form, check=is_typeis, bare=True): ...


class InitVarType(Form):
    type: Any

    __check__ = is_init_var


class BareInitVarType(Form):
    __check__ = is_bare_init_var


__all__ = [
    "AnnotatedType",
    "BareAnnotatedType",
    "BareClassVarType",
    "BareFinalType",
    "BareInitVarType",
    "BareNotRequiredType",
    "BareReadOnlyType",
    "BareRequiredType",
    "BareTypeGuardType",
    "BareTypeIsType",
    "ClassVarType",
    "FinalType",
    "InitVarType",
    "NotRequiredType",
    "ReadOnlyType",
    "RequiredType",
    "TypeGuardType",
    "TypeIsType",
]
