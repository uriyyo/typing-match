from typing import Any

from typing_inspection.typing_objects import is_deprecated, is_noextraitems

from ._checks import is_sentinel
from ._core import Form


class DeprecatedType(Form, check=is_deprecated, bare=True):
    message: str
    category: Any
    stacklevel: int


class NoExtraItemsType(Form, check=is_noextraitems, bare=True): ...


class SentinelType(Form):
    __check__ = is_sentinel


__all__ = [
    "DeprecatedType",
    "NoExtraItemsType",
    "SentinelType",
]
