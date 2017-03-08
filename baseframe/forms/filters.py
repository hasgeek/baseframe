# -*- coding: utf-8 -*-

"""
Use filters with form fields to process filter data::

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


def lower():
    """
    Convert data to lower case.
    """
    def lower_inner(value):
        return value.lower() if value else value
    return lower_inner


def upper():
    """
    Convert data to upper case.
    """
    def upper_inner(value):
        return value.upper() if value else value
    return upper_inner


def strip(chars=None):
    """
    Strip whitespace from both ends

    :param chars: If specified, strip these characters instead of whitespace
    """
    def strip_inner(value):
        return value.strip(chars) if value else value
    return strip_inner


def lstrip(chars=None):
    """
    Strip whitespace from beginning of data

    :param chars: If specified, strip these characters instead of whitespace
    """
    def lstrip_inner(value):
        return value.lstrip(chars) if value else value
    return lstrip_inner


def rstrip(chars=None):
    """
    Strip whitespace from end of data

    :param chars: If specified, strip these characters instead of whitespace
    """
    def rstrip_inner(value):
        return value.rstrip(chars) if value else value
    return rstrip_inner


def none_if_empty():
    """
    If data is empty or evalues to boolean false, replace with None
    """
    def none_if_empty_inner(value):
        return value if value else None
    return none_if_empty_inner
