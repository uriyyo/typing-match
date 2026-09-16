from collections.abc import Awaitable as _Awaitable
from collections.abc import Callable as _Callable
from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from collections.abc import Sequence as _Sequence
from collections.abc import Set as _AbstractSet  # noqa: PYI025
from dataclasses import InitVar
from types import EllipsisType
from typing import Any, TypeVar, get_args, get_origin

from typing_extensions import Sentinel, TypeIs
from typing_inspection.introspection import is_union_origin
from typing_inspection.typing_objects import (
    DEPRECATED_ALIASES,
    NoneType,
    is_annotated,
    is_classvar,
    is_final,
    is_notrequired,
    is_readonly,
    is_required,
    is_typevartuple,
)
from typing_inspection.typing_objects import is_typevar as _is_typevar


def is_union_alias(obj: Any, /) -> bool:
    return is_union_origin(get_origin(obj))


def is_generic_alias(obj: Any, /) -> bool:
    origin = get_origin(obj)

    return (
        isinstance(origin, type)
        and hasattr(obj, "__args__")
        and not is_annotated(origin)
        and not is_union_alias(obj)
    )


def is_bare_generic_alias(obj: Any, /) -> bool:
    return isinstance(get_origin(obj), type) and not hasattr(obj, "__args__")


_QUALIFIERS = (is_final, is_classvar, is_required, is_notrequired, is_readonly)


def is_qualifier(obj: Any, /) -> bool:
    origin = get_origin(obj)

    return any(check(origin) for check in _QUALIFIERS) or is_init_var(obj)


def is_init_var(obj: Any, /) -> bool:
    return isinstance(obj, InitVar)


def is_bare_init_var(obj: Any, /) -> bool:
    return obj is InitVar


def is_none(obj: Any, /) -> bool:
    return obj is None or obj is NoneType


def is_ellipsis(obj: Any, /) -> bool:
    return obj is Ellipsis or obj is EllipsisType


def is_typevar(obj: Any, /) -> TypeIs[TypeVar]:
    return _is_typevar(obj) and get_origin(obj) is None and not is_typevartuple(obj)


def is_optional(obj: Any, /) -> bool:
    return is_union_alias(obj) and NoneType in get_args(obj)


def is_callable_alias(obj: Any, /) -> bool:
    return is_generic_alias(obj) and get_origin(obj) is _Callable


def is_tuple_alias(obj: Any, /) -> bool:
    return is_generic_alias(obj) and get_origin(obj) is tuple


def is_sequence_alias(obj: Any, /) -> bool:
    return is_generic_alias(obj) and issubclass(get_origin(obj), _Sequence)


_ATOMIC_SEQUENCES = (str, bytes, bytearray, memoryview)


def is_non_str_sequence(obj: Any, /) -> bool:
    cls = obj if is_plain_class(obj) else get_origin(obj)

    return (
        isinstance(cls, type)
        and issubclass(cls, _Sequence)
        and not issubclass(cls, _ATOMIC_SEQUENCES)
    )


def is_mapping_alias(obj: Any, /) -> bool:
    return is_generic_alias(obj) and issubclass(get_origin(obj), _Mapping)


def is_set_alias(obj: Any, /) -> bool:
    return is_generic_alias(obj) and issubclass(get_origin(obj), _AbstractSet)


def is_iterable_alias(obj: Any, /) -> bool:
    return is_generic_alias(obj) and issubclass(get_origin(obj), _Iterable)


def is_awaitable_alias(obj: Any, /) -> bool:
    return is_generic_alias(obj) and issubclass(get_origin(obj), _Awaitable)


def is_type_alias(obj: Any, /) -> bool:
    return is_generic_alias(obj) and get_origin(obj) is type


_DEPRECATED_ORIGINS = set(DEPRECATED_ALIASES.values())


def is_deprecated_alias(obj: Any, /) -> bool:
    return (
        is_generic_alias(obj)
        and get_origin(obj) in _DEPRECATED_ORIGINS
        and getattr(obj, "__module__", None) in ("typing", "typing_extensions")
    )


def is_bare_deprecated_alias(obj: Any, /) -> bool:
    try:
        return obj in DEPRECATED_ALIASES
    except TypeError:
        return False


def is_plain_class(obj: Any, /) -> TypeIs[type]:
    return isinstance(obj, type) and get_origin(obj) is None and not is_annotated(obj)


def is_sentinel(obj: Any, /) -> TypeIs[Sentinel]:
    return isinstance(obj, Sentinel)


__all__ = [
    "is_awaitable_alias",
    "is_bare_deprecated_alias",
    "is_bare_generic_alias",
    "is_bare_init_var",
    "is_callable_alias",
    "is_deprecated_alias",
    "is_ellipsis",
    "is_generic_alias",
    "is_init_var",
    "is_iterable_alias",
    "is_mapping_alias",
    "is_non_str_sequence",
    "is_none",
    "is_optional",
    "is_plain_class",
    "is_qualifier",
    "is_sentinel",
    "is_sequence_alias",
    "is_set_alias",
    "is_tuple_alias",
    "is_type_alias",
    "is_typevar",
    "is_union_alias",
]
