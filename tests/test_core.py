import typing as ty

import pytest

from typing_match import AnnotatedType, FinalType, Form, FormMeta, alias


def test_matchers_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError, match="match-only pattern"):
        AnnotatedType(int, (int,), ())


def test_match_args_come_from_the_annotations() -> None:
    assert AnnotatedType.__match_args__ == ("__origin__", "__args__", "__metadata__")
    assert FinalType.__match_args__ == ("__origin__", "__args__")


def test_a_missing_attribute_fails_the_pattern_instead_of_raising() -> None:
    class Weird(Form, check=lambda tp: True, bare=True):
        __origin__: object

    match int:
        case Weird(__origin__=_):
            pytest.fail("a plain class has no __origin__")
        case _:
            pass


def test_custom_matcher() -> None:
    def is_list(tp: object) -> bool:
        return ty.get_origin(tp) is list

    class ListType(Form):
        __origin__: object
        __args__: tuple[object, ...]

        __check__ = is_list

    assert isinstance(list[int], ListType)
    assert not isinstance(dict[str, int], ListType)

    match list[int]:
        case ListType(_, [alias.int]):
            pass
        case _:
            pytest.fail("expected a ListType")


def test_form_itself_is_abstract() -> None:
    with pytest.raises(NotImplementedError):
        isinstance(int, Form)


def test_every_matcher_uses_the_metaclass() -> None:
    import typing_match

    matchers = [
        getattr(typing_match, name)
        for name in typing_match.__all__
        if name not in ("Form", "FormMeta", "alias", "pat")
    ]

    assert matchers
    assert all(type(matcher) is FormMeta for matcher in matchers)
