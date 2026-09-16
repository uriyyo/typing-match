import collections.abc
import dataclasses
import typing as ty

import typing_extensions as te

T = te.TypeVar("T")
P = te.ParamSpec("P")
Ts = te.TypeVarTuple("Ts")

TD = te.TypedDict("TD", {"a": int})
NT = ty.NamedTuple("NT", [("a", int)])
TAT = te.TypeAliasType("TAT", int)
UserId = te.NewType("UserId", int)


class Proto(te.Protocol):
    def method(self) -> int: ...


SAMPLES: dict[str, object] = {
    "Annotated[int, 1]": ty.Annotated[int, 1],
    "Annotated": ty.Annotated,
    "Final[int]": ty.Final[int],
    "Final": ty.Final,
    "ClassVar[int]": ty.ClassVar[int],
    "ClassVar": ty.ClassVar,
    "Required[int]": te.Required[int],
    "Required": te.Required,
    "NotRequired[int]": te.NotRequired[int],
    "NotRequired": te.NotRequired,
    "ReadOnly[int]": te.ReadOnly[int],
    "ReadOnly": te.ReadOnly,
    "TypeGuard[int]": te.TypeGuard[int],
    "TypeGuard": te.TypeGuard,
    "TypeIs[int]": te.TypeIs[int],
    "TypeIs": te.TypeIs,
    "InitVar[int]": dataclasses.InitVar[int],
    "InitVar": dataclasses.InitVar,
    "Union[int, str]": ty.Union[int, str],
    "int | str": int | str,
    "Union": ty.Union,
    "Optional[int]": ty.Optional[int],
    "int | None": int | None,
    "Literal[1]": ty.Literal[1],
    "Literal": ty.Literal,
    "list[int]": list[int],
    "List[int]": ty.List[int],
    "List": ty.List,
    "dict[str, int]": dict[str, int],
    "tuple[int, ...]": tuple[int, ...],
    "type[int]": type[int],
    "Type[int]": ty.Type[int],
    "Callable[[int], str]": ty.Callable[[int], str],
    "Callable": ty.Callable,
    "Concatenate[int, P]": te.Concatenate[int, P],
    "Concatenate": te.Concatenate,
    "Unpack[Ts]": te.Unpack[Ts],
    "Unpack": te.Unpack,
    "Sequence[int]": collections.abc.Sequence[int],
    "Mapping[str, int]": collections.abc.Mapping[str, int],
    "Set[int]": collections.abc.Set[int],
    "Iterable[int]": collections.abc.Iterable[int],
    "Awaitable[int]": collections.abc.Awaitable[int],
    "Any": ty.Any,
    "te.Any": te.Any,
    "Never": te.Never,
    "NoReturn": ty.NoReturn,
    "Self": te.Self,
    "LiteralString": te.LiteralString,
    "TypeAlias": ty.TypeAlias,
    "NoDefault": te.NoDefault,
    "None": None,
    "NoneType": type(None),
    "...": ...,
    "T": T,
    "P": P,
    "Ts": Ts,
    "P.args": P.args,
    "P.kwargs": P.kwargs,
    "deprecated('msg')": te.deprecated("msg"),
    "NoExtraItems": te.NoExtraItems,
    "Sentinel": te.Sentinel("MISSING"),
    "Protocol class": Proto,
    "NewType": UserId,
    "TypeAliasType": TAT,
    "ForwardRef": ty.ForwardRef("X"),
    "TypedDict": TD,
    "NamedTuple": NT,
    "int": int,
    "object": object,
    "str": str,
    "list": list,
}
