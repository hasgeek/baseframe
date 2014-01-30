# -*- coding: utf-8 -*-

"""
Baseframe forms
"""

from flask import render_template, request, Markup, abort, flash, redirect, escape, url_for, make_response
import wtforms
from flask.ext.wtf import Form as BaseForm
from .. import b__ as __
from ..signals import form_validation_error, form_validation_success

from .fields import *
from .widgets import *
from .validators import *
# SQLAlchemy-based fields/widgets/validators are not automatically imported here


class Form(BaseForm):
    """
    Form with additional methods.
    """
    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        # Make editing objects easier
        self.edit_obj = kwargs.get('obj')
        self.edit_model = kwargs.get('model')
        self.edit_parent = kwargs.get('parent')
        if self.edit_obj:
            if hasattr(self.edit_obj, 'id'):
                self.edit_id = self.edit_obj.id
            else:
                self.edit_id = None
            if not self.edit_model:
                self.edit_model = self.edit_obj.__class__
            if not self.edit_parent and hasattr(self.edit_obj, 'parent'):
                self.edit_parent = self.edit_obj.parent
        else:
            self.edit_id = None

    def validate(self):
        result = super(Form, self).validate()
        if self.errors:
            form_validation_error.send(self)
        else:
            form_validation_success.send(self)
        return result


class ConfirmDeleteForm(Form):
    """
    Confirm a delete operation
    """
    # The labels on these widgets are not used. See delete.html.
    delete = wtforms.fields.SubmitField(__(u"Delete"))
    cancel = wtforms.fields.SubmitField(__(u"Cancel"))


def render_form(form, title, message='', formid='form', submit=__(u"Submit"), cancel_url=None, ajax=False):
    multipart = False
    for field in form:
        if isinstance(field.widget, wtforms.widgets.FileInput):
            multipart = True
    if request.is_xhr and ajax:
        return make_response(render_template('baseframe/ajaxform.html', form=form, title=title,
            message=message, formid=formid, submit=submit,
            cancel_url=cancel_url, multipart=multipart))
    else:
        return make_response(render_template('baseframe/autoform.html', form=form, title=title,
            message=message, formid=formid, submit=submit,
            cancel_url=cancel_url, ajax=ajax, multipart=multipart))


def render_message(title, message, code=200):
    if request.is_xhr:
        return make_response(Markup("<p>%s</p>" % escape(message)), code)
    else:
        return make_response(render_template('baseframe/message.html', title=title, message=message), code)


def render_redirect(url, code=302):
    if request.is_xhr:
        return make_response(render_template('baseframe/redirect.html', url=url))
    else:
        return redirect(url, code=code)


def render_delete_sqla(obj, db, title, message, success=u'', next=None, cancel_url=None):
    if not obj:
        abort(404)
    form = ConfirmDeleteForm()
    if request.method in ('POST', 'DELETE') and form.validate():
        if 'delete' in request.form or request.method == 'DELETE':
            db.session.delete(obj)
            db.session.commit()
            if success:
                flash(success, 'success')
            return render_redirect(next or url_for('index'), code=303)
        else:
            return render_redirect(cancel_url or next or url_for('index'), code=303)
    return make_response(render_template('baseframe/delete.html', form=form, title=title, message=message))
