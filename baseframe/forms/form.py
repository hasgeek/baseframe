# -*- coding: utf-8 -*-

from speaklater import is_lazy_string
import wtforms
from wtforms.compat import iteritems
from flask.ext.wtf import Form as BaseForm

from ..signals import form_validation_error, form_validation_success
from . import fields as bfields, validators as bvalidators, parsleyjs as bparsleyjs, filters as bfilters

__all__ = ['field_registry', 'widget_registry', 'validator_registry', 'Form', 'FormGenerator']

# Use a hardcoded list to control what is available to user-facing apps
field_registry = {
    'SelectField': bparsleyjs.SelectField,
    'SelectMultipleField': bfields.SelectMultipleField,
    'RadioField': bparsleyjs.RadioField,
    'StringField': bparsleyjs.StringField,
    'IntegerField': bparsleyjs.IntegerField,
    'DecimalField': bparsleyjs.DecimalField,
    'FloatField': bparsleyjs.FloatField,
    'BooleanField': bparsleyjs.BooleanField,
    'TelField': bparsleyjs.TelField,
    'URLField': bparsleyjs.URLField,
    'EmailField': bparsleyjs.EmailField,
    'DateTimeField': bfields.DateTimeField,
    'DateField': bparsleyjs.DateField,
    'TextAreaField': bparsleyjs.TextAreaField,
    'PasswordField': bparsleyjs.PasswordField,
    # Baseframe fields
    'RichTextField': bfields.TinyMce4Field,
    'TextListField': bfields.TextListField,
    'UserSelectField': bfields.UserSelectField,
    'UserSelectMultiField': bfields.UserSelectMultiField,
    'GeonameSelectField': bfields.GeonameSelectField,
    'GeonameSelectMultiField': bfields.GeonameSelectMultiField,
    'AnnotatedTextField': bfields.AnnotatedTextField,
    'MarkdownField': bfields.MarkdownField,
    'ImageField': bfields.ImgeeField,
    }

widget_registry = {}

validator_registry = {
    'Length': (wtforms.validators.Length, 'min', 'max', 'message'),
    'NumberRange': (wtforms.validators.NumberRange, 'min', 'max', 'message'),
    'Optional': (wtforms.validators.Optional, 'strip_whitespace'),
    'Required': (wtforms.validators.DataRequired, 'message'),
    'AnyOf': (wtforms.validators.AnyOf, 'values', 'message'),
    'NoneOf': (wtforms.validators.NoneOf, 'values', 'message'),
    'ValidEmail': bvalidators.ValidEmail,
    'ValidUrl': bvalidators.ValidUrl,
    'AllUrlsValid': bvalidators.AllUrlsValid,
    }

filter_registry = {
    'lower': (bfilters.lower,),
    'upper': (bfilters.upper,),
    'strip': (bfilters.strip, 'chars'),
    'lstrip': (bfilters.lstrip, 'chars'),
    'rstrip': (bfilters.rstrip, 'chars'),
    'none_if_empty': (bfilters.none_if_empty),
}


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

    def validate(self, send_signals=True):
        result = super(Form, self).validate()
        if send_signals:
            self.send_signals()
        return result

    def send_signals(self):
        if self.errors:
            form_validation_error.send(self)
        else:
            form_validation_success.send(self)

    def errors_with_data(self):
        # Convert lazy_gettext error strings into unicode so they don't cause problems downstream
        # (like when pickling)
        return {name: {'data': f.data, 'errors': [unicode(e) if is_lazy_string(e) else e for e in f.errors]}
            for name, f in iteritems(self._fields) if f.errors}


class FormGenerator(object):
    """
    Creates forms from a JSON-compatible dictionary structure
    based on the allowed set of fields, widgets, validators and filters.
    """
    def __init__(self, fields=None, widgets=None, validators=None, filters=None, default_field='StringField'):
        # If using global defaults, make a copy in this class so that
        # they can be customised post-init without clobbering the globals
        self.fields = fields or dict(field_registry)
        self.widgets = widgets or dict(widget_registry)
        self.validators = validators or dict(validator_registry)
        self.filters = filters or dict(filter_registry)

        self.default_field = default_field

    def generate(self, formstruct):
        """
        Generate a dynamic form from the given data structure.
        """
        class DynamicForm(Form):
            pass

        for fielddata in formstruct:
            fielddata = dict(fielddata)  # Make a copy
            name = fielddata.pop('name', None)
            type_ = fielddata.pop('type', None)
            if not name:
                continue  # Skip unnamed fields
            if (not type_) or type_ not in field_registry:
                type_ = self.default_field  # Default to string input

            # TODO: Process widget requests

            # Make a list of validators
            validators = []
            validators_data = fielddata.pop('validators', [])
            for item in validators_data:
                if isinstance(item, basestring) and item in validator_registry:
                    validators.append(validator_registry[item][0]())
                else:
                    itemname = item.pop('type', None)
                    itemparams = {}
                    if itemname:
                        for paramname in item:
                            if paramname in validator_registry[itemname][1:]:
                                itemparams[paramname] = item[paramname]
                        validators.append(validator_registry[itemname][0](**itemparams))

            # Make a list of filters
            filters = []
            filters_data = fielddata.pop('filters', [])
            for item in filters_data:
                if isinstance(item, basestring) and item in filter_registry:
                    filters.append(filter_registry[item][0]())
                else:
                    itemname = item.pop('type', None)
                    itemparams = {}
                    if itemname:
                        for paramname in item:
                            if paramname in filter_registry[itemname][1:]:
                                itemparams[paramname] = item[paramname]
                        filters.append(filter_registry[itemname][0](**itemparams))

            # TODO: Also validate the parameters in fielddata, like with validators above
            setattr(DynamicForm, name, field_registry[type_](validators=validators, filters=filters, **fielddata))
        return DynamicForm
