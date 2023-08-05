from __future__ import annotations


class ValueMissingError(ValueError):
    """Raised when the value is missing."""


class ValueAlreadySetError(ValueError):
    """Raised when the value is already set."""
