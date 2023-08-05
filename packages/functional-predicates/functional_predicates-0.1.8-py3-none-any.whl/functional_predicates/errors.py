from __future__ import annotations


class InvalidValueError(ValueError):
    """Raised when binding an invalid value."""


class UnboundValueError(ValueError):
    """Raised when no value is bound."""


class ValueAlreadyBoundError(ValueError):
    """Raised when a value is already bound."""
