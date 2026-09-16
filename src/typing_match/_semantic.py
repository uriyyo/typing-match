from typing import Any

from ._checks import (
    is_awaitable_alias,
    is_bare_deprecated_alias,
    is_callable_alias,
    is_deprecated_alias,
    is_iterable_alias,
    is_mapping_alias,
    is_non_str_sequence,
    is_optional,
    is_plain_class,
    is_qualifier,
    is_sequence_alias,
    is_set_alias,
    is_tuple_alias,
    is_type_alias,
)
from ._core import Form


class OptionalType(Form):
    __args__: tuple[Any, ...]

    __check__ = is_optional


class CallableType(Form):
    __origin__: Any
    __args__: tuple[Any, ...]

    __check__ = is_callable_alias


class TupleType(Form):
    __origin__: Any
    __args__: tuple[Any, ...]

    __check__ = is_tuple_alias


class SequenceType(Form):
    __origin__: Any
    __args__: tuple[Any, ...]

    __check__ = is_sequence_alias


class MappingType(Form):
    __origin__: Any
    __args__: tuple[Any, ...]

    __check__ = is_mapping_alias


class SetType(Form):
    __origin__: Any
    __args__: tuple[Any, ...]

    __check__ = is_set_alias


class NonStrSequenceType(Form):
    __check__ = is_non_str_sequence


class IterableType(Form):
    __origin__: Any
    __args__: tuple[Any, ...]

    __check__ = is_iterable_alias


class AwaitableType(Form):
    __origin__: Any
    __args__: tuple[Any, ...]

    __check__ = is_awaitable_alias


class TypeType(Form):
    __origin__: Any
    __args__: tuple[Any, ...]

    __check__ = is_type_alias


class DeprecatedAliasType(Form):
    __origin__: Any
    __args__: tuple[Any, ...]

    __check__ = is_deprecated_alias


class BareDeprecatedAliasType(Form):
    __origin__: Any

    __check__ = is_bare_deprecated_alias


class PlainType(Form):
    __name__: str

    __check__ = is_plain_class


class QualifierType(Form):
    __origin__: Any
    __args__: tuple[Any, ...]

    __check__ = is_qualifier


__all__ = [
    "AwaitableType",
    "BareDeprecatedAliasType",
    "CallableType",
    "DeprecatedAliasType",
    "IterableType",
    "MappingType",
    "NonStrSequenceType",
    "OptionalType",
    "PlainType",
    "QualifierType",
    "SequenceType",
    "SetType",
    "TupleType",
    "TypeType",
]
