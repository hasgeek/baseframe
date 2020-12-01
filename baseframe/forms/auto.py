from typing import Optional, Tuple, Union

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
from werkzeug.wrappers import Response
import wtforms

from coaster.utils import buid

from ..blueprint import THEME_FILES
from ..extensions import __
from ..utils import request_is_xhr
from .fields import SubmitField
from .form import Form


class ConfirmDeleteForm(Form):
    """Confirm a delete operation."""

    # The labels on these widgets are not used. See delete.html.
    delete = SubmitField(__("Delete"))
    cancel = SubmitField(__("Cancel"))


def render_form(
    form: Form,
    title: str,
    message: str = '',
    formid: Optional[str] = None,
    submit: str = __("Submit"),
    cancel_url: Optional[str] = None,
    ajax: bool = False,
    with_chrome: bool = True,
    action: Optional[str] = None,
    autosave: bool = False,
    draft_revision: bool = None,
    template: str = '',
) -> Union[str, Tuple[str, int], Response]:  # TODO: Use ReturnView
    """Render a form."""
    multipart = False
    ref_id = 'form-' + (formid or buid())
    if not action:
        action = request.url
    for field in form:
        if isinstance(field.widget, wtforms.widgets.FileInput):
            multipart = True
    if not with_chrome:
        if not template:
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
    if not template and request_is_xhr() and ajax:
        template = THEME_FILES[current_app.config['theme']]['ajaxform.html.jinja2']
    elif not template:
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


def render_message(title: str, message: str, code: int = 200) -> Response:
    """Render a message."""
    template = THEME_FILES[current_app.config['theme']]['message.html.jinja2']
    if request_is_xhr():
        return make_response(Markup("<p>%s</p>" % escape(message)), code)
    else:
        return make_response(
            render_template(template, title=title, message=message), code
        )


def render_redirect(url: str, code: int = 302) -> Response:
    """Render a redirect, using a JS redirect for XHR requests, HTTP otherwise."""
    template = THEME_FILES[current_app.config['theme']]['redirect.html.jinja2']
    if request_is_xhr():
        return make_response(render_template(template, url=url))
    else:
        return redirect(url, code=code)


def render_delete_sqla(
    obj,
    db,
    title: str,
    message: str,
    success: str = '',
    next: Optional[str] = None,  # NOQA: A002
    cancel_url: Optional[str] = None,
    delete_text: Optional[str] = None,
    cancel_text: Optional[str] = None,
) -> Response:
    """Render a delete page for SQLAlchemy objects."""
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
