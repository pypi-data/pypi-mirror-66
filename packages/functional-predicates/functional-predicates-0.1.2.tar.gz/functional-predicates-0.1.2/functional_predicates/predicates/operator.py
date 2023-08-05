from __future__ import annotations

from operator import eq
from operator import ge
from operator import gt
from operator import le
from operator import lt
from operator import ne
from typing import Any
from typing import Callable
from typing import TypeVar

from functional_predicates.misc import sentinel
from functional_predicates.predicate import Predicate


ComparisonLike = TypeVar("ComparisonLike", bound="Comparison")


class Comparison(Predicate):
    operator: Callable[[Any, Any], bool]

    def __init__(self: Comparison, other: Any, *, value: Any = sentinel) -> None:
        super().__init__(value=value)
        self.other = other

    def _bool(self: Comparison) -> bool:
        return self.operator(self.value, self.other)

    def _call(self: ComparisonLike, value: Any) -> ComparisonLike:
        return type(self)(self.other, value=value)

    def _repr(self: Comparison) -> str:
        infix = {lt: "<", le: "<=", eq: "==", ne: "!=", ge: ">=", gt: ">"}[self.operator]
        return f"{self._mb_value}{self._mb_space}{infix} {self.other}"


class LT(Comparison):
    operator = lt


class LE(Comparison):
    operator = le


class Eq(Comparison):
    operator = eq


class NE(Comparison):
    operator = ne


class GE(Comparison):
    operator = ge


class GT(Comparison):
    operator = gt
