# typing-match

Destructure typing objects with the `match` statement.

```python
from typing import Annotated, Optional
from typing_match import AnnotatedType, GenericType, OptionalType, alias

match Annotated[Optional[list[int]], "meta"]:
    case AnnotatedType(
        __origin__=OptionalType(__args__=[GenericType(alias.list, [item]), _]),
        __metadata__=[*meta],
    ):
        print(item, meta)  # <class 'int'> ['meta']
```

No wrapping, no parsing step: the subject of the `match` is the real typing
object, and the matchers read its real attributes.

Requires Python >= 3.10 and typing-extensions >= 4.14.

## How it works

A class pattern does exactly two things -- an `isinstance()` check, then a
`getattr()` per sub-pattern. So a class that is never instantiated, whose
metaclass redefines `__instancecheck__`, is enough to turn any typing form into
a pattern:

```python
class AnnotatedType(Form, check=is_annotated):
    __origin__: Any
    __args__: tuple[Any, ...]
    __metadata__: tuple[Any, ...]
```

The annotations name the attributes to read off the matched object and become
`__match_args__`, so positional patterns work too:

```python
case AnnotatedType(origin, _, [meta]): ...
```

Detection comes from [typing-inspection], so the `typing` and
`typing_extensions` spellings of a form are both recognized, on every supported
Python.

## Matchers

`XType` matches the subscripted form, `BareXType` the unsubscripted one.

| Group           | Matchers                                                                                                                              |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Qualifiers      | `AnnotatedType`, `FinalType`, `ClassVarType`, `RequiredType`, `NotRequiredType`, `ReadOnlyType`, `InitVarType`                        |
| Narrowing       | `TypeGuardType`, `TypeIsType`                                                                                                         |
| Composites      | `UnionType`, `LiteralType`, `GenericType`, `ConcatenateType`, `UnpackType`                                                            |
| Atoms           | `AnyType`, `NeverType`, `NoReturnType`, `SelfType`, `LiteralStringType`, `TypeAliasType`, `NoDefaultType`, `NoneType`, `EllipsisType` |
| Type parameters | `TypeVarType`, `ParamSpecType`, `TypeVarTupleType`, `ParamSpecArgsType`, `ParamSpecKwargsType`                                        |
| Named entities  | `NewTypeType`, `AliasType`, `ForwardRefType`, `TypedDictType`, `NamedTupleType`, `ProtocolType`                                       |
| Semantic        | `OptionalType`, `CallableType`, `TupleType`, `TypeType`, `PlainType`, `QualifierType`, `DeprecatedAliasType`                          |
| Capabilities    | `SequenceType`, `MappingType`, `SetType`, `IterableType`, `AwaitableType`, `NonStrSequenceType`                                       |
| Extensions      | `DeprecatedType`, `NoExtraItemsType`, `SentinelType`                                                                                  |

The semantic matchers deliberately overlap the one-to-one ones: an
`Optional[int]` is also a `UnionType`, a `Callable[[int], str]` and a
`type[int]` are also `GenericType`s, a `Protocol` class is also a `PlainType`.
Order your `case` clauses accordingly. `QualifierType` covers exactly the
members of [typing-inspection]'s `Qualifier`, `InitVar` included.

`DeprecatedAliasType` (with its `Bare` twin) singles out the legacy spelling:
`List[int]` matches it, `list[int]` does not, although both are `GenericType` --
which is exactly the distinction annotation-modernizing code needs.

The capability matchers classify by what the origin *is a subclass of* rather
than what it is, so one `case` covers a whole family of aliases -- directly in
the pattern, nothing to prepare outside the `match`:

```python
match tp:
    case MappingType(_, [key, value]):
        ...  # dict[str, int], Mapping[str, int], OrderedDict[str, int], ...
    case SequenceType(_, [item]):
        ...  # list[int], Sequence[int], ...
    case AwaitableType(__args__=[*_, result]):
        ...  # Awaitable[int], Coroutine[Any, Any, int]
```

Every sequence, mapping and set alias is also an `IterableType`, so put the
narrower capability first.

`NonStrSequenceType` handles the classic `str`-is-a-`Sequence` trap. It admits
every spelling of a sequence -- `list[int]`, bare `List`, plain `list` -- while
refusing the atomic ones (`str`, `bytes`, `bytearray`, `memoryview`):

```python
match tp:
    case NonStrSequenceType():
        ...  # matches list, list[int], Sequence[str] -- never str itself
```

Because the spellings carry different attributes, it declares none; use
keyword patterns (`NonStrSequenceType(__args__=[item])`), which simply fail to
match on the spellings that lack the attribute.

The extensions group matches runtime companions of annotations rather than
typing forms: `DeprecatedType` destructures a `warnings.deprecated` /
`typing_extensions.deprecated` instance (`message`, `category`, `stacklevel`),
typically found inside `Annotated` metadata; `SentinelType` matches a PEP 661
`Sentinel`; `NoExtraItemsType` the PEP 728 sentinel.

## `alias`: bare names capture, dotted names compare

In a `match` statement a bare name is a _capture pattern_. `case
GenericType(list, [int])` matches every generic alias and rebinds `list` and
`int` as locals -- almost never what you want. Only a dotted name is compared,
which is what `typing_match.alias` is for:

```python
from typing_match import GenericType, alias

match dict[str, list[int]]:
    case GenericType(alias.dict, [alias.str, GenericType(alias.list, [item])]):
        ...
```

It carries the builtins, `collections`, `collections.abc`, `types`, `re`,
`pathlib`, `datetime`, `enum`, `io`, `ipaddress`, `numbers`, `zoneinfo` and
friends, under their real names -- so `collections.abc.Sequence` is
`alias.collections.abc.Sequence`.

## Recipes

**Seeing through `Annotated`.** Both alternatives of an or-pattern must bind the
same names, which is exactly what makes this work -- no guard, no second clause:

```python
match tp:
    case AnnotatedType(__origin__=inner) | inner:
        ...  # `inner` is the underlying type either way
```

**Any attribute, not just the declared ones.** `__match_args__` only constrains
_positional_ sub-patterns. A keyword pattern is a plain `getattr` on the
subject, so anything the object carries is reachable:

```python
case FinalType(__parameters__=()): ...   # not in FinalType.__match_args__
```

**Parameterized matchers.** `case Matcher[int]()` is a syntax error -- pattern
syntax allows no subscripts and no calls. Build the matcher _outside_ the match
instead, closing over the parameter, and use it as an ordinary class pattern:

```python
def list_of(item):
    def check(obj):
        return get_origin(obj) is list and get_args(obj) == (item,)

    cls = type(f"list[{item.__name__}]", (Form,), {})
    cls.__check__ = check
    return cls


list_of_int = list_of(int)

match tp:
    case list_of_int():
        ...  # top level
    case GenericType(alias.dict, [alias.str, list_of_int()]):
        ...  # nested
```

A class pattern goes through `isinstance`, so this holds against any subject.

There is a lighter-weight variant. A _value_ pattern compares with `==`, and
every typing object returns `NotImplemented` against an unknown type, so a
custom reflected `__eq__` runs. The `typing_match.pat` module ships the common
ones -- `Contains`, `OfType`, `Satisfies`:

```python
from typing_match import UnionType, pat


class p:
    admits_str = pat.Contains(str)  # __eq__ returns `str in other`


case UnionType(__args__=p.admits_str): ...
```

Note the asymmetry, though: this one depends on the _subject_ yielding control.
Every typing object does, as does anything using the `@dataclass`-generated
`__eq__` -- but the common hand-written idiom
`return isinstance(other, Cls) and ...` returns `False` rather than
`NotImplemented`, and silently swallows the comparison. That only bites on
metadata objects inside `Annotated`. When in doubt, use the class pattern.

**Mapping patterns work on `__annotations__`.** It is a real `dict`, so the
whole mapping-pattern syntax applies, `**rest` included:

```python
case TypedDictType(__annotations__={"a": alias.int, **rest}): ...
```

## Two things to know about the raw attributes

Sub-patterns read the _actual_ typing object, so the library cannot normalize
what it exposes.

**`Callable` arguments are flat.** `Callable[[int, str], bool].__args__` is
`(int, str, bool)`, not `([int, str], bool)`. Split it in the pattern:

```python
case CallableType(__args__=[*params, ret]): ...
```

A `Callable[..., str]` puts `Ellipsis` in the first position and a
`Callable[P, str]` a `ParamSpec`, both of which have matchers of their own.

**A union's `__origin__` is version-dependent.** Below Python 3.14, `int | str`
is a `types.UnionType` and has no `__origin__` at all, while `Union[int, str]`
does; from 3.14 both spellings are the same object and both have one.
`UnionType` therefore exposes `__args__` alone, which is stable everywhere, and
matches both spellings.

A pattern asking for an attribute the object does not have simply does not
match -- it never raises -- so version-dependent attributes such as
`TypeVar.__default__` are safe to use.

## Custom matchers

Subclass `Form` with any predicate. Most forms need nothing more than an `is_*`
from [typing-inspection] passed as `check=` -- by default it is applied to the
subject's _origin_, and `bare=True` applies it to the subject itself:

```python
from typing_inspection.typing_objects import is_final


class FinalType(Form, check=is_final): ...  # Final[int]


class BareFinalType(Form, check=is_final, bare=True):  # Final
    ...
```

Anything else assigns `__check__` directly:

```python
from typing import Any, get_origin
from typing_match import Form


def is_list_alias(obj: Any, /) -> bool:
    return get_origin(obj) is list


class ListType(Form):
    __origin__: object
    __args__: tuple[object, ...]

    __check__ = is_list_alias
```

Assign `__check__` as a plain function, not a `staticmethod`; it is only ever
looked up on the class. The predicates the library defines itself live in
`typing_match._checks` and follow the `typing-inspection` conventions: one
positional-only `obj`, and a `TypeIs` return where the check narrows.

[typing-inspection]: https://github.com/pydantic/typing-inspection
