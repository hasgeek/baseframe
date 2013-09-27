# -*- coding: utf-8 -*-

"""
SQLAlchemy-based form fields and widgets
"""

import wtforms
from coaster.sqlalchemy import MarkdownComposite
from .. import b__ as __

__all__ = ['AvailableName', 'MarkdownField']


class AvailableName(object):
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
            existing = query.first()
            if existing:
                raise wtforms.ValidationError(self.message)


class MarkdownField(wtforms.TextAreaField):
    """
    TextArea field, which has class='markdown' and
    whose contents are transformed into a MarkdownComposite obj.
    """
    def __call__(self, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = "%s %s" % (c, 'markdown')
        return super(MarkdownField, self).__call__(**kwargs)

    def populate_obj(self, obj, name):
        md = MarkdownComposite(self.data)
        setattr(obj, name, md)
