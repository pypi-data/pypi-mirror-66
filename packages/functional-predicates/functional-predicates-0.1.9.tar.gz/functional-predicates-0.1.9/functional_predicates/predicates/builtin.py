from __future__ import annotations

from functional_predicates.predicates.predicate import BinaryPredicate
from functional_predicates.predicates.predicate import UnaryPredicate


class All(UnaryPredicate):
    operator = all

    def _repr(self: All) -> str:
        return f"all({self._mb_value})"


class Any(UnaryPredicate):
    operator = any

    def _repr(self: Any) -> str:
        return f"any({self._mb_value})"


class Callable(UnaryPredicate):
    operator = callable

    def _repr(self: Callable) -> str:
        return f"callable({self._mb_value})"


class HasAttr(BinaryPredicate):
    operator = hasattr

    def _repr(self: HasAttr) -> str:
        return f"hasattr({self._mb_value}{self._mb_comma_space}{self.other})"


class IsInstance(BinaryPredicate):
    operator = isinstance

    def _repr(self: IsInstance) -> str:
        return f"isinstance({self._mb_value}{self._mb_comma_space}{self.other})"


class IsSubClass(BinaryPredicate):
    operator = issubclass

    def _repr(self: IsSubClass) -> str:
        return f"issubclass({self._mb_value}{self._mb_comma_space}{self.other})"
