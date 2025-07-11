"""
Use filters with form fields to process filter data.

::

    StringField('name', filters=[lower(), strip(), none_if_empty()])

Some filters accept config parameters while others don't. All of them need
to be called to retrieve the configured filter for the sake of consistency.

Filters apply *both* when a form is populated from an object, and from form
data. This means they need to be bidirectional and cannot change datatype,
unlike the `coerce` parameter accepted by SelectField, which only applies to
form data.

Filters may receive None as input for an unpopulated field, which is why many
of these have a "value.operation if value else value" construct. The original
value is returned if it's falsy.
"""

from collections.abc import Iterable
from typing import Any, Callable, Optional

from coaster.utils import unicode_extended_whitespace

__all__ = ['lower', 'lstrip', 'none_if_empty', 'rstrip', 'strip', 'strip_each', 'upper']


def lower() -> Callable[[Optional[str]], Optional[str]]:
    """Convert data to lower case."""

    def lower_inner(value: Optional[str]) -> Optional[str]:
        return value.lower() if value else value

    return lower_inner


def upper() -> Callable[[Optional[str]], Optional[str]]:
    """Convert data to upper case."""

    def upper_inner(value: Optional[str]) -> Optional[str]:
        return value.upper() if value else value

    return upper_inner


def strip(
    chars: str = unicode_extended_whitespace,
) -> Callable[[Optional[str]], Optional[str]]:
    """
    Strip whitespace from both ends.

    :param chars: If specified, strip these characters instead of whitespace
    """

    def strip_inner(value: Optional[str]) -> Optional[str]:
        return value.strip(chars) if value else value

    return strip_inner


def lstrip(
    chars: str = unicode_extended_whitespace,
) -> Callable[[Optional[str]], Optional[str]]:
    """
    Strip whitespace from beginning of data.

    :param chars: If specified, strip these characters instead of whitespace
    """

    def lstrip_inner(value: Optional[str]) -> Optional[str]:
        return value.lstrip(chars) if value else value

    return lstrip_inner


def rstrip(
    chars: str = unicode_extended_whitespace,
) -> Callable[[Optional[str]], Optional[str]]:
    """
    Strip whitespace from end of data.

    :param chars: If specified, strip these characters instead of whitespace
    """

    def rstrip_inner(value: Optional[str]) -> Optional[str]:
        return value.rstrip(chars) if value else value

    return rstrip_inner


def strip_each(
    chars: str = unicode_extended_whitespace,
) -> Callable[[Optional[Iterable[str]]], Optional[Iterable[str]]]:
    """
    Strip whitespace and remove blank elements from each element in an iterable.

    Falsy values are returned unprocessed.

    :param chars: If specified, strip these characters instead of whitespace
    """

    def strip_each_inner(
        value: Optional[Iterable[str]],
    ) -> Optional[Iterable[str]]:
        if value:
            return [sline for sline in [line.strip(chars) for line in value] if sline]
        return value

    return strip_each_inner


def none_if_empty() -> Callable[[Any], Optional[Any]]:
    """If data is empty or evaluates to boolean false, replace with None."""

    def none_if_empty_inner(value: Any) -> Optional[Any]:
        return value if value else None

    return none_if_empty_inner
