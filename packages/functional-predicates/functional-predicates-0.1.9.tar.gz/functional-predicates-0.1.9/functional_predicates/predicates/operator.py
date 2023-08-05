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

from functional_predicates.predicates.predicate import BinaryPredicate
from functional_predicates.predicates.predicate import UnaryPredicate


class LT(BinaryPredicate):
    operator = lt

    def _repr(self: BinaryPredicate) -> str:
        return f"{self._mb_value}{self._mb_space}< {self.other}"


class LE(BinaryPredicate):
    operator = le

    def _repr(self: BinaryPredicate) -> str:
        return f"{self._mb_value}{self._mb_space}<= {self.other}"


class Eq(BinaryPredicate):
    operator = eq

    def _repr(self: BinaryPredicate) -> str:
        return f"{self._mb_value}{self._mb_space}== {self.other}"


class NE(BinaryPredicate):
    operator = ne

    def _repr(self: BinaryPredicate) -> str:
        return f"{self._mb_value}{self._mb_space}!= {self.other}"


class GE(BinaryPredicate):
    operator = ge

    def _repr(self: BinaryPredicate) -> str:
        return f"{self._mb_value}{self._mb_space}>= {self.other}"


class GT(BinaryPredicate):
    operator = gt

    def _repr(self: BinaryPredicate) -> str:
        return f"{self._mb_value}{self._mb_space}> {self.other}"


class Not_(UnaryPredicate):
    operator = not_

    def _repr(self: Not_) -> str:
        return f"~{self._mb_value}"


class Truth(UnaryPredicate):
    operator = truth

    def _repr(self: Truth) -> str:
        return f"{self._mb_value}"


class Is_(BinaryPredicate):
    operator = is_

    def _repr(self: BinaryPredicate) -> str:
        return f"{self._mb_value}{self._mb_space}is {self.other}"


class IsNot(BinaryPredicate):
    operator = is_not

    def _repr(self: BinaryPredicate) -> str:
        return f"{self._mb_value}{self._mb_space}is not {self.other}"


class Contains(BinaryPredicate):
    operator = contains

    def _repr(self: BinaryPredicate) -> str:
        return f"{self.other} in{self._mb_space}{self._mb_value}"
