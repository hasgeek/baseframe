"""Redefined WTForms widgets and some extra widgets."""

from __future__ import annotations

import typing as t

from flask import current_app, render_template
from furl import furl
from markupsafe import Markup, escape
from wtforms import Field as WTField
from wtforms.widgets import RadioInput, Select, html_params
import wtforms

from ..extensions import _

__all__ = [
    'TinyMce4',
    'SubmitInput',
    'DateTimeInput',
    'CoordinatesInput',
    'RadioMatrixInput',
    'ImgeeWidget',
    'InlineListWidget',
    'RadioInput',
    'SelectWidget',
    'Select2Widget',
]


# This class borrowed from https://github.com/industrydive/wtforms_extended_selectfield
class SelectWidget(Select):
    """Add support of choices with ``optgroup`` to the ``Select`` widget."""

    def __call__(self, field: WTField, **kwargs: t.Any) -> Markup:
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = True
        html = [f'<select {html_params(name=field.name, **kwargs)}>']
        for item1, item2 in field.choices:
            if isinstance(item2, (list, tuple)):
                group_label = item1
                group_items = item2
                html.append(f'<optgroup {html_params(label=group_label)}>')
                for inner_val, inner_label in group_items:
                    html.append(
                        self.render_option(
                            inner_val,
                            inner_label,
                            field.coerce(inner_val) == field.data,
                        )
                    )
                html.append('</optgroup>')
            else:
                val = item1
                label = item2
                html.append(self.render_option(val, label, val == field.data))
        html.append('</select>')
        return Markup(''.join(html))


class Select2Widget(Select):
    """Add a select2 class to the rendered select widget."""

    def __call__(self, field: WTField, **kwargs: t.Any) -> Markup:
        kwargs.setdefault('id', field.id)
        kwargs.pop('type', field.type)
        if field.multiple:
            kwargs['multiple'] = 'multiple'
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        if c:
            kwargs['class'] = f'select2 {c}'
        else:
            kwargs['class'] = 'select2'
        html = [f'<select {html_params(name=field.name, **kwargs)}>']
        if field.iter_choices():
            for val, label, selected in field.iter_choices():
                html.append(self.render_option(val, label, selected))
        html.append('</select>')
        return Markup(''.join(html))


class TinyMce4(wtforms.widgets.TextArea):
    """Rich text widget with Tiny MCE 4."""

    #: Used as an identifier in forms.html.jinja2
    input_type: str = 'tinymce4'

    def __call__(self, field: WTField, **kwargs: t.Any) -> Markup:
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        if c:
            kwargs['class'] = f'richtext {c}'
        else:
            kwargs['class'] = 'richtext'
        return super().__call__(field, **kwargs)


class SubmitInput(wtforms.widgets.SubmitInput):
    """Submit input with pre-defined classes."""

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        self.css_class = kwargs.pop('class', '') or kwargs.pop('class_', '')
        super().__init__(*args, **kwargs)

    def __call__(self, field: WTField, **kwargs: t.Any) -> Markup:
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = f'{self.css_class} {c}'
        return super().__call__(field, **kwargs)


class DateTimeInput(wtforms.widgets.Input):
    """Render date and time inputs."""

    input_type = 'datetime-local'

    def __call__(self, field: WTField, **kwargs: t.Any) -> Markup:
        kwargs.setdefault('id', field.id)
        field_id = kwargs.pop('id')
        kwargs.pop('type', None)
        value = kwargs.pop('value', None)
        if value is None:  # Allow blank value to override field data
            value = field._value() or ''
        class_ = kwargs.pop('class', kwargs.pop('class_', ''))
        input_attrs = html_params(name=field.name, id=field_id, value=value, **kwargs)
        return Markup(
            f'<input type="datetime-local" class="{class_}"'
            f' {input_attrs} /> {field.tzname}'
        )


class CoordinatesInput(wtforms.widgets.core.Input):
    """Render latitude and longitude coordinates."""

    input_type = 'text'

    def __call__(self, field: WTField, **kwargs: t.Any) -> Markup:
        id_ = kwargs.pop('id', field.id)
        kwargs.setdefault('type', self.input_type)
        kwargs.setdefault('size', 10)  # 9 digits precision and +/- sign
        kwargs.pop(
            'placeholder', None
        )  # Discard placeholder, use custom values for each input below
        value = kwargs.pop('value', None)
        if not value:
            value = field._value()
        if not value:
            value = ['', '']
        elif isinstance(value, str):
            value = value.split(',', 1)
        if len(value) < 2:
            value.append('')

        return Markup(
            # pylint: disable=consider-using-f-string
            '<input {}> <input {}>'.format(
                self.html_params(
                    id=id_ + '_latitude',
                    name=field.name,
                    placeholder=_("Latitude"),
                    value=value[0],
                    **kwargs,
                ),
                self.html_params(
                    id=id_ + '_longitude',
                    name=field.name,
                    placeholder=_("Longitude"),
                    value=value[1],
                    **kwargs,
                ),
            )
        )


class RadioMatrixInput:
    """Render a table with a radio matrix."""

    def __call__(self, field: RadioMatrixField, **kwargs: t.Any) -> Markup:
        rendered = []
        table_class = kwargs.pop('table_class', 'table')
        rendered.append(f'<table class="{escape(table_class)}">')
        rendered.append('<thead>')
        rendered.append('<tr>')
        rendered.append(f'<th>{escape(field.label)}</th>')
        for _value, label in field.choices:
            rendered.append(f'<th>{escape(label)}</th>')
        rendered.append('</th>')
        rendered.append('</thead>')
        rendered.append('<tbody>')
        for name, title in field.fields:
            rendered.append('<tr>')
            rendered.append(f'<td>{escape(title)}</td>')
            selected = field.data.get(name)
            for value, _label in field.choices:
                params: t.Dict[str, t.Any] = {
                    'type': 'radio',
                    'name': name,
                    'value': value,
                }
                if str(selected) == str(value):
                    params['checked'] = True
                rendered.append(f'<td><input {html_params(**params)}/></td>')
            rendered.append('</tr>')
        rendered.append('</tbody>')
        rendered.append('</table>')

        return Markup('\n'.join(rendered))


class InlineListWidget:
    """
    Renders a list of fields as buttons.

    This is used for fields which encapsulate many inner fields as subfields.
    The widget will try to iterate the field to get access to the subfields and
    call them to render them.

    If `prefix_label` is set, the subfield's label is printed before the field,
    otherwise afterwards. The latter is useful for iterating radios or
    checkboxes.
    """

    def __init__(
        self,
        html_tag: str = 'div',
        class_: str = '',
        class_prefix: str = '',
    ) -> None:
        self.html_tag = html_tag
        self.class_ = class_
        self.class_prefix = class_prefix

    def __call__(self, field: WTField, **kwargs: t.Any) -> Markup:
        kwargs.setdefault('id', field.id)
        kwargs['class_'] = (
            kwargs.pop('class_', kwargs.pop('class', '')).strip() + ' ' + self.class_
        ).strip()
        html = [f'<{escape(self.html_tag)} {html_params(**kwargs)}>']
        for subfield in field:
            html.append(
                f'<label for="{escape(subfield.id)}" class="{escape(self.class_prefix)}'
                f'{escape(subfield.data)}">{escape(subfield())}'
                f' {escape(subfield.label.text)}</label>'
            )
        html.append(f'</{escape(self.html_tag)}>')
        return Markup('\n'.join(html))


class ImgeeWidget(wtforms.widgets.Input):
    input_type = 'hidden'

    def __call__(self, field: WTField, **kwargs: t.Any) -> Markup:
        id_ = kwargs.pop('id', field.id)
        kwargs.setdefault('type', self.input_type)
        imgee_host = current_app.config.get('IMGEE_HOST')
        if not imgee_host:
            raise ValueError("No imgee server specified in config variable IMGEE_HOST")

        upload_url = f'{imgee_host}/{field.profile}/popup'

        value = kwargs.pop('value', None)
        if not value:
            value = field._value()
        if not value:
            value = ''
        elif isinstance(value, furl):
            value = furl.url

        # pylint: disable=consider-using-f-string
        iframe_html = Markup(
            '<iframe {} class="imgee-upload"></iframe>'.format(
                self.html_params(
                    id='iframe_' + id_ + '_upload',
                    input_id=id_,
                    src=upload_url,
                ),
            )
        )

        field_html = Markup(
            '<img {}> <input {}>'.format(
                self.html_params(id='img_' + id_, src=value, width='200', **kwargs),
                self.html_params(
                    id=id_,
                    name=field.name,
                    placeholder=_("Image URL"),
                    value=value,
                    **kwargs,
                ),
            )
        )

        return Markup(
            render_template(
                'baseframe/mui/imgeefield.html.jinja2',
                field=field,
                iframe_html=iframe_html,
                field_html=field_html,
            )
        )


if t.TYPE_CHECKING:
    from .fields import RadioMatrixField
