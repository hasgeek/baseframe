"""SQLAlchemy-based form fields and widgets."""

import typing as t

from wtforms import Field as WTField
from wtforms import Form as WTForm
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

from ..extensions import __
from .validators import StopValidation

__all__ = [
    'AvailableAttr',
    'AvailableName',
    'QuerySelectField',
    'QuerySelectMultipleField',
]


class AvailableAttr:
    """Check whether the specified attribute is available for the model being edited."""

    def __init__(
        self, attr: str, message: t.Optional[str] = None, model: t.Any = None
    ) -> None:
        self.model = model
        self.attr = attr
        if not message:
            message = __(f"This {attr} is already in use")
        self.message = message

    def __call__(self, form: WTForm, field: WTField) -> None:
        model = self.model or form.edit_model
        if not model:
            raise TypeError(
                "Either the validator or the form MUST be linked to a model"
            )
        scoped = hasattr(model, 'parent')
        if model:
            query = model.query.filter(getattr(model, self.attr) == field.data)
            if form.edit_id:
                query = query.filter(model.id != form.edit_id)
            if scoped:
                query = query.filter_by(parent=form.edit_parent)
            if query.notempty():
                raise StopValidation(self.message)


class AvailableName(AvailableAttr):
    """Check whether the specified name is available for the model being edited."""

    def __init__(self, message: t.Optional[str] = None, model: t.Any = None) -> None:
        if not message:
            message = __("This URL name is already in use")
        super().__init__('name', message, model)
