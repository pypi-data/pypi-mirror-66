from __future__ import annotations

from re import escape
from typing import List

from pytest import mark
from pytest import raises

from functional_predicates import Check
from functional_predicates.check import Checker
from functional_predicates.misc import red


# comparisons


@mark.parametrize(
    "checker, infix, passing, failing",
    [
        (Check.lt, "<", [-1, -2, -3], [0, 1, 2]),
        (Check.le, "<=", [0, -1, -2], [1, 2, 3]),
        (Check.eq, "==", [0], [1, -1, 2, -2]),
        (Check.ne, "!=", [1, -1, 2, -2], [0]),
        (Check.ge, ">=", [0, 1, 2], [-1, -2, -3]),
        (Check.gt, ">", [1, 2, 3], [0, -1, -2]),
    ],
)
def test_comparisons(checker: Checker, infix: str, passing: List[int], failing: List[int]) -> None:
    check = checker(0)
    assert isinstance(check, Checker)
    assert repr(check) == f"{infix} 0"
    for i in passing:
        assert check(i)
    for i in failing:
        with raises(AssertionError, match=escape(red(f"{i} {infix} 0"))):
            assert check(i)
