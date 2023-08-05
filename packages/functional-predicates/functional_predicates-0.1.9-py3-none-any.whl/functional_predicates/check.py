from __future__ import annotations

import typing
from itertools import chain
from typing import Iterable
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

from functional_predicates.base import Base
from functional_predicates.misc import sentinel
from functional_predicates.predicates.builtin import All
from functional_predicates.predicates.builtin import Any
from functional_predicates.predicates.builtin import Callable
from functional_predicates.predicates.builtin import HasAttr
from functional_predicates.predicates.builtin import IsInstance
from functional_predicates.predicates.builtin import IsSubClass
from functional_predicates.predicates.operator import Contains
from functional_predicates.predicates.operator import Eq
from functional_predicates.predicates.operator import GE
from functional_predicates.predicates.operator import GT
from functional_predicates.predicates.operator import Is_
from functional_predicates.predicates.operator import IsNot
from functional_predicates.predicates.operator import LE
from functional_predicates.predicates.operator import LT
from functional_predicates.predicates.operator import NE
from functional_predicates.predicates.operator import Not_
from functional_predicates.predicates.operator import Truth
from functional_predicates.predicates.predicate import Predicate


class Checker(Base):
    def __init__(
        self: Checker,
        *,
        value: typing.Any = sentinel,
        predicates: Optional[Iterable[Predicate]] = None,
    ) -> None:
        super().__init__(value=value)
        if predicates is None:
            self.predicates = []
        else:
            self.predicates = predicates

    # builtin

    def all(self: Checker) -> Checker:  # noqa: A003
        return self._append(All)

    def any(self: Checker) -> Checker:  # noqa: A003
        return self._append(Any)

    def callable(self: Checker) -> Checker:  # noqa: A003
        return self._append(Callable)

    def hasattr(self: Checker, x: str) -> Checker:  # noqa: A003
        return self._append(HasAttr, x)

    def isinstance(self: Checker, x: Union[Type, Tuple[Type, ...]]) -> Checker:  # noqa: A003
        return self._append(IsInstance, x)

    def issubclass(self: Checker, x: Union[Type, Tuple[Type, ...]]) -> Checker:  # noqa: A003
        return self._append(IsSubClass, x)

    # operator

    def lt(self: Checker, x: typing.Any) -> Checker:
        return self._append(LT, x)

    def le(self: Checker, x: typing.Any) -> Checker:
        return self._append(LE, x)

    def eq(self: Checker, x: typing.Any) -> Checker:
        return self._append(Eq, x)

    def ne(self: Checker, x: typing.Any) -> Checker:
        return self._append(NE, x)

    def ge(self: Checker, x: typing.Any) -> Checker:
        return self._append(GE, x)

    def gt(self: Checker, x: typing.Any) -> Checker:
        return self._append(GT, x)

    def not_(self: Checker) -> Checker:
        return self._append(Not_)

    def truth(self: Checker) -> Checker:
        return self._append(Truth)

    def is_(self: Checker, x: typing.Any) -> Checker:
        return self._append(Is_, x)

    def is_not(self: Checker, x: typing.Any) -> Checker:
        return self._append(IsNot, x)

    def contains(self: Checker, x: typing.Any) -> Checker:
        return self._append(Contains, x)

    # private

    def _append(
        self: Checker,
        cls: typing.Callable[..., Predicate],
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> Checker:
        return type(self)(
            value=self.value,
            predicates=list(chain(self.predicates, [cls(*args, value=self.value, **kwargs)])),
        )

    def _bool(self: Checker) -> bool:
        return all(self.predicates)

    def _call(self: Checker, value: typing.Any) -> Checker:
        return type(self)(
            value=value, predicates=[predicate(value=value) for predicate in self.predicates],
        )

    def _repr(self: Checker) -> str:
        if self.predicates:
            return ", ".join(map(repr, self.predicates))
        else:
            return f"{type(self).__name__}{self._mb_paren_value}"


Check = Checker()
