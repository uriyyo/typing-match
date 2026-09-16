from collections.abc import Callable
from inspect import get_annotations
from typing import Any, ClassVar, NoReturn, get_origin

_Check = Callable[[Any], bool]


def _abstract_check(tp: object) -> bool:
    msg = "Form is abstract; subclass it with a check= keyword"
    raise NotImplementedError(msg)


class FormMeta(type):
    __check__: Any

    def __instancecheck__(cls, instance: object) -> bool:
        return cls.__check__(instance)

    def __call__(cls, *args: Any, **kwargs: Any) -> NoReturn:
        msg = f"{cls.__name__} is a match-only pattern and cannot be instantiated"
        raise TypeError(msg)


class Form(metaclass=FormMeta):
    __check__: ClassVar[Any] = _abstract_check

    def __init_subclass__(
        cls,
        check: _Check | None = None,
        bare: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init_subclass__(**kwargs)

        cls.__match_args__ = tuple(get_annotations(cls))

        if check is None:
            return

        if bare:
            cls.__check__ = check
        else:

            def __check__(tp: object, _check: _Check = check) -> bool:
                return _check(get_origin(tp))

            cls.__check__ = __check__


__all__ = [
    "Form",
    "FormMeta",
]
