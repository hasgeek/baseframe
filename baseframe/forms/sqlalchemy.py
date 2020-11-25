"""
SQLAlchemy-based form fields and widgets
"""

from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

from .. import b__ as __
from .validators import StopValidation

__all__ = ['AvailableName', 'QuerySelectField', 'QuerySelectMultipleField']


class AvailableAttr(object):
    """
    Validator to check whether the specified attribute is available
    for the model being edited.
    """

    def __init__(self, attr, message=None, model=None):
        self.model = model
        self.attr = attr
        if not message:
            message = __("This {attr} is already in use".format(attr=attr))
        self.message = message

    def __call__(self, form, field):
        model = self.model or form.edit_model
        if not model:
            raise TypeError(
                "Either the validator or the form MUST be linked to a model"
            )
        if hasattr(model, 'parent'):
            scoped = True
        else:
            scoped = False
        if model:
            query = model.query.filter(getattr(model, self.attr) == field.data)
            if form.edit_id:
                query = query.filter(model.id != form.edit_id)
            if scoped:
                query = query.filter_by(parent=form.edit_parent)
            if query.notempty():
                raise StopValidation(self.message)


class AvailableName(AvailableAttr):
    """
    Validator to check whether the specified name is available
    for the model being edited.
    """

    def __init__(self, message=None, model=None):
        if not message:
            message = __("This URL name is already in use")
        super(AvailableName, self).__init__('name', message, model)
