"""
WTForms fields and widgets with ParsleyJS headers. This is a fork of wtforms-parsleyjs
based on https://github.com/johannes-gehrs/wtforms-parsleyjs and
https://github.com/fuhrysteve/wtforms-parsleyjs. We've forked it into Baseframe because
the upstream repositories appear unmaintained, and from past experience, we'll have trouble
getting patches accepted every time WTForms or ParsleyJS has an update. This works best for
us if we maintain our own fork.

wtforms-parsleysj is MIT licensed, while the rest of Baseframe is either BSD (our code) or
various other open source licenses (other third party code).
"""

__author__ = 'Johannes Gehrs (jgehrs@gmail.com)'

import re
import copy

from wtforms.validators import (Length, NumberRange, Email, EqualTo, IPAddress,
    Regexp, URL, AnyOf)
try:
    from wtforms.validators import DataRequired
except ImportError:
    # wtforms < 2.x
    from wtforms.validators import Required as DataRequired

from wtforms.widgets import (TextInput as _TextInput, PasswordInput as _PasswordInput,
    CheckboxInput as _CheckboxInput, Select as _Select, TextArea as _TextArea,
    ListWidget as _ListWidget, HiddenInput as _HiddenInput, Input)
from wtforms.widgets.html5 import (TelInput as _TelInput, URLInput as _URLInput, EmailInput as _EmailInput,
    DateInput as _DateInput, NumberInput as _NumberInput)
from wtforms.fields import (StringField as _StringField, BooleanField as _BooleanField,
    DecimalField as _DecimalField, IntegerField as _IntegerField,
    FloatField as _FloatField, PasswordField as _PasswordField,
    SelectField as _SelectField, TextAreaField as _TextAreaField,
    RadioField as _RadioField)
from wtforms.fields.html5 import (URLField as _URLField, EmailField as _EmailField, TelField as _TelField,
    DateField as _DateField)


__all__ = [
    # ParsleyJS helpers
    'parsley_kwargs', 'ParsleyInputMixin',
    # Widgets
    'TextInput', 'PasswordInput', 'HiddenInput', 'TextArea', 'CheckboxInput', 'Select', 'ListWidget',
    'TelInput', 'URLInput', 'EmailInput', 'DateInput', 'NumberInput',
    # Fields
    'StringField', 'IntegerField', 'RadioField', 'BooleanField', 'DecimalField', 'FloatField', 'PasswordField',
    'HiddenField', 'TextAreaField', 'SelectField', 'TelField', 'URLField', 'EmailField', 'DateField']


def parsley_kwargs(field, kwargs):
    """
    Return new *kwargs* for *widget*.

    Generate *kwargs* from the validators present for the widget.

    Note that the regex validation relies on the regex pattern being compatible with
    both ECMA script and Python. The regex is not converted in any way.
    It's possible to simply supply your own "parsley-regexp" keyword to the field
    to explicitly provide the ECMA script regex.
    See http://flask.pocoo.org/docs/patterns/wtforms/#forms-in-templates

    Note that the WTForms url validator probably is a bit more liberal than the parsley
    one. Do check if the behaviour suits your needs.
    """
    new_kwargs = copy.deepcopy(kwargs)
    for vali in field.validators:
        copy_message = True
        if isinstance(vali, Email):
            _email_kwargs(new_kwargs)
        elif isinstance(vali, EqualTo):
            _equal_to_kwargs(new_kwargs, vali)
        elif isinstance(vali, IPAddress):
            _ip_address_kwargs(new_kwargs)
        elif isinstance(vali, Length):
            _length_kwargs(new_kwargs, vali)
        elif isinstance(vali, NumberRange):
            _number_range_kwargs(new_kwargs, vali)
        elif isinstance(vali, DataRequired):
            _input_required_kwargs(new_kwargs)
            _trigger_kwargs(new_kwargs, u'key')
        elif isinstance(vali, Regexp) and 'data_regexp' not in new_kwargs:
            _regexp_kwargs(new_kwargs, vali)
        elif isinstance(vali, URL):
            _url_kwargs(new_kwargs)
        elif isinstance(vali, AnyOf):
            _anyof_kwargs(new_kwargs, vali)
        else:
            # Don't copy messages from unknown validators
            copy_message = False

        if 'data_trigger' not in new_kwargs:
            _trigger_kwargs(new_kwargs)
        if 'parsley-error-message' not in new_kwargs and copy_message and vali.message is not None:
            _message_kwargs(new_kwargs, message=vali.message)

    return new_kwargs


def _email_kwargs(kwargs):
    kwargs[u'data-parsley-type'] = u'email'


def _equal_to_kwargs(kwargs, vali):
    kwargs[u'data-parsley-equalto'] = u'#' + vali.fieldname


def _ip_address_kwargs(kwargs):
    # Regexp from http://stackoverflow.com/a/4460645
    kwargs[u'data-parsley-regexp'] =\
        r'^\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b$'


def _length_kwargs(kwargs, vali):
    default_number = -1

    if vali.max != default_number and vali.min != default_number:
        kwargs[u'data-parsley-rangelength'] = u'[' + str(vali.min) + u',' + str(vali.max) + u']'
    else:
        if vali.max == default_number:
            kwargs[u'data-parsley-minlength'] = str(vali.min)
        if vali.min == default_number:
            kwargs[u'data-parsley-maxlength'] = str(vali.max)


def _number_range_kwargs(kwargs, vali):
    kwargs[u'data-parsley-range'] = u'[' + str(vali.min) + u',' + str(vali.max) + u']'


def _input_required_kwargs(kwargs):
    kwargs[u'data-parsley-required'] = u'true'


def _regexp_kwargs(kwargs, vali):
    # Apparently, this is the best way to check for RegexObject Type
    # It's needed because WTForms allows compiled regexps to be passed to the validator
    RegexObject = type(re.compile(''))
    if isinstance(vali.regex, RegexObject):
        regex_string = vali.regex.pattern
    else:
        regex_string = vali.regex
    kwargs[u'data-parsley-regexp'] = regex_string


def _url_kwargs(kwargs):
    kwargs[u'data-parsley-type'] = u'url'


def _string_seq_delimiter(vali, kwargs):
    # We normally use a comma as the delimiter - looks clean and it's parsley's default.
    # If the strings for which we check contain a comma, we cannot use it as a delimiter.
    default_delimiter = u','
    fallback_delimiter = u';;;'
    delimiter = default_delimiter
    for value in vali.values:
        if value.find(',') != -1:
            delimiter = fallback_delimiter
            break
    if delimiter != default_delimiter:
        kwargs[u'data-parsley-inlist-delimiter'] = delimiter
    return delimiter


def _anyof_kwargs(kwargs, vali):
    delimiter = _string_seq_delimiter(vali, kwargs)
    kwargs[u'data-parsley-inlist'] = delimiter.join(vali.values)


def _trigger_kwargs(kwargs, trigger=u'change'):
    kwargs[u'data-parsley-trigger'] = trigger


def _message_kwargs(kwargs, message):
    kwargs[u'data-parsley-error-message'] = message


class ParsleyInputMixin(Input):
    def __call__(self, field, **kwargs):
        kwargs = parsley_kwargs(field, kwargs)
        return super(ParsleyInputMixin, self).__call__(field, **kwargs)


class TextInput(_TextInput, ParsleyInputMixin):
    pass


class PasswordInput(_PasswordInput, ParsleyInputMixin):
    pass


class HiddenInput(_HiddenInput, ParsleyInputMixin):
    pass


class TextArea(_TextArea, ParsleyInputMixin):
    pass


class CheckboxInput(_CheckboxInput, ParsleyInputMixin):
    pass


class TelInput(_TelInput, ParsleyInputMixin):
    pass


class URLInput(_URLInput, ParsleyInputMixin):
    pass


class EmailInput(_EmailInput, ParsleyInputMixin):
    pass


class DateInput(_DateInput, ParsleyInputMixin):
    pass


class NumberInput(_NumberInput, ParsleyInputMixin):
    pass


class Select(_Select):
    def __call__(self, field, **kwargs):
        kwargs = parsley_kwargs(field, kwargs)
        return super(Select, self).__call__(field, **kwargs)


class ListWidget(_ListWidget):
    def __call__(self, field, **kwargs):
        kwargs = parsley_kwargs(field, kwargs)
        return super(ListWidget, self).__call__(field, **kwargs)


class StringField(_StringField):
    widget = TextInput()


class IntegerField(_IntegerField):
    widget = NumberInput()


class RadioField(_RadioField):
    widget = ListWidget()


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
