import typing as ty

import pytest

from typing_match import UnionType, pat


class p:
    admits_str = pat.Contains(str)
    a_class = pat.OfType(type)
    all_classes = pat.Satisfies(lambda args: all(isinstance(a, type) for a in args))


def test_contains() -> None:
    match ty.Union[int, str]:
        case UnionType(__args__=p.admits_str):
            pass
        case _:
            pytest.fail("expected a union admitting str")

    match ty.Union[int, bytes]:
        case UnionType(__args__=p.admits_str):
            pytest.fail("no str in this union")
        case UnionType():
            pass
        case _:
            pytest.fail("expected a UnionType")


def test_contains_yields_on_non_containers() -> None:
    match 42:
        case p.admits_str:
            pytest.fail("an int contains nothing")
        case _:
            pass


def test_of_type() -> None:
    match ty.Union[int, str]:
        case UnionType(__args__=[p.a_class, p.a_class]):
            pass
        case _:
            pytest.fail("expected two runtime classes")


def test_satisfies() -> None:
    match ty.Union[int, str]:
        case UnionType(__args__=p.all_classes):
            pass
        case _:
            pytest.fail("expected all-class union arguments")

    match ty.Union[int, ty.Literal[1]]:
        case UnionType(__args__=p.all_classes):
            pytest.fail("Literal[1] is not a class")
        case UnionType():
            pass
        case _:
            pytest.fail("expected a UnionType")


def test_helpers_are_unhashable() -> None:
    for helper in (p.admits_str, p.a_class, p.all_classes):
        with pytest.raises(TypeError):
            hash(helper)


def test_reprs() -> None:
    assert repr(pat.Contains(str)) == "Contains(<class 'str'>)"
    assert repr(pat.OfType(int)) == "OfType(<class 'int'>)"
    assert repr(pat.Satisfies(callable)) == "Satisfies(callable)"
    assert repr(pat.Satisfies(callable, name="is_callable")) == (
        "Satisfies(is_callable)"
    )
