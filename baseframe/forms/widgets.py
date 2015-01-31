# -*- coding: utf-8 -*-

import wtforms
from wtforms.compat import text_type
from flask import Markup
from .. import b_ as _

__all__ = ['TinyMce3', 'TinyMce4', 'SubmitInput', 'DateTimeInput', 'HiddenInput', 'CoordinatesInput',
    'RadioMatrixInput']


class TinyMce3(wtforms.widgets.TextArea):
    """
    Rich text widget with Tiny MCE 3.
    """
    input_type = "tinymce3"

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        if c:
            kwargs['class'] = u'%s %s' % ('richtext', c)
        else:
            kwargs['class'] = 'richtext'
        return super(TinyMce3, self).__call__(field, **kwargs)


class TinyMce4(wtforms.widgets.TextArea):
    """
    Rich text widget with Tiny MCE 4.
    """
    input_type = "tinymce4"

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        if c:
            kwargs['class'] = u'%s %s' % ('richtext', c)
        else:
            kwargs['class'] = 'richtext'
        return super(TinyMce4, self).__call__(field, **kwargs)


class SubmitInput(wtforms.widgets.SubmitInput):
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


class DateTimeInput(wtforms.widgets.Input):
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
        class_ = kwargs.pop('class', kwargs.pop('class_', ''))
        date_value, time_value = value.split(' ', 1)
        return Markup(u'<input type="text" class="datetime-date %s" data-datepicker="datepicker" %s /> <input type="text" class="datetime-time %s" %s />' % (
            class_,
            wtforms.widgets.html_params(name=field.name, id=field_id + '-date', value=date_value, **kwargs),
            class_,
            wtforms.widgets.html_params(name=field.name, id=field_id + '-time', value=time_value, **kwargs)
            ))


class HiddenInput(wtforms.widgets.core.Input):
    """
    Render a hidden input. This widget exists solely to escape processing by form.hidden_tag()
    """
    input_type = 'hidden'


class CoordinatesInput(wtforms.widgets.core.Input):
    """
    Render latitude and longitude coordinates
    """
    input_type = 'text'

    def __call__(self, field, **kwargs):
        id_ = kwargs.pop('id', field.id)
        kwargs.setdefault('type', self.input_type)
        kwargs.setdefault('size', 10)  # 9 digits precision and +/- sign
        kwargs.pop('placeholder', None)  # Discard placeholder, use custom values for each input below
        value = kwargs.pop('value', None)
        if not value:
            value = field._value()
        if not value:
            value = ['', '']
        elif isinstance(value, basestring):
            value = value.split(',', 1)
        if len(value) < 2:
            value.append('')

        return Markup('<input %s> <input %s>' % (
            self.html_params(id=id_ + '_latitude', name=field.name, placeholder=_("Latitude"),
                value=value[0], **kwargs),
            self.html_params(id=id_ + '_longitude', name=field.name, placeholder=_("Longitude"),
                value=value[1], **kwargs)))


class RadioMatrixInput(object):
    """
    Render a table with a radio matrix
    """

    def __call__(self, field, **kwargs):

        rendered = []
        rendered.append('<table class="%s">' % kwargs.pop('table_class', 'table'))
        rendered.append('<thead>')
        rendered.append('<tr>')
        rendered.append('<th>%s</th>' % field.label)
        for value, label in field.choices:
            rendered.append('<th>%s</th>' % label)
        rendered.append('</th>')
        rendered.append('</thead>')
        rendered.append('<tbody>')
        for name, title in field.fields:
            rendered.append('<tr>')
            rendered.append('<td>%s</td>' % title)
            selected = field.data.get(name)
            for value, label in field.choices:
                params = {'type': 'radio', 'name': name, 'value': value}
                if text_type(selected) == text_type(value):
                    params['checked'] = True
                rendered.append('<td><input %s/></td>' % wtforms.widgets.html_params(**params))
            rendered.append('</tr>')
        rendered.append('</tbody>')
        rendered.append('</table>')

        return Markup('\n'.join(rendered))
