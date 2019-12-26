# -*- coding: utf-8 -*-

"""
Patches WTForms to add additional functionality as required by Baseframe.
"""

from __future__ import absolute_import

import wtforms

__all__ = []


def _patch_wtforms_add_flags():
    """Patch WTForms validators as required (currently just one type of patch)"""

    def add_flags(validator, flags):
        """Add more flags to existing WTForms validators"""
        validator.field_flags = tuple(flags) + tuple(
            getattr(validator, 'field_flags', ())
        )

    # Patch the `EqualTo` validator to add a 'not_solo' flag on any field it is used on
    add_flags(wtforms.validators.EqualTo, ('not_solo',))


_patch_wtforms_add_flags()
del _patch_wtforms_add_flags


def _patch_wtforms_field_init():
    original_field_init = None

    def field_init(
        self,
        label=None,
        validators=None,
        filters=(),
        description='',
        id=None,  # NOQA: A002
        default=None,
        widget=None,
        _form=None,
        _name=None,
        _prefix='',
        _translations=None,
        _meta=None,
        widget_attrs=None,
        **kwargs
    ):

        original_field_init(
            self,
            label,
            validators,
            filters=filters,
            description=description,
            id=id,
            default=default,
            widget=widget,
            _form=_form,
            _name=_name,
            _prefix=_prefix,
            _translations=_translations,
            _meta=_meta,
            **kwargs
        )
        self.widget_attrs = widget_attrs or {}

    if wtforms.fields.Field.__init__ is not field_init:
        original_field_init = wtforms.fields.Field.__init__
        wtforms.fields.Field.__init__ = field_init


_patch_wtforms_field_init()
del _patch_wtforms_field_init


def render_script(self, tag=True):
    """
    Render the JavaScript necessary (including script tag) for this field.

    This delegates rendering to
    :meth:`meta.render_field_script`
    whose default behavior is to call the field's widget, passing any
    keyword arguments from this call along to the widget.

    :param bool tag: If False, don't include a ``<script>`` tag
    """
    return self.meta.render_field_script(self, tag)


def meta_render_script(self, field, tag):
    """
    render_script allows customization of how widget rendering is done.

    The default implementation calls ``field.widget.render_js(field, **render_kw)``
    """
    if hasattr(field.widget, 'render_script'):
        return field.widget.render_script(field, tag)


def _patch_wtforms_field_render():
    wtforms.Field.render_script = render_script
    wtforms.meta.DefaultMeta.render_field_script = meta_render_script


_patch_wtforms_field_render()
del _patch_wtforms_field_render
