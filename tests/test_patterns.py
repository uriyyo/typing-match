import dataclasses
import typing as ty

import pytest
import typing_extensions as te

from typing_match import (
    AliasType,
    AnnotatedType,
    AnyType,
    AwaitableType,
    BareAnnotatedType,
    BareDeprecatedAliasType,
    BareGenericType,
    CallableType,
    ClassVarType,
    DeprecatedAliasType,
    DeprecatedType,
    EllipsisType,
    FinalType,
    Form,
    ForwardRefType,
    GenericType,
    InitVarType,
    LiteralType,
    MappingType,
    NamedTupleType,
    NewTypeType,
    NoneType,
    NonStrSequenceType,
    OptionalType,
    ParamSpecArgsType,
    PlainType,
    ProtocolType,
    QualifierType,
    SentinelType,
    SequenceType,
    TupleType,
    TypedDictType,
    TypeType,
    TypeVarType,
    UnionType,
    UnpackType,
    alias,
)

P = te.ParamSpec("P")
Ts = te.TypeVarTuple("Ts")


def test_keyword_pattern() -> None:
    match ty.Annotated[int, "meta"]:
        case AnnotatedType(__origin__=alias.int, __metadata__=("meta",)):
            pass
        case _:
            pytest.fail("expected an AnnotatedType")


def test_positional_pattern_follows_match_args() -> None:
    assert AnnotatedType.__match_args__ == ("__origin__", "__args__", "__metadata__")

    match ty.Annotated[int, "meta"]:
        case AnnotatedType(origin, _, [meta]):
            assert origin is int
            assert meta == "meta"
        case _:
            pytest.fail("expected an AnnotatedType")


def test_bare_form() -> None:
    match ty.Annotated:
        case AnnotatedType():
            pytest.fail("the bare form must not match the subscripted matcher")
        case BareAnnotatedType():
            pass
        case _:
            pytest.fail("expected a BareAnnotatedType")


def test_capture_and_recurse() -> None:
    match ty.Annotated[ty.Optional[list[int]], "meta"]:
        case AnnotatedType(
            __origin__=OptionalType(__args__=[GenericType(alias.list, [arg]), _]),
        ):
            assert arg is int
        case _:
            pytest.fail("expected a nested Optional[list[int]]")


@pytest.mark.parametrize("union", [ty.Union[int, str], int | str])
def test_both_union_spellings(union: object) -> None:
    match union:
        case UnionType([*args]):
            assert args == [int, str]
        case _:
            pytest.fail("expected a UnionType")


def test_callable_args_are_flat() -> None:
    match ty.Callable[[int, str], bool]:
        case CallableType(__args__=[*params, ret]):
            assert params == [int, str]
            assert ret is bool
        case _:
            pytest.fail("expected a CallableType")


def test_callable_with_ellipsis() -> None:
    match ty.Callable[..., bool]:
        case CallableType(__args__=[EllipsisType(), ret]):
            assert ret is bool
        case _:
            pytest.fail("expected a CallableType taking any arguments")


def test_alternation() -> None:
    for tp in (ty.Final[int], ty.ClassVar[int]):
        match tp:
            case FinalType(__args__=[arg]) | ClassVarType(__args__=[arg]):
                assert arg is int
            case _:
                pytest.fail("expected a qualifier")


def test_semantic_matcher_overlaps_the_one_to_one_matcher() -> None:
    match ty.Final[int]:
        case QualifierType(__args__=[arg]):
            assert arg is int
        case _:
            pytest.fail("expected a QualifierType")


def test_guard() -> None:
    match ty.Literal["a", "b"]:
        case LiteralType([*values]) if all(isinstance(v, str) for v in values):
            assert values == ["a", "b"]
        case _:
            pytest.fail("expected a string LiteralType")


def test_tuple_of_unknown_length() -> None:
    match tuple[int, ...]:
        case TupleType(__args__=[item, EllipsisType()]):
            assert item is int
        case _:
            pytest.fail("expected a homogeneous TupleType")


def test_optional_strips_none() -> None:
    match ty.Optional[int]:
        case OptionalType(__args__=[inner, NoneType()]):
            assert inner is int
        case _:
            pytest.fail("expected an OptionalType")


def test_bare_generic_exposes_its_origin() -> None:
    match ty.List:
        case BareGenericType(origin):
            assert origin is list
        case _:
            pytest.fail("expected a BareGenericType")


def test_type_var() -> None:
    T = te.TypeVar("T", bound=int, covariant=True)

    match T:
        case TypeVarType(__name__="T", __bound__=alias.int, __covariant__=True):
            pass
        case _:
            pytest.fail("expected a TypeVarType")


def test_param_spec_args_point_back_at_the_param_spec() -> None:
    match P.args:
        case ParamSpecArgsType(origin):
            assert origin is P
        case _:
            pytest.fail("expected a ParamSpecArgsType")


def test_unpack() -> None:
    match te.Unpack[Ts]:
        case UnpackType(__args__=[Ts_]):
            assert Ts_ is Ts
        case _:
            pytest.fail("expected an UnpackType")


def test_new_type() -> None:
    UserId = te.NewType("UserId", int)

    match UserId:
        case NewTypeType(name, supertype):
            assert name == "UserId"
            assert supertype is int
        case _:
            pytest.fail("expected a NewTypeType")


def test_type_alias_type() -> None:
    Alias = te.TypeAliasType("Alias", list[int])

    match Alias:
        case AliasType(
            __name__="Alias",
            __value__=GenericType(alias.list, [alias.int]),
        ):
            pass
        case _:
            pytest.fail("expected an AliasType")


def test_forward_ref() -> None:
    match ty.ForwardRef("Model"):
        case ForwardRefType("Model"):
            pass
        case _:
            pytest.fail("expected a ForwardRefType")


def test_init_var() -> None:
    match dataclasses.InitVar[int]:
        case InitVarType(alias.int):
            pass
        case _:
            pytest.fail("expected an InitVarType")


def test_typed_dict() -> None:
    TD = te.TypedDict("TD", {"a": int, "b": te.NotRequired[str]})

    match TD:
        case TypedDictType(
            __annotations__={"a": alias.int},
            __required_keys__=required,
        ):
            assert required == frozenset({"a"})
        case _:
            pytest.fail("expected a TypedDictType")


def test_named_tuple() -> None:
    NT = ty.NamedTuple("NT", [("a", int)])

    match NT:
        case NamedTupleType(("a",), {"a": alias.int}):
            pass
        case _:
            pytest.fail("expected a NamedTupleType")


def test_dispatch_over_a_whole_annotation() -> None:
    def describe(tp: object) -> str:
        match tp:
            case AnnotatedType(__origin__=inner, __metadata__=[*meta]):
                return f"{describe(inner)} annotated with {meta}"
            case OptionalType(__args__=[inner, NoneType()]):
                return f"optional {describe(inner)}"
            case UnionType([*args]):
                return " or ".join(describe(arg) for arg in args)
            case CallableType(__args__=[*params, ret]):
                params_ = ", ".join(describe(p) for p in params)
                return f"({params_}) -> {describe(ret)}"
            case GenericType(origin, [*args]):
                return f"{origin.__name__} of {', '.join(describe(a) for a in args)}"
            case LiteralType([*values]):
                return f"one of {values}"
            case AnyType():
                return "anything"
            case NoneType():
                return "none"
            case PlainType(name):
                return name
            case _:
                return "?"

    assert describe(ty.Annotated[ty.Optional[int], "meta"]) == (
        "optional int annotated with ['meta']"
    )
    assert describe(dict[str, list[int]]) == "dict of str, list of int"
    assert describe(ty.Callable[[int], ty.Any]) == "(int) -> anything"
    assert describe(ty.Union[int, str, None]) == "int or str or none"
    assert describe(ty.Literal[1, 2]) == "one of [1, 2]"


def test_or_pattern_binding_one_name_strips_annotated() -> None:
    def strip(tp: object) -> object:
        match tp:
            case AnnotatedType(__origin__=inner) | inner:
                return inner

    assert strip(ty.Annotated[int, "meta"]) is int
    assert strip(int) is int
    assert strip(list[int]) == list[int]


def test_predicate_object_as_a_value_pattern() -> None:
    class Contains:
        def __init__(self, needle: object) -> None:
            self.needle = needle

        def __eq__(self, other: object) -> bool:
            return isinstance(other, tuple) and self.needle in other

        __hash__ = None  # type: ignore[assignment]

    class pred:
        admits_str = Contains(str)

    def describe(tp: object) -> str:
        match tp:
            case UnionType(__args__=pred.admits_str):
                return "union admitting str"
            case UnionType():
                return "other union"
            case _:
                return "not a union"

    assert describe(ty.Union[int, str]) == "union admitting str"
    assert describe(ty.Union[int, bytes]) == "other union"
    assert describe(int) == "not a union"


def test_parameterized_matcher_via_value_pattern() -> None:
    class ListOf:
        def __init__(self, item: object) -> None:
            self.item = item

        def __eq__(self, other: object) -> bool:
            return ty.get_origin(other) is list and ty.get_args(other) == (self.item,)

        __hash__ = None  # type: ignore[assignment]

    class pat:
        list_of_int = ListOf(int)

    match list[int]:
        case pat.list_of_int:
            pass
        case _:
            pytest.fail("expected list[int]")

    match dict[str, list[int]]:
        case GenericType(alias.dict, [alias.str, pat.list_of_int]):
            pass
        case _:
            pytest.fail("expected dict[str, list[int]]")

    match dict[str, list[str]]:
        case GenericType(alias.dict, [alias.str, pat.list_of_int]):
            pytest.fail("list[str] is not list[int]")
        case _:
            pass


def test_keyword_pattern_reads_undeclared_attributes() -> None:
    assert "__parameters__" not in FinalType.__match_args__

    match ty.Final[int]:
        case FinalType(__parameters__=()):
            pass
        case _:
            pytest.fail("expected an unparameterized Final")


def test_mapping_pattern_captures_the_rest() -> None:
    TD = te.TypedDict("TD", {"a": int, "b": str, "c": bytes})

    match TD:
        case TypedDictType(__annotations__={"a": alias.int, **rest}):
            assert sorted(rest) == ["b", "c"]
        case _:
            pytest.fail("expected a TypedDictType")


def _list_of(item: object) -> type:
    def check(obj: object) -> bool:
        return ty.get_origin(obj) is list and ty.get_args(obj) == (item,)

    cls = type(f"list[{getattr(item, '__name__', item)}]", (Form,), {})
    cls.__check__ = check

    return cls


def test_parameterized_matcher_via_form_subclass() -> None:
    list_of_int = _list_of(int)

    match list[int]:
        case list_of_int():
            pass
        case _:
            pytest.fail("expected list[int]")

    match dict[str, list[int]]:
        case GenericType(alias.dict, [alias.str, list_of_int()]):
            pass
        case _:
            pytest.fail("expected dict[str, list[int]]")

    match list[str]:
        case list_of_int():
            pytest.fail("list[str] is not list[int]")
        case _:
            pass


def test_form_subclass_is_immune_to_a_hostile_eq() -> None:
    class Hostile:
        def __eq__(self, other: object) -> bool:
            return False

        __hash__ = None  # type: ignore[assignment]

    class pat:
        never_equal = Hostile()

    anything = type("anything", (Form,), {})
    anything.__check__ = lambda obj: True

    subject = ty.Annotated[int, Hostile()]

    match subject:
        case AnnotatedType(__metadata__=[pat.never_equal]):
            pytest.fail("a hostile __eq__ must swallow the value pattern")
        case AnnotatedType(__metadata__=[anything()]):
            pass
        case _:
            pytest.fail("expected the class pattern to match")


def test_deprecated_inside_annotated_metadata() -> None:
    match ty.Annotated[int, te.deprecated("use Y instead")]:
        case AnnotatedType(__metadata__=[DeprecatedType(message=msg)]):
            assert msg == "use Y instead"
        case _:
            pytest.fail("expected a DeprecatedType in the metadata")


def test_deprecated_alias_spelling() -> None:
    match ty.List[int]:
        case DeprecatedAliasType(origin, [arg]):
            assert origin is list
            assert arg is int
        case _:
            pytest.fail("expected a DeprecatedAliasType")

    match list[int]:
        case DeprecatedAliasType():
            pytest.fail("the modern spelling must not match")
        case GenericType():
            pass
        case _:
            pytest.fail("expected a GenericType")


def test_bare_deprecated_alias_spelling() -> None:
    match ty.List:
        case BareDeprecatedAliasType(origin):
            assert origin is list
        case _:
            pytest.fail("expected a BareDeprecatedAliasType")

    match list:
        case BareDeprecatedAliasType():
            pytest.fail("the runtime class must not match")
        case PlainType():
            pass
        case _:
            pytest.fail("expected a PlainType")


def test_subscripted_type() -> None:
    match type[int]:
        case TypeType(_, [arg]):
            assert arg is int
        case _:
            pytest.fail("expected a TypeType")

    match type:
        case TypeType():
            pytest.fail("bare type must stay a PlainType")
        case PlainType():
            pass
        case _:
            pytest.fail("expected a PlainType")


def test_protocol() -> None:
    class Readable(te.Protocol):
        def read(self) -> bytes: ...

    @te.runtime_checkable
    class Closeable(te.Protocol):
        def close(self) -> None: ...

    match Readable:
        case ProtocolType(name):
            assert name == "Readable"
        case _:
            pytest.fail("expected a ProtocolType")

    match Readable:
        case ProtocolType(_is_runtime_protocol=True):
            pytest.fail("Readable is not runtime-checkable")
        case ProtocolType():
            pass
        case _:
            pytest.fail("expected a ProtocolType")

    match Closeable:
        case ProtocolType(_is_runtime_protocol=True):
            pass
        case _:
            pytest.fail("expected a runtime-checkable ProtocolType")


def test_sentinel() -> None:
    MISSING = te.Sentinel("MISSING")

    match MISSING:
        case SentinelType(_name=name):
            assert name == "MISSING"
        case _:
            pytest.fail("expected a SentinelType")


def test_capability_matchers_are_used_inline() -> None:
    import collections.abc

    match dict[str, list[int]]:
        case MappingType(_, [key, SequenceType(_, [item])]):
            assert key is str
            assert item is int
        case _:
            pytest.fail("expected a mapping of sequences")

    match collections.abc.Mapping[str, int]:
        case MappingType(origin, [_, value]):
            assert origin is collections.abc.Mapping
            assert value is int
        case _:
            pytest.fail("expected a MappingType")

    match collections.abc.Coroutine[ty.Any, ty.Any, int]:
        case AwaitableType(__args__=[*_, result]):
            assert result is int
        case _:
            pytest.fail("expected an AwaitableType")


def test_non_str_sequence() -> None:
    import collections.abc

    for tp in (list[int], ty.List[int], ty.List, list, collections.abc.Sequence[int]):
        match tp:
            case NonStrSequenceType():
                pass
            case _:
                pytest.fail(f"expected {tp!r} to be a non-str sequence")

    for tp in (str, bytes, bytearray, str | None, dict[str, int], int):
        match tp:
            case NonStrSequenceType():
                pytest.fail(f"{tp!r} must not count as a non-str sequence")
            case _:
                pass

    match ty.Sequence[int]:
        case NonStrSequenceType(__args__=[item]):
            assert item is int
        case _:
            pytest.fail("expected a subscripted non-str sequence")
