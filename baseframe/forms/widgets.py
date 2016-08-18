# -*- coding: utf-8 -*-

import wtforms
from wtforms.compat import text_type
from wtforms.widgets import RadioInput, Select, HTMLString, html_params
from flask import Markup
from .. import b_ as _

__all__ = ['TinyMce3', 'TinyMce4', 'SubmitInput', 'DateTimeInput', 'HiddenInput', 'CoordinatesInput',
    'RadioMatrixInput', 'InlineListWidget', 'RadioInput', 'SelectWidget']


# This class borrowed from https://github.com/industrydive/wtforms_extended_selectfield
class SelectWidget(Select):
    """
    Add support of choices with ``optgroup`` to the ``Select`` widget.
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = True
        html = ['<select %s>' % html_params(name=field.name, **kwargs)]
        for item1, item2 in field.choices:
            if isinstance(item2, (list, tuple)):
                group_label = item1
                group_items = item2
                html.append('<optgroup %s>' % html_params(label=group_label))
                for inner_val, inner_label in group_items:
                    html.append(self.render_option(inner_val, inner_label, inner_val == field.data))
                html.append('</optgroup>')
            else:
                val = item1
                label = item2
                html.append(self.render_option(val, label, val == field.data))
        html.append('</select>')
        return HTMLString(''.join(html))


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
        return Markup(u'<input type="date" class="datetime-date %s" %s /> <input type="text" class="datetime-time %s" %s /> %s' % (
            class_,
            wtforms.widgets.html_params(name=field.name, id=field_id + '-date', value=date_value, **kwargs),
            class_,
            wtforms.widgets.html_params(name=field.name, id=field_id + '-time', value=time_value, **kwargs),
            field.tzname,
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


class InlineListWidget(object):
    """
    Renders a list of fields as buttons.

    This is used for fields which encapsulate many inner fields as subfields.
    The widget will try to iterate the field to get access to the subfields and
    call them to render them.

    If `prefix_label` is set, the subfield's label is printed before the field,
    otherwise afterwards. The latter is useful for iterating radios or
    checkboxes.
    """
    def __init__(self, html_tag='div', class_='', class_prefix=''):
        self.html_tag = html_tag
        self.class_ = ''
        self.class_prefix = class_prefix

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs['class_'] = (kwargs.pop('class_', kwargs.pop('class', '')).strip() + ' ' + self.class_).strip()
        html = ['<%s %s>' % (self.html_tag, wtforms.widgets.html_params(**kwargs))]
        for subfield in field:
            html.append('<label for="%s" class="%s%s">%s %s</label>' % (
                subfield.id, self.class_prefix, subfield.data, subfield(), subfield.label.text))
        html.append('</%s>' % self.html_tag)
        return Markup('\n'.join(html))
