import pytest
from samples import SAMPLES

import typing_match as tm

MATCHERS = [
    name for name in tm.__all__ if name not in ("Form", "FormMeta", "alias", "pat")
]

EXPECTED: dict[str, list[str]] = {
    "Annotated[int, 1]": ["AnnotatedType"],
    "Annotated": ["BareAnnotatedType"],
    "Final[int]": ["FinalType", "QualifierType"],
    "Final": ["BareFinalType"],
    "ClassVar[int]": ["ClassVarType", "QualifierType"],
    "ClassVar": ["BareClassVarType"],
    "Required[int]": ["QualifierType", "RequiredType"],
    "Required": ["BareRequiredType"],
    "NotRequired[int]": ["NotRequiredType", "QualifierType"],
    "NotRequired": ["BareNotRequiredType"],
    "ReadOnly[int]": ["QualifierType", "ReadOnlyType"],
    "ReadOnly": ["BareReadOnlyType"],
    "TypeGuard[int]": ["TypeGuardType"],
    "TypeGuard": ["BareTypeGuardType"],
    "TypeIs[int]": ["TypeIsType"],
    "TypeIs": ["BareTypeIsType"],
    "InitVar[int]": ["InitVarType", "QualifierType"],
    "InitVar": ["BareInitVarType", "PlainType"],
    "Union[int, str]": ["UnionType"],
    "int | str": ["UnionType"],
    "Union": ["BareUnionType"],
    "Optional[int]": ["OptionalType", "UnionType"],
    "int | None": ["OptionalType", "UnionType"],
    "Literal[1]": ["LiteralType"],
    "Literal": ["BareLiteralType"],
    "list[int]": ["GenericType", "IterableType", "NonStrSequenceType", "SequenceType"],
    "List[int]": [
        "DeprecatedAliasType",
        "GenericType",
        "IterableType",
        "NonStrSequenceType",
        "SequenceType",
    ],
    "List": ["BareDeprecatedAliasType", "BareGenericType", "NonStrSequenceType"],
    "dict[str, int]": ["GenericType", "IterableType", "MappingType"],
    "tuple[int, ...]": [
        "GenericType",
        "IterableType",
        "NonStrSequenceType",
        "SequenceType",
        "TupleType",
    ],
    "type[int]": ["GenericType", "TypeType"],
    "Type[int]": ["DeprecatedAliasType", "GenericType", "TypeType"],
    "Callable[[int], str]": ["CallableType", "DeprecatedAliasType", "GenericType"],
    "Callable": ["BareDeprecatedAliasType", "BareGenericType"],
    "Concatenate[int, P]": ["ConcatenateType"],
    "Concatenate": ["BareConcatenateType"],
    "Unpack[Ts]": ["UnpackType"],
    "Unpack": ["BareUnpackType"],
    "Sequence[int]": [
        "GenericType",
        "IterableType",
        "NonStrSequenceType",
        "SequenceType",
    ],
    "Mapping[str, int]": ["GenericType", "IterableType", "MappingType"],
    "Set[int]": ["GenericType", "IterableType", "SetType"],
    "Iterable[int]": ["GenericType", "IterableType"],
    "Awaitable[int]": ["AwaitableType", "GenericType"],
    "Any": ["AnyType"],
    "Never": ["NeverType"],
    "NoReturn": ["NoReturnType"],
    "Self": ["SelfType"],
    "LiteralString": ["LiteralStringType"],
    "TypeAlias": ["TypeAliasType"],
    "NoDefault": ["NoDefaultType"],
    "None": ["NoneType"],
    "NoneType": ["NoneType", "PlainType"],
    "...": ["EllipsisType"],
    "T": ["TypeVarType"],
    "P": ["ParamSpecType"],
    "Ts": ["TypeVarTupleType"],
    "P.args": ["ParamSpecArgsType"],
    "P.kwargs": ["ParamSpecKwargsType"],
    "deprecated('msg')": ["DeprecatedType"],
    "NoExtraItems": ["NoExtraItemsType"],
    "Sentinel": ["SentinelType"],
    "Protocol class": ["PlainType", "ProtocolType"],
    "NewType": ["NewTypeType"],
    "TypeAliasType": ["AliasType"],
    "ForwardRef": ["ForwardRefType"],
    "TypedDict": ["PlainType", "TypedDictType"],
    "NamedTuple": ["NamedTupleType", "NonStrSequenceType", "PlainType"],
    "int": ["PlainType"],
    "object": ["PlainType"],
    "str": ["PlainType"],
    "list": ["NonStrSequenceType", "PlainType"],
}


@pytest.mark.parametrize("label", SAMPLES)
def test_matches_exactly_expected_matchers(label: str) -> None:
    sample = SAMPLES[label]
    matched = [name for name in MATCHERS if isinstance(sample, getattr(tm, name))]

    assert matched == sorted(EXPECTED[label])


def test_every_sample_is_covered() -> None:
    assert SAMPLES.keys() == EXPECTED.keys()


def test_every_matcher_has_a_positive_case() -> None:
    covered = {name for names in EXPECTED.values() for name in names}

    assert covered == set(MATCHERS)
