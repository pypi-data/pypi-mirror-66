from __future__ import annotations

from typing import Any

from functional_predicates.misc import sentinel
from functional_predicates.predicate import Predicate


class Callable(Predicate):
    def _bool(self: Callable) -> bool:
        return callable(self.value)

    def _call(self: Callable, value: Any) -> Callable:
        return type(self)(value=value)

    def _repr(self: Callable) -> str:
        return f"callable({self._mb_value})"


class IsInstance(Predicate):
    def __init__(self: IsInstance, class_or_tuple: Any, *, value: Any = sentinel) -> None:
        super().__init__(value=value)
        self.class_or_tuple = class_or_tuple

    def _bool(self: IsInstance) -> bool:
        return isinstance(self.value, self.class_or_tuple)

    def _call(self: IsInstance, value: Any) -> IsInstance:
        return type(self)(self.class_or_tuple, value=value)

    def _repr(self: IsInstance) -> str:
        return f"isinstance({self._mb_value}{self._mb_comma}{self._mb_space}{self.class_or_tuple})"
