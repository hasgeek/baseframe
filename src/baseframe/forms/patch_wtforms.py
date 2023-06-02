"""Patches WTForms to add additional functionality as required by Baseframe."""

import typing as t

import wtforms

from .typing import ValidatorProtocol


def _patch_wtforms_add_flags() -> None:
    def add_flags(validator: ValidatorProtocol, flags: t.Dict[str, t.Any]) -> None:
        validator_flags = dict(getattr(validator, 'field_flags', {}))  # Make a copy
        validator_flags.update(flags)  # Add new flags
        validator.field_flags = validator_flags  # Add back into validator

    add_flags(wtforms.validators.EqualTo, {'not_solo': True})


_patch_wtforms_add_flags()
del _patch_wtforms_add_flags


def _patch_json_output() -> None:
    """Add __json__ method to Field class."""

    def field_json(self: wtforms.Field) -> t.Dict[str, t.Any]:
        """Render field to a JSON-compatible dictionary."""
        return {
            'name': self.name,
            'type': self.type,
            'data': self._value(),  # pylint: disable=W0212
        }

    wtforms.fields.Field.__json__ = field_json


_patch_json_output()
del _patch_json_output
