from __future__ import annotations

from typing import Any
from typing import Callable
from typing import TypeVar

from functional_predicates.base import Base
from functional_predicates.misc import green
from functional_predicates.misc import red
from functional_predicates.misc import sentinel


UnaryPredicateLike = TypeVar("UnaryPredicateLike", bound="UnaryPredicate")
BinaryPredicateLike = TypeVar("BinaryPredicateLike", bound="BinaryPredicate")


class Predicate(Base):
    def __repr__(self: Predicate) -> str:
        text = self._repr()
        if self._has_value:
            return green(text) if self else red(text)
        else:
            return text


class UnaryPredicate(Predicate):
    operator: Callable[[Any], bool]

    def _bool(self: UnaryPredicate) -> bool:
        return self.operator(self.value)

    def _call(self: UnaryPredicateLike, value: Any) -> UnaryPredicateLike:
        return type(self)(value=value)


class BinaryPredicate(Predicate):
    operator: Callable[[Any, Any], bool]

    def __init__(self: BinaryPredicate, other: Any, *, value: Any = sentinel) -> None:
        super().__init__(value=value)
        self.other = other

    def _bool(self: BinaryPredicate) -> bool:
        return self.operator(self.value, self.other)

    def _call(self: BinaryPredicateLike, value: Any) -> BinaryPredicateLike:
        return type(self)(self.other, value=value)
