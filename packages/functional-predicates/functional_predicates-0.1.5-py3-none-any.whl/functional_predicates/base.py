from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import TypeVar

from functional_predicates.errors import InvalidValueError
from functional_predicates.errors import UnboundValueError
from functional_predicates.errors import ValueAlreadyBoundError
from functional_predicates.misc import sentinel


BaseLike = TypeVar("BaseLike", bound="Base")


class Base(ABC):
    def __init__(self: Base, *, value: Any = sentinel) -> None:
        self.value = value

    def __bool__(self: Base) -> bool:
        if self._has_value:
            return self._bool()
        else:
            raise UnboundValueError(f"{self} has no bound value")

    def __call__(self: BaseLike, value: Any) -> BaseLike:
        if self._has_value:
            raise ValueAlreadyBoundError(f"{self} already has a value")
        else:
            if value is sentinel:
                raise InvalidValueError(f"{self} cannot bind {value}")
            else:
                return self._call(value)

    def __repr__(self: Base) -> str:
        return self._repr()

    def __str__(self: Base) -> str:
        return repr(self)

    @abstractmethod
    def _bool(self: Base) -> bool:
        raise NotImplementedError

    @abstractmethod
    def _call(self: BaseLike, value: Any) -> BaseLike:
        raise NotImplementedError(value)

    @abstractmethod
    def _repr(self: Base) -> str:
        raise NotImplementedError

    # private

    @property
    def _has_value(self: Base) -> bool:
        return self.value is not sentinel

    @property
    def _mb_comma_space(self: Base) -> str:
        return ", " if self._has_value else ""

    @property
    def _mb_paren_value(self: Base) -> str:
        return f"({self.value})" if self._has_value else ""

    @property
    def _mb_space(self: Base) -> str:
        return " " if self._has_value else ""

    @property
    def _mb_value(self: Base) -> str:
        return f"{self.value}" if self._has_value else ""
