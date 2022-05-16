"""Patches WTForms to add additional functionality as required by Baseframe."""

from typing import Any, Dict, Optional

from markupsafe import Markup, escape
import wtforms

from .fields import FilterList, ValidatorList


def _patch_wtforms_add_flags() -> None:
    def add_flags(validator, flags: Dict[str, Any]):
        validator_flags = dict(getattr(validator, 'field_flags', {}))  # Make a copy
        validator_flags.update(flags)  # Add new flags
        validator.field_flags = validator_flags  # Add back into validator

    add_flags(wtforms.validators.EqualTo, {'not_solo': True})


_patch_wtforms_add_flags()
del _patch_wtforms_add_flags


def _patch_wtforms_field_init() -> None:
    original_field_init = wtforms.fields.Field.__init__

    def field_init(
        self,
        label: str = None,
        validators: ValidatorList = None,
        filters: FilterList = (),
        description: str = '',
        id: Optional[str] = None,  # NOQA: A002
        default: Optional[str] = None,
        widget=None,
        render_kw: Optional[Dict[str, Optional[str]]] = None,
        name=None,
        _form=None,
        _prefix='',
        _translations=None,
        _meta=None,
        widget_attrs: Optional[
            Dict[str, Optional[str]]
        ] = None,  # Deprecated by render_kw in WTForms 3.0
        **kwargs,
    ):
        if widget_attrs:
            if render_kw:
                render_kw.update(widget_attrs)
            else:
                render_kw = widget_attrs
        original_field_init(
            self,
            escape(label),  # wtforms<3.0 doesn't escape label text
            validators,
            filters=filters,
            description=description,
            id=id,
            default=default,
            widget=widget,
            render_kw=render_kw,
            name=name,
            _form=_form,
            _prefix=_prefix,
            _translations=_translations,
            _meta=_meta,
            **kwargs,
        )

    wtforms.fields.Field.__init__ = field_init


_patch_wtforms_field_init()
del _patch_wtforms_field_init


def _patch_label_call() -> None:
    """Escape text before display (bug in WTForms < 3.0)."""

    def label_call(self, text=None, **kwargs):
        if "for_" in kwargs:
            kwargs["for"] = kwargs.pop("for_")
        else:
            kwargs.setdefault("for", self.field_id)

        attributes = wtforms.widgets.html_params(**kwargs)
        text = escape(text or self.text)
        return Markup("<label %s>%s</label>" % (attributes, text))

    wtforms.fields.core.Label.__call__ = label_call


_patch_label_call()
del _patch_label_call


def _patch_json_output() -> None:
    def field_json(self):
        return {
            'name': self.name,
            'type': self.type,
            'data': self._value(),
        }

    wtforms.fields.Field.__json__ = field_json


_patch_json_output()
del _patch_json_output
