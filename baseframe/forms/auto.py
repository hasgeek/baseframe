# -*- coding: utf-8 -*-

import wtforms
from flask import render_template, request, Markup, abort, flash, redirect, escape, url_for, make_response, current_app, jsonify
from .. import b__ as __
from .. import b_ as _
from .. import THEME_FILES
from .form import Form
from .fields import SubmitField


class ConfirmDeleteForm(Form):
    """
    Confirm a delete operation
    """
    # The labels on these widgets are not used. See delete.html.
    delete = SubmitField(__(u"Delete"))
    cancel = SubmitField(__(u"Cancel"))


def render_form(form, title, message='', formid='form', submit=__(u"Submit"), cancel_url=None, ajax=False, with_chrome=True):
    multipart = False
    for field in form:
        if isinstance(field.widget, wtforms.widgets.FileInput):
            multipart = True
    if form.errors:
        # TODO: Why is this 200?
        code = 200  # 400
    else:
        code = 200
    if request.is_xhr and ajax:
        template = THEME_FILES[current_app.config['theme']]['ajaxform.html.jinja2']
    else:
        if with_chrome:
            template = THEME_FILES[current_app.config['theme']]['autoform.html.jinja2']
            return make_response(render_template(template, form=form, title=title,
            message=message, formid=formid, submit=submit,
            cancel_url=cancel_url, ajax=ajax, multipart=multipart), code)
        template = THEME_FILES[current_app.config['theme']]['autoform_xhr.html.jinja2']
        return render_template(template, form=form, title=title,
            message=message, formid=formid, submit=submit,
            cancel_url=cancel_url, ajax=ajax, multipart=multipart)


def render_message(title, message, code=200):
    template = THEME_FILES[current_app.config['theme']]['message.html.jinja2']
    if request.is_xhr:
        return make_response(Markup("<p>%s</p>" % escape(message)), code)
    else:
        return make_response(render_template(template, title=title, message=message), code)


def render_redirect(url, code=302):
    template = THEME_FILES[current_app.config['theme']]['redirect.html.jinja2']
    if request.is_xhr:
        return make_response(render_template(template, url=url))
    else:
        return redirect(url, code=code)


def render_delete_sqla(obj, db, title, message, success=u'', next=None, cancel_url=None, with_response=True):
    if not obj:
        abort(404)
    form = ConfirmDeleteForm()
    if request.method in ('POST', 'DELETE') and form.validate():
        print ('form', request.form)
        if 'delete' in request.form or request.method == 'DELETE':
            db.session.delete(obj)
            db.session.commit()
            if success:
                flash(success, 'success')
            if request.is_xhr:
                return make_response(jsonify(status='ok', doc=_(u"Deleted"), result={'url': next or url_for('index')}), 303)
            return render_redirect(next or url_for('index'), code=303)
        else:
            if request.is_xhr:
                return make_response(jsonify(status='ok', doc=_(u"Cancel"), result={'url': cancel_url or next or url_for('index')}), 303)
            return render_redirect(cancel_url or next or url_for('index'), code=303)
    if with_response:
        template = THEME_FILES[current_app.config['theme']]['delete.html.jinja2']
        return make_response(render_template(template, form=form, title=title, message=message))
    template = THEME_FILES[current_app.config['theme']]['delete_template.html.jinja2']
    return render_template(template, form=form, title=title, message=message)
