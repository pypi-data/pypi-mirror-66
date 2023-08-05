from __future__ import annotations

from operator import contains
from operator import eq
from operator import ge
from operator import gt
from operator import is_
from operator import is_not
from operator import le
from operator import lt
from operator import ne
from operator import not_
from operator import truth
from typing import Any
from typing import Callable
from typing import TypeVar

from functional_predicates.misc import sentinel
from functional_predicates.predicate import Predicate


UnaryLike = TypeVar("UnaryLike", bound="Unary")
BinaryLike = TypeVar("BinaryLike", bound="Binary")


class Unary(Predicate):
    operator: Callable[[Any], bool]
    infix_map = {not_: "~", truth: ""}

    def _bool(self: Unary) -> bool:
        return self.operator(self.value)

    def _call(self: UnaryLike, value: Any) -> UnaryLike:
        return type(self)(value=value)

    def _repr(self: Unary) -> str:
        return f"{self.infix_map[self.operator]}{self._mb_space}{self._mb_value}"


class Binary(Predicate):
    operator: Callable[[Any, Any], bool]
    infix_map = {
        lt: "<",
        le: "<=",
        eq: "==",
        ne: "!=",
        ge: ">=",
        gt: ">",
        is_: "is",
        is_not: "is not",
        contains: "contains",
    }

    def __init__(self: Binary, other: Any, *, value: Any = sentinel) -> None:
        super().__init__(value=value)
        self.other = other

    def _bool(self: Binary) -> bool:
        return self.operator(self.value, self.other)

    def _call(self: BinaryLike, value: Any) -> BinaryLike:
        return type(self)(self.other, value=value)

    def _repr(self: Binary) -> str:
        return f"{self._mb_value}{self._mb_space}{self.infix_map[self.operator]} {self.other}"


class LT(Binary):
    operator = lt


class LE(Binary):
    operator = le


class Eq(Binary):
    operator = eq


class NE(Binary):
    operator = ne


class GE(Binary):
    operator = ge


class GT(Binary):
    operator = gt


class Not_(Unary):
    operator = not_


class Truth(Unary):
    operator = truth


class Is_(Binary):
    operator = is_


class IsNot(Binary):
    operator = is_not


class Contains(Binary):
    operator = contains
