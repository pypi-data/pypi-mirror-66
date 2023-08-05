from __future__ import annotations

from functional_predicates.base import Base
from functional_predicates.misc import green
from functional_predicates.misc import red


class Predicate(Base):
    def __repr__(self: Predicate) -> str:
        text = self._repr()
        if self._has_value:
            return green(text) if self else red(text)
        else:
            return text
