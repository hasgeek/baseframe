# -*- coding: utf-8 -*-

"""
SQLAlchemy-based form fields and widgets
"""

import wtforms
from .. import b__ as __

__all__ = ['AvailableName']


class AvailableName(object):
    """
    Validator to check whether the specified name is available
    for the model being edited.
    """
    def __init__(self, message=None, scoped=False):
        self.scoped = scoped
        if not message:
            message = __("That URL name is already in use")
        self.message = message

    def __call__(self, form, field):
        if form.edit_model:
            query = form.edit_model.query.filter_by(name=field.data)
            if form.edit_id:
                query = query.filter(form.edit_model.id != form.edit_id)
            if self.scoped:
                query = query.filter_by(parent=form.edit_parent)
            existing = query.count()
            if existing:
                raise wtforms.validators.StopValidation(self.message)
