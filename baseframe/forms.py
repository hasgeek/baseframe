# -*- coding: utf-8 -*-

"""
Standard forms
"""

from pytz import utc, timezone as pytz_timezone
import bleach
import dns.resolver
from flask import render_template, request, Markup, abort, flash, redirect, json, escape, url_for, make_response
from wtforms.widgets import html_params
import flask.ext.wtf as wtf
from coaster import make_name, get_email_domain
from . import b__ as __


class ValidEmailDomain(object):
    message_domain = __(u"This domain does not exist")
    message_email = __(u"This email address does not exist")

    def __init__(self, message=None, message_domain=None, message_email=None):
        self.message = message
        if message_domain:
            self.message_domain = message_domain
        if message_email:
            self.message_email = message_email

    def __call__(self, form, field):
        email_domain = get_email_domain(field.data)
        try:
            dns.resolver.query(email_domain, 'MX')
        except dns.resolver.NXDOMAIN:
            raise wtf.ValidationError(self.message or self.message_domain)
        except dns.resolver.NoAnswer:
            raise wtf.ValidationError(self.message or self.message_email)
        except (dns.resolver.Timeout, dns.resolver.NoNameservers):
            pass


class RichText(wtf.widgets.TextArea):
    """
    Rich text widget.
    """
    input_type = "tinymce"

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        if c:
            kwargs['class'] = u'%s %s' % ('richtext', c)
        else:
            kwargs['class'] = 'richtext'
        return super(RichText, self).__call__(field, **kwargs)


class SubmitInput(wtf.widgets.SubmitInput):
    """
    Submit input with pre-defined classes.
    """
    def __init__(self, *args, **kwargs):
        self.css_class = kwargs.pop('class', '') or kwargs.pop('class_', '')
        super(SubmitInput, self).__init__(*args, **kwargs)

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % (self.css_class, c)
        return super(SubmitInput, self).__call__(field, **kwargs)


class DateTimeInput(wtf.widgets.Input):
    """
    Render date and time inputs.
    """
    input_type = 'datetime'

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        field_id = kwargs.pop('id')
        kwargs.pop('type', None)
        value = kwargs.pop('value', None)
        if value is None:
            value = field._value()
        if not value:
            value = ' '
        date_value, time_value = value.split(' ', 1)
        return Markup(u'<input type="text" class="datetime-date" data-datepicker="datepicker" %s /> <input type="text" class="datetime-time" %s />' % (
            html_params(name=field.name, id=field_id + '-date', value=date_value, **kwargs),
            html_params(name=field.name, id=field_id + '-time', value=time_value, **kwargs)
            ))


class RichTextField(wtf.fields.TextAreaField):
    """
    Rich text field.
    """
    widget = RichText()

    # TODO: Accept valid_tags as a init parameter
    def __init__(self,
            # WTForms fields
            label=u'',
            validators=None,
            filters=(),
            description=u'',
            id=None,
            default=None,
            widget=None,
            _form=None,
            _name=None,
            _prefix='',

            # Additional fields
            content_css=None,
            linkify=True, nofollow=True,
            tinymce_options=None,
            sanitize_tags=None, sanitize_attributes=None, **kwargs):

        super(RichTextField, self).__init__(label=label, validators=validators, filters=filters,
            description=description, id=id, default=default, widget=widget, _form=_form, _name=_name,
            _prefix=_prefix, **kwargs)

        if tinymce_options is None:
            tinymce_options = {}
        else:
            # Clone the dict to preserve local edits
            tinymce_options = dict(tinymce_options)

        # Set defaults for TinyMCE
        tinymce_options.setdefault('theme', "advanced")
        tinymce_options.setdefault('plugins', "")
        tinymce_options.setdefault('theme_advanced_buttons1',
            "bold,italic,|,sup,sub,|,bullist,numlist,|,link,unlink,|,blockquote,|,removeformat,code")
        tinymce_options.setdefault('theme_advanced_buttons2', "")
        tinymce_options.setdefault('theme_advanced_buttons3', "")
        tinymce_options.setdefault('blockformats', "p,h3,h4,h5,h6,blockquote,dt,dd")
        tinymce_options.setdefault('width', "100%")
        tinymce_options.setdefault('height', "159")
        tinymce_options.setdefault('valid_elements',
            "p,br,strong/b,em/i,sup,sub,h3,h4,h5,h6,ul,ol,li,a[!href|title|target],blockquote,code")
        tinymce_options.setdefault('theme_advanced_toolbar_location', "top")
        tinymce_options.setdefault('theme_advanced_toolbar_align', "left")
        tinymce_options.setdefault('theme_advanced_statusbar_location', "bottom")
        tinymce_options.setdefault('theme_advanced_resizing', True)
        tinymce_options.setdefault('theme_advanced_path', False)
        tinymce_options.setdefault('relative_urls', False)

        # Remove options that cannot be set by callers
        tinymce_options.pop('content_css', None)
        tinymce_options.pop('script_url', None)
        tinymce_options.pop('setup', None)

        if sanitize_tags is None:
            sanitize_tags = ['p', 'br', 'strong', 'em', 'sup', 'sub', 'h3', 'h4', 'h5', 'h6',
                'ul', 'ol', 'li', 'a', 'blockquote', 'code']
        if sanitize_attributes is None:
            sanitize_attributes = {'a': ['href', 'title', 'target']}

        self.linkify = linkify
        self.nofollow = nofollow
        self.tinymce_options = tinymce_options

        self.content_css = content_css
        self.sanitize_tags = sanitize_tags
        self.sanitize_attributes = sanitize_attributes

    def tinymce_options_json(self):
        return [(Markup(json.dumps(k)), Markup(json.dumps(v))) for k, v in self.tinymce_options.items()]

    def process_formdata(self, valuelist):
        super(RichTextField, self).process_formdata(valuelist)
        # Sanitize data
        self.data = bleach.clean(self.data,
            tags=self.sanitize_tags,
            attributes=self.sanitize_attributes)
        if self.linkify:
            if self.nofollow:
                self.data = bleach.linkify(self.data)
            else:
                self.data = bleach.linkify(self.data, callbacks=[])


class DateTimeField(wtf.fields.DateTimeField):
    """
    A text field which stores a `datetime.datetime` matching a format.
    """
    widget = DateTimeInput()

    def __init__(self, label=None, validators=None,
            format='%Y-%m-%d %I:%M%p', timezone=None, **kwargs):
        super(DateTimeField, self).__init__(label, validators, **kwargs)
        self.format = format
        self.timezone = timezone
        if timezone:
            self.tz = pytz_timezone(timezone)
        else:
            self.tz = utc

    def _value(self):
        if self.data:
            if self.timezone:
                if self.data.tzinfo is None:
                    data = utc.localize(self.data).astimezone(self.tz)
                else:
                    data = self.data.astimezone(self.tz)
            else:
                data = self.data
            value = data.strftime(self.format)
        else:
            value = ''
        return value

    def process_formdata(self, valuelist):
        super(DateTimeField, self).process_formdata(valuelist)
        if self.timezone:
            # Convert from user timezone back to UTC, then discard tzinfo
            self.data = self.tz.localize(self.data).astimezone(utc).replace(tzinfo=None)


class HiddenMultiField(wtf.fields.TextField):
    """
    A hidden field that stores multiple comma-separated values, meant to be
    used as an Ajax widget target. The optional ``separator`` parameter
    can be used to specify an alternate separator character (default ``','``).
    """
    widget = wtf.HiddenInput()

    def __init__(self, *args, **kwargs):
        self.separator = kwargs.pop('separator', ',')
        super(HiddenMultiField, self).__init__(*args, **kwargs)

    def _value(self):
        if self.data:
            return self.separator.join(self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        super(HiddenMultiField, self).process_formdata(valuelist)
        if not self.data:
            self.data = []  # Calling ''.split(',') will give us [''] which is not "falsy"
        else:
            self.data = self.data.split(self.separator)


class Form(wtf.Form):
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
            self.edit_id = self.edit_obj.id
            if not self.edit_model:
                self.edit_model = self.edit_obj.__class__
            if not self.edit_parent and hasattr(self.edit_obj, 'parent'):
                self.edit_parent = self.edit_obj.parent
        else:
            self.edit_id = None


class ValidName(object):
    def __init__(self, message=None):
        if not message:
            message = __("Name contains unsupported characters")
        self.message = message

    def __call__(self, form, field):
        if make_name(field.data) != field.data:
            raise wtf.ValidationError(self.message)


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
                raise wtf.ValidationError(self.message)


class ConfirmDeleteForm(Form):
    """
    Confirm a delete operation
    """
    # The labels on these widgets are not used. See delete.html.
    delete = wtf.SubmitField(__(u"Delete"))
    cancel = wtf.SubmitField(__(u"Cancel"))


def render_form(form, title, message='', formid='form', submit=__(u"Submit"), cancel_url=None, ajax=False):
    multipart = False
    for field in form:
        if isinstance(field.widget, wtf.FileInput):
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
        return make_response(render_template('baseframe/redirect.html', quoted_url=Markup(json.dumps(url))))
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
            return render_redirect(next or url_for('index'))
        else:
            return render_redirect(cancel_url or next or url_for('index'))
    return make_response(render_template('baseframe/delete.html', form=form, title=title, message=message))
