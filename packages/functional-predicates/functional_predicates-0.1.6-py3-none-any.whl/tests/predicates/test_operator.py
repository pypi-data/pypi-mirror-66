from __future__ import annotations

from re import escape
from typing import Any
from typing import Callable
from typing import List

from pytest import mark
from pytest import raises

from functional_predicates import Check
from functional_predicates.check import Checker
from functional_predicates.misc import red


@mark.parametrize(
    "checker, infix, passing, failing",
    [
        (Check.not_, "~", [False, 0, ""], [True, 1, " "]),
        (Check.truth, "", [True, 1, "1"], [False, 0, ""]),
    ],
)
def test_unary(
    checker: Callable[[], Checker], infix: str, passing: List[int], failing: List[int],
) -> None:
    check = checker()
    assert isinstance(check, Checker)
    assert repr(check) == infix
    for i in passing:
        assert check(i)
    for i in failing:
        with raises(AssertionError, match=escape(red(f"{infix} {i}"))):
            assert check(i)


_test_sentinel = object()


@mark.parametrize(
    "checker, value, infix, passing, failing",
    [
        (Check.lt, 0, "<", [-1, -2, -3], [0, 1, 2]),
        (Check.le, 0, "<=", [0, -1, -2], [1, 2, 3]),
        (Check.eq, 0, "==", [0], [1, -1, 2, -2]),
        (Check.ne, 0, "!=", [1, -1, 2, -2], [0]),
        (Check.ge, 0, ">=", [0, 1, 2], [-1, -2, -3]),
        (Check.gt, 0, ">", [1, 2, 3], [0, -1, -2]),
        (Check.is_, _test_sentinel, "is", [_test_sentinel], [object()]),
        (Check.contains, 0, "contains", [[0], [0, 1], [0, 1, 2]], [[], [-1], [-2]]),
    ],
)
def test_binary(
    checker: Callable[[Any], Checker],
    value: Any,
    infix: str,
    passing: List[Any],
    failing: List[Any],
) -> None:
    check = checker(value)
    assert isinstance(check, Checker)
    assert repr(check) == f"{infix} {value}"
    for i in passing:
        assert check(i)
    for i in failing:
        with raises(AssertionError, match=escape(red(f"{i} {infix} {value}"))):
            assert check(i)
