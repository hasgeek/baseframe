"""Patches WTForms to add additional functionality as required by Baseframe."""

from typing import Any, Dict

import wtforms


def _patch_wtforms_add_flags() -> None:
    def add_flags(validator, flags: Dict[str, Any]):
        validator_flags = dict(getattr(validator, 'field_flags', {}))  # Make a copy
        validator_flags.update(flags)  # Add new flags
        validator.field_flags = validator_flags  # Add back into validator

    add_flags(wtforms.validators.EqualTo, {'not_solo': True})


_patch_wtforms_add_flags()
del _patch_wtforms_add_flags


def _patch_json_output() -> None:
    """Add __json__ method to Field class."""

    def field_json(self):
        """Render field to a JSON-compatible dictionary."""
        return {
            'name': self.name,
            'type': self.type,
            'data': self._value(),  # skipcq: PYL-W0212
        }

    wtforms.fields.Field.__json__ = field_json


_patch_json_output()
del _patch_json_output
