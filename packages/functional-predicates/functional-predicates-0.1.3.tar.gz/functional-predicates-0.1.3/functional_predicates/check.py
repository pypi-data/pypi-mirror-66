from __future__ import annotations

import typing
from itertools import chain
from typing import Any
from typing import Iterable
from typing import Optional

from functional_predicates.base import Base
from functional_predicates.misc import sentinel
from functional_predicates.predicate import Predicate
from functional_predicates.predicates.operator import Eq
from functional_predicates.predicates.operator import GE
from functional_predicates.predicates.operator import GT
from functional_predicates.predicates.operator import LE
from functional_predicates.predicates.operator import LT
from functional_predicates.predicates.operator import NE
from functional_predicates.predicates.operator import Not_
from functional_predicates.predicates.types import Callable
from functional_predicates.predicates.types import IsInstance


class Checker(Base):
    def __init__(
        self: Checker, *, value: Any = sentinel, predicates: Optional[Iterable[Predicate]] = None,
    ) -> None:
        super().__init__(value=value)
        if predicates is None:
            self.predicates = []
        else:
            self.predicates = predicates

    # operator

    def lt(self: Checker, x: Any) -> Checker:
        return self._append(LT, x)

    def le(self: Checker, x: Any) -> Checker:
        return self._append(LE, x)

    def eq(self: Checker, x: Any) -> Checker:
        return self._append(Eq, x)

    def ne(self: Checker, x: Any) -> Checker:
        return self._append(NE, x)

    def ge(self: Checker, x: Any) -> Checker:
        return self._append(GE, x)

    def gt(self: Checker, x: Any) -> Checker:
        return self._append(GT, x)

    def not_(self: Checker) -> Checker:
        return self._append(Not_)

    # types

    def callable(self: Checker) -> Checker:  # noqa: A003
        return self._append(Callable)

    def isinstance(self: Checker, x: Any) -> Checker:  # noqa: A003
        return self._append(IsInstance, x)

    # private

    def _append(
        self: Checker, cls: typing.Callable[..., Predicate], *args: Any, **kwargs: Any,
    ) -> Checker:
        return type(self)(
            value=self.value,
            predicates=list(chain(self.predicates, [cls(*args, value=self.value, **kwargs)])),
        )

    def _bool(self: Checker) -> bool:
        return all(self.predicates)

    def _call(self: Checker, value: Any) -> Checker:
        return type(self)(
            value=value, predicates=[predicate(value=value) for predicate in self.predicates],
        )

    def _repr(self: Checker) -> str:
        if self.predicates:
            return ", ".join(map(repr, self.predicates))
        else:
            return f"{type(self).__name__}{self._mb_paren_value}"


Check = Checker()
