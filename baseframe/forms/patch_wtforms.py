# -*- coding: utf-8 -*-

"""
Patches WTForms to add additional functionality as required by Baseframe.
"""

__all__ = []


import wtforms


def add_flags(validator, flags):
    validator.field_flags = tuple(flags) + tuple(getattr(validator, 'field_flags', ()))


add_flags(wtforms.validators.EqualTo, ('not_solo', ))
