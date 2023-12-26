"""
WTForms fields and widgets with ParsleyJS headers.

This is a fork of WTForms-ParsleyJS based on
https://github.com/johannes-gehrs/wtforms-parsleyjs and
https://github.com/fuhrysteve/wtforms-parsleyjs. We've forked it into Baseframe because
the upstream repositories appear unmaintained, and from past experience, we'll have
trouble getting patches accepted every time WTForms or ParsleyJS has an update. This
works best for us if we maintain our own fork.

WTForms-ParsleyJS is MIT licensed, while the rest of Baseframe is either BSD (our code)
or various other open source licenses (other third party code).
"""

import copy
import re
import typing as t

from markupsafe import Markup
from wtforms import Field as WTField
from wtforms.fields import (
    BooleanField as _BooleanField,
    DateField as _DateField,
    DecimalField as _DecimalField,
    EmailField as _EmailField,
    FloatField as _FloatField,
    IntegerField as _IntegerField,
    PasswordField as _PasswordField,
    RadioField as _RadioField,
    SelectField as _SelectField,
    StringField as _StringField,
    TelField as _TelField,
    TextAreaField as _TextAreaField,
    URLField as _URLField,
)
from wtforms.validators import (
    URL,
    AnyOf,
    DataRequired,
    Email,
    EqualTo,
    InputRequired,
    IPAddress,
    Length,
    NumberRange,
    Regexp,
)
from wtforms.widgets import (
    CheckboxInput as _CheckboxInput,
    DateInput as _DateInput,
    EmailInput as _EmailInput,
    HiddenInput as _HiddenInput,
    ListWidget as _ListWidget,
    NumberInput as _NumberInput,
    PasswordInput as _PasswordInput,
    Select as _Select,
    TelInput as _TelInput,
    TextArea as _TextArea,
    TextInput as _TextInput,
    URLInput as _URLInput,
    html_params,
)

from .typing import ValidatorCallable

__author__ = 'Johannes Gehrs (jgehrs@gmail.com)'

__all__ = [
    # ParsleyJS helpers
    'parsley_kwargs',
    'ParsleyInputMixin',
    # Widgets
    'TextInput',
    'PasswordInput',
    'HiddenInput',
    'TextArea',
    'CheckboxInput',
    'Select',
    'ListWidget',
    'TelInput',
    'URLInput',
    'EmailInput',
    'DateInput',
    'NumberInput',
    # Fields
    'StringField',
    'IntegerField',
    'RadioField',
    'BooleanField',
    'DecimalField',
    'FloatField',
    'PasswordField',
    'HiddenField',
    'TextAreaField',
    'SelectField',
    'TelField',
    'URLField',
    'EmailField',
    'DateField',
]


def parsley_kwargs(
    field: WTField, kwargs: t.Any, extend: bool = True
) -> t.Dict[str, t.Any]:
    """
    Generate updated kwargs from the validators present for the widget.

    Note that the regex validation relies on the regex pattern being compatible with
    both ECMA script and Python. The regex is not converted in any way.
    It's possible to simply supply your own "parsley-regexp" keyword to the field
    to explicitly provide the ECMA script regex.
    See http://flask.pocoo.org/docs/patterns/wtforms/#forms-in-templates

    Note that the WTForms url validator probably is a bit more liberal than the parsley
    one. Do check if the behaviour suits your needs.
    """
    if extend:
        new_kwargs: t.Dict[str, t.Any] = copy.deepcopy(kwargs)
    else:
        new_kwargs = {}
    for vali in field.validators:
        if isinstance(vali, Email):
            _email_kwargs(new_kwargs, vali)
        elif isinstance(vali, EqualTo):
            _equal_to_kwargs(new_kwargs, vali)
        elif isinstance(vali, IPAddress):
            _ip_address_kwargs(new_kwargs, vali)
        elif isinstance(vali, Length):
            _length_kwargs(new_kwargs, vali)
        elif isinstance(vali, NumberRange):
            _number_range_kwargs(new_kwargs, vali)
        elif isinstance(vali, (DataRequired, InputRequired)):
            _input_required_kwargs(new_kwargs, vali)
        elif isinstance(vali, Regexp) and 'data_regexp' not in new_kwargs:
            _regexp_kwargs(new_kwargs, vali)
        elif isinstance(vali, URL):
            _url_kwargs(new_kwargs, vali)
        elif isinstance(vali, AnyOf):
            _anyof_kwargs(new_kwargs, vali)

        if 'data-parsley-trigger' not in new_kwargs:
            _trigger_kwargs(new_kwargs)

    return new_kwargs


def _email_kwargs(kwargs: t.Dict[str, t.Any], vali: ValidatorCallable) -> None:
    kwargs['data-parsley-type'] = 'email'


def _equal_to_kwargs(kwargs: t.Dict[str, t.Any], vali: EqualTo) -> None:
    kwargs['data-parsley-equalto'] = '#' + vali.fieldname


def _ip_address_kwargs(kwargs: t.Dict[str, t.Any], vali: IPAddress) -> None:
    # Regexp from http://stackoverflow.com/a/4460645
    kwargs['data-parsley-regexp'] = (
        r'^\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b$'
    )


def _length_kwargs(kwargs: t.Dict[str, t.Any], vali: Length) -> None:
    default_number = -1

    if default_number not in (vali.min, vali.max):
        kwargs['minlength'] = str(vali.min)
        kwargs['maxlength'] = str(vali.max)
        kwargs['data-parsley-length'] = '[' + str(vali.min) + ',' + str(vali.max) + ']'
    else:
        if vali.min != default_number:
            kwargs['minlength'] = str(vali.min)
            kwargs['data-parsley-minlength'] = str(vali.min)
        if vali.max != default_number:
            kwargs['maxlength'] = str(vali.max)
            kwargs['data-parsley-maxlength'] = str(vali.max)


def _number_range_kwargs(kwargs: t.Dict[str, t.Any], vali: NumberRange) -> None:
    kwargs['data-parsley-range'] = '[' + str(vali.min) + ',' + str(vali.max) + ']'


def _input_required_kwargs(
    kwargs: t.Dict[str, t.Any], vali: t.Union[InputRequired, DataRequired]
) -> None:
    kwargs['data-parsley-required'] = 'true'
    if vali.message:
        kwargs['data-parsley-required-message'] = vali.message


def _regexp_kwargs(kwargs: t.Dict[str, t.Any], vali: Regexp) -> None:
    if isinstance(vali.regex, re.Pattern):
        # WTForms allows compiled regexps to be passed to the validator, but we need
        # the pattern text
        regex_string = vali.regex.pattern
    else:
        regex_string = vali.regex
    kwargs['data-parsley-regexp'] = regex_string


def _url_kwargs(kwargs: t.Dict[str, t.Any], vali: URL) -> None:
    kwargs['data-parsley-type'] = 'url'


def _string_seq_delimiter(kwargs: t.Dict[str, t.Any], vali: AnyOf) -> str:
    # We normally use a comma as the delimiter - looks clean and it's parsley's default.
    # If the strings for which we check contain a comma, we cannot use it as a
    # delimiter.
    default_delimiter = ','
    fallback_delimiter = ';;;'
    delimiter = default_delimiter
    for value in vali.values:
        if value.find(',') != -1:
            delimiter = fallback_delimiter
            break
    if delimiter != default_delimiter:
        kwargs['data-parsley-inlist-delimiter'] = delimiter
    return delimiter


def _anyof_kwargs(kwargs: t.Dict[str, t.Any], vali: AnyOf) -> None:
    delimiter = _string_seq_delimiter(kwargs, vali)
    kwargs['data-parsley-inlist'] = delimiter.join(vali.values)


def _trigger_kwargs(
    kwargs: t.Dict[str, t.Any], trigger: str = 'change focusout'
) -> None:
    kwargs['data-parsley-trigger'] = trigger


def _message_kwargs(kwargs: t.Dict[str, t.Any], message: str) -> None:
    kwargs['data-parsley-error-message'] = message


class ParsleyInputMixin:
    def __call__(self, field: WTField, **kwargs: t.Any) -> str:
        kwargs = parsley_kwargs(field, kwargs)
        return super().__call__(field, **kwargs)  # type: ignore[misc]


class TextInput(ParsleyInputMixin, _TextInput):
    pass


class PasswordInput(ParsleyInputMixin, _PasswordInput):
    pass


class HiddenInput(ParsleyInputMixin, _HiddenInput):
    pass


class TextArea(ParsleyInputMixin, _TextArea):
    pass


class CheckboxInput(ParsleyInputMixin, _CheckboxInput):
    pass


class TelInput(ParsleyInputMixin, _TelInput):
    pass


class URLInput(ParsleyInputMixin, _URLInput):
    pass


class EmailInput(ParsleyInputMixin, _EmailInput):
    pass


class DateInput(ParsleyInputMixin, _DateInput):
    pass


class NumberInput(ParsleyInputMixin, _NumberInput):
    pass


class Select(ParsleyInputMixin, _Select):
    pass


class ListWidget(_ListWidget):
    def __call__(self, field: WTField, **kwargs: t.Any) -> str:
        sub_kwargs = parsley_kwargs(field, kwargs, extend=False)
        kwargs.setdefault('id', field.id)
        html = [f'<{self.html_tag} {html_params(**kwargs)}>']
        for subfield in field:
            if self.prefix_label:
                html.append(f'<li>{subfield.label} {subfield(**sub_kwargs)}</li>')
            else:
                html.append(f'<li>{subfield(**sub_kwargs)} {subfield.label}</li>')
        html.append(f'</{self.html_tag}>')
        return Markup(''.join(html))


class StringField(_StringField):
    widget = TextInput()


class IntegerField(_IntegerField):
    widget = NumberInput()


class RadioField(_RadioField):
    widget = ListWidget(prefix_label=False)


class BooleanField(_BooleanField):
    widget = CheckboxInput()


class DecimalField(_DecimalField):
    widget = NumberInput()


class FloatField(_FloatField):
    widget = NumberInput()


class PasswordField(_PasswordField):
    widget = PasswordInput()


class HiddenField(_PasswordField):
    widget = HiddenInput()


class TextAreaField(_TextAreaField):
    widget = TextArea()


class SelectField(_SelectField):
    widget = Select()


class TelField(_TelField):
    widget = TelInput()


class URLField(_URLField):
    widget = URLInput()


class EmailField(_EmailField):
    widget = EmailInput()


class DateField(_DateField):
    widget = DateInput()
