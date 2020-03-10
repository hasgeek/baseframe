# -*- coding: utf-8 -*-

from flask import (
    Markup,
    abort,
    current_app,
    escape,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
import wtforms

from coaster.utils import buid

from .. import THEME_FILES
from .. import b__ as __
from .. import request_is_xhr
from .fields import SubmitField
from .form import Form


class ConfirmDeleteForm(Form):
    """
    Confirm a delete operation
    """

    # The labels on these widgets are not used. See delete.html.
    delete = SubmitField(__(u"Delete"))
    cancel = SubmitField(__(u"Cancel"))


def render_form(
    form,
    title,
    message='',
    formid=None,
    submit=__(u"Submit"),
    cancel_url=None,
    ajax=False,
    with_chrome=True,
    action=None,
    autosave=False,
    draft_revision=None,
):
    multipart = False
    ref_id = 'form-' + (formid or buid())
    if not action:
        action = request.url
    for field in form:
        if isinstance(field.widget, wtforms.widgets.FileInput):
            multipart = True
    if not with_chrome:
        template = THEME_FILES[current_app.config['theme']]['ajaxform.html.jinja2']
        return render_template(
            template,
            form=form,
            title=title,
            message=message,
            formid=formid,
            ref_id=ref_id,
            action=action,
            submit=submit,
            cancel_url=cancel_url,
            ajax=ajax,
            multipart=multipart,
            with_chrome=with_chrome,
            autosave=autosave,
            draft_revision=draft_revision,
        )
    if request_is_xhr() and ajax:
        template = THEME_FILES[current_app.config['theme']]['ajaxform.html.jinja2']
    else:
        template = THEME_FILES[current_app.config['theme']]['autoform.html.jinja2']
    return make_response(
        render_template(
            template,
            form=form,
            title=title,
            message=message,
            formid=formid,
            ref_id=ref_id,
            action=action,
            submit=submit,
            cancel_url=cancel_url,
            ajax=ajax,
            multipart=multipart,
            autosave=autosave,
            draft_revision=draft_revision,
        ),
        200,
    )


def render_message(title, message, code=200):
    template = THEME_FILES[current_app.config['theme']]['message.html.jinja2']
    if request_is_xhr():
        return make_response(Markup("<p>%s</p>" % escape(message)), code)
    else:
        return make_response(
            render_template(template, title=title, message=message), code
        )


def render_redirect(url, code=302):
    template = THEME_FILES[current_app.config['theme']]['redirect.html.jinja2']
    if request_is_xhr():
        return make_response(render_template(template, url=url))
    else:
        return redirect(url, code=code)


def render_delete_sqla(
    obj,
    db,
    title,
    message,
    success=u'',
    next=None,  # NOQA: A002
    cancel_url=None,
    delete_text=None,
    cancel_text=None,
):
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
    template = THEME_FILES[current_app.config['theme']]['delete.html.jinja2']
    return make_response(
        render_template(
            template,
            form=form,
            title=title,
            message=message,
            delete_text=delete_text,
            cancel_text=cancel_text,
        )
    )
