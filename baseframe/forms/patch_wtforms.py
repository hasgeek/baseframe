# -*- coding: utf-8 -*-

"""
Patches WTForms to add additional functionality as required by Baseframe.
"""

from __future__ import absolute_import
import wtforms

__all__ = []


def _patch_wtforms_add_flags():
    def add_flags(validator, flags):
        validator.field_flags = tuple(flags) + tuple(getattr(validator, 'field_flags', ()))

    add_flags(wtforms.validators.EqualTo, ('not_solo', ))


_patch_wtforms_add_flags()
del _patch_wtforms_add_flags


def _patch_wtforms_field_init():
    original_field_init = None

    def __field_init__(self, label=None, validators=None, filters=tuple(),
            description='', id=None, default=None, widget=None,
            _form=None, _name=None, _prefix='', _translations=None,
            _meta=None, widget_attrs=None, **kwargs):

        original_field_init(self, label, validators, filters=filters,
            description=description, id=id, default=default, widget=widget, _form=_form,
            _name=_name, _prefix=_prefix, _translations=_translations, _meta=_meta, **kwargs)
        self.widget_attrs = widget_attrs or {}

    if wtforms.fields.Field.__init__ is not __field_init__:
        original_field_init = wtforms.fields.Field.__init__
        wtforms.fields.Field.__init__ = __field_init__


_patch_wtforms_field_init()
del _patch_wtforms_field_init
