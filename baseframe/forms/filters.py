# -*- coding: utf-8 -*-

# Filters may receive None as input for an unpopulated field, which is why
# many of these have a "value.operation if value else value" construct.
# The original value is returned if it's falsy.


def join(sep):
    def join_inner(value):
        return sep.join(value)
    return join_inner


def lower():
    def lower_inner(value):
        return value.lower() if value else value
    return lower_inner


def upper():
    def upper_inner(value):
        return value.upper() if value else value
    return upper_inner


def strip(chars=None):
    def strip_inner(value):
        return value.strip(chars) if value else value
    return strip_inner


def lstrip(chars=None):
    def lstrip_inner(value):
        return value.lstrip(chars) if value else value
    return lstrip_inner


def rstrip(chars=None):
    def rstrip_inner(value):
        return value.rstrip(chars) if value else value
    return rstrip_inner


def split(sep=None, maxsplit=-1):
    def split_inner(value):
        return value.split(sep, maxsplit) if value else value
    return split_inner


def splitlines(keepends=False):
    def splitlines_inner(value):
        return value.splitlines(keepends) if value else value
    return splitlines_inner


def nullblank():
    def nullblank_inner(value):
        return value if value else None
    return nullblank_inner
