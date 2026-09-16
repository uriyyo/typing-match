from collections.abc import Callable, Container
from typing import Any, cast


class Contains:
    def __init__(self, item: Any, /) -> None:
        self.item = item

    def __eq__(self, other: object) -> Any:
        try:
            return self.item in cast("Container[Any]", other)
        except TypeError:
            return NotImplemented

    __hash__ = None  # type: ignore[assignment]

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.item!r})"


class OfType:
    def __init__(self, cls: type | tuple[type, ...], /) -> None:
        self.cls = cls

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.cls)

    __hash__ = None  # type: ignore[assignment]

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.cls!r})"


class Satisfies:
    def __init__(
        self,
        pred: Callable[[Any], object],
        /,
        *,
        name: str | None = None,
    ) -> None:
        self.pred = pred
        self.name = name

    def __eq__(self, other: object) -> bool:
        return bool(self.pred(other))

    __hash__ = None  # type: ignore[assignment]

    def __repr__(self) -> str:
        name = self.name or getattr(self.pred, "__name__", repr(self.pred))
        return f"{type(self).__name__}({name})"


__all__ = [
    "Contains",
    "OfType",
    "Satisfies",
]
