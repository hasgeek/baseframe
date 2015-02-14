# -*- coding: utf-8 -*-

"""
SQLAlchemy-based form fields and widgets
"""

from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from .. import b__ as __
from .validators import StopValidation

__all__ = ['AvailableName', 'QuerySelectField', 'QuerySelectMultipleField']


class AvailableName(object):
    """
    Validator to check whether the specified name is available
    for the model being edited.
    """
    def __init__(self, message=None, model=None):
        self.model = model
        if not message:
            message = __("This URL name is already in use")
        self.message = message

    def __call__(self, form, field):
        model = self.model or form.edit_model
        if hasattr(model, 'parent'):
            scoped = True
        else:
            scoped = False
        if model:
            query = model.query.filter_by(name=field.data)
            if form.edit_id:
                query = query.filter(model.id != form.edit_id)
            if scoped:
                query = query.filter_by(parent=form.edit_parent)
            if query.notempty():
                raise StopValidation(self.message)
