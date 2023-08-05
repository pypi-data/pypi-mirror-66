from __future__ import annotations

from typing import Any
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

from functional_predicates.misc import sentinel
from functional_predicates.predicate import Predicate


CallableLike = TypeVar("CallableLike", bound="Callable")
HasAttrLike = TypeVar("HasAttrLike", bound="HasAttr")
IsInstanceLike = TypeVar("IsInstanceLike", bound="IsInstance")


class Callable(Predicate):
    def _bool(self: Callable) -> bool:
        return callable(self.value)

    def _call(self: CallableLike, value: Any) -> CallableLike:
        return type(self)(value=value)

    def _repr(self: Callable) -> str:
        return f"callable({self._mb_value})"


class HasAttr(Predicate):
    def __init__(
        self: HasAttr, attr: Union[Type, Tuple[Type, ...]], *, value: Any = sentinel,
    ) -> None:
        super().__init__(value=value)
        self.attr = attr

    def _bool(self: HasAttr) -> bool:
        return hasattr(self.value, self.attr)

    def _call(self: HasAttrLike, value: Any) -> HasAttrLike:
        return type(self)(self.attr, value=value)

    def _repr(self: HasAttr) -> str:
        return f"hasattr({self._mb_value}{self._mb_comma_space}{self.attr})"


class IsInstance(Predicate):
    def __init__(
        self: IsInstance, class_or_tuple: Union[Type, Tuple[Type, ...]], *, value: Any = sentinel,
    ) -> None:
        super().__init__(value=value)
        self.class_or_tuple = class_or_tuple

    def _bool(self: IsInstance) -> bool:
        return isinstance(self.value, self.class_or_tuple)

    def _call(self: IsInstanceLike, value: Any) -> IsInstanceLike:
        return type(self)(self.class_or_tuple, value=value)

    def _repr(self: IsInstance) -> str:
        return f"isinstance({self._mb_value}{self._mb_comma_space}{self.class_or_tuple})"
