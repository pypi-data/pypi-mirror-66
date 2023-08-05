from __future__ import annotations

from re import escape

from pytest import raises

from functional_predicates import Check
from functional_predicates.check import Checker
from functional_predicates.misc import red


def test_all() -> None:
    check = Check.all()
    assert isinstance(check, Checker)
    assert repr(check) == "all()"
    assert check([True, True])
    with raises(AssertionError, match=escape(red("all([True, False])"))):
        assert check([True, False])


def test_any() -> None:
    check = Check.any()
    assert isinstance(check, Checker)
    assert repr(check) == "any()"
    assert check([True, False])
    with raises(AssertionError, match=escape(red("any([False, False])"))):
        assert check([False, False])


def test_callable() -> None:
    check = Check.callable()
    assert isinstance(check, Checker)
    assert repr(check) == "callable()"

    def func() -> None:
        ...

    assert check(func)
    assert check(lambda x: x)
    with raises(AssertionError, match=escape(red("callable(0)"))):
        assert check(0)


def test_hasattr() -> None:
    check = Check.hasattr("real")
    assert isinstance(check, Checker)
    assert repr(check) == "hasattr(real)"
    assert check(0)
    with raises(AssertionError, match=escape(red("hasattr(0, real)"))):
        assert check("0")


def test_isinstance() -> None:
    check = Check.isinstance(int)
    assert isinstance(check, Checker)
    assert repr(check) == "isinstance(<class 'int'>)"
    assert check(0)
    with raises(AssertionError, match=escape(red("isinstance(0, <class 'int'>)"))):
        assert check("0")


def test_issubclass() -> None:
    check = Check.issubclass(int)
    assert isinstance(check, Checker)
    assert repr(check) == "issubclass(<class 'int'>)"
    assert check(int)

    class SubInt(int):
        ...

    assert check(SubInt)

    with raises(AssertionError, match=escape(red("issubclass(<class 'float'>, <class 'int'>)"))):
        assert check(float)
