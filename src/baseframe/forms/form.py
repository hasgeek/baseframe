"""Form base class and redefined fields with ParsleyJS support."""

from __future__ import annotations

import warnings
from collections.abc import Iterable
from typing import Any, Callable, Optional, Union
from typing_extensions import TypeAlias

import wtforms
from flask import current_app
from flask_wtf import FlaskForm as BaseForm
from werkzeug.datastructures import MultiDict
from wtforms import Field as WTField
from wtforms.utils import unset_value

from ..signals import form_validation_error, form_validation_success
from . import (
    fields as bfields,
    filters as bfilters,
    parsleyjs as bparsleyjs,
    validators as bvalidators,
)
from .typing import FilterCallable, ValidatorCallable, ValidatorList, WidgetProtocol

__all__ = [
    'Form',
    'FormGenerator',
    'RecaptchaForm',
    'field_registry',
    'validator_registry',
    'widget_registry',
]

# Use a hardcoded list to control what is available to user-facing apps
field_registry: dict[str, WTField] = {
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

WidgetRegistryEntry: TypeAlias = tuple[Callable[..., WidgetProtocol]]
widget_registry: dict[str, WidgetRegistryEntry] = {}

ValidatorRegistryEntry: TypeAlias = Union[
    tuple[Callable[..., ValidatorCallable]],
    tuple[Callable[..., ValidatorCallable], str],
    tuple[Callable[..., ValidatorCallable], str, str],
    tuple[Callable[..., ValidatorCallable], str, str, str],
]
validator_registry: dict[str, ValidatorRegistryEntry] = {
    'Length': (wtforms.validators.Length, 'min', 'max', 'message'),
    'NumberRange': (wtforms.validators.NumberRange, 'min', 'max', 'message'),
    'Optional': (wtforms.validators.Optional, 'strip_whitespace'),
    'Required': (wtforms.validators.DataRequired, 'message'),
    'AnyOf': (wtforms.validators.AnyOf, 'values', 'message'),
    'NoneOf': (wtforms.validators.NoneOf, 'values', 'message'),
    'ValidEmail': (bvalidators.ValidEmail,),
    'ValidUrl': (bvalidators.ValidUrl,),
    'AllUrlsValid': (bvalidators.AllUrlsValid,),
}

FilterRegistryEntry: TypeAlias = Union[
    tuple[Callable[..., FilterCallable]],
    tuple[Callable[..., FilterCallable], str],
]
filter_registry: dict[str, FilterRegistryEntry] = {
    'lower': (bfilters.lower,),
    'upper': (bfilters.upper,),
    'strip': (bfilters.strip, 'chars'),
    'lstrip': (bfilters.lstrip, 'chars'),
    'rstrip': (bfilters.rstrip, 'chars'),
    'none_if_empty': (bfilters.none_if_empty,),
}


class Form(BaseForm):
    """Form with additional methods."""

    __expects__: Iterable[str] = ()
    __returns__: Iterable[str] = ()

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Validate :attr:`__expects__` and :attr:`__returns__` in sub-classes."""
        super().__init_subclass__(**kwargs)
        if {'edit_obj', 'edit_model', 'edit_parent', 'edit_id'} & set(cls.__expects__):
            raise TypeError(
                "This form has __expects__ parameters that are reserved by the base"
                " form"
            )

        if set(cls.__dict__.keys()) & set(cls.__expects__):
            raise TypeError(
                "This form has __expects__ parameters that clash with field names"
            )
        if 'set_queries' in cls.__dict__ and 'queries' not in cls.__dict__:
            warnings.warn(
                f"`{cls.__qualname__}.set_queries` is deprecated due to conflict with"
                " `set_<fieldname>` methods. Rename it to `__post_init__`",
                stacklevel=2,
            )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for attr in self.__expects__:
            if attr not in kwargs:
                raise TypeError(f"Expected parameter {attr} was not supplied")
            setattr(self, attr, kwargs.pop(attr))

        # TODO: These fields predate the `__expects__` protocol and are pending
        # deprecation.
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

        # Call baseclass after expected parameters have been set. `__init__` will call
        # `process`, which will in turn call the ``get_<fieldname>`` methods, and they
        # will need proper context
        super().__init__(*args, **kwargs)

        # Finally, populate the ``choices`` attr of selection fields
        if callable(post_init := getattr(self, '__post_init__', None)) or callable(
            post_init := getattr(self, 'set_queries', None)
        ):
            post_init()  # pylint: disable=not-callable

    def __json__(self) -> Any:
        """Render this form as JSON."""
        return [field.__json__() for field in self._fields.values()]

    def populate_obj(self, obj: Any) -> None:
        """
        Populate the attributes of the passed `obj` with data from the form's fields.

        If the form has a ``set_<fieldname>`` method, it will be called with the object
        in place of the field's ``populate_obj`` method. The custom method is then
        responsible for populating the object with that field's value.

        This method overrides the default implementation in WTForms to support custom
        set methods.
        """
        for name, field in self._fields.items():
            if hasattr(self, 'set_' + name):
                getattr(self, 'set_' + name)(obj)
            else:
                field.populate_obj(obj, name)

    def process(
        self,
        formdata: Optional[MultiDict] = None,
        obj: Any = None,
        data: Optional[dict[str, Any]] = None,
        extra_filters: Optional[dict[str, Iterable[Callable[[Any], Any]]]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Take form, object data, and keyword arg input and have the fields process them.

        :param formdata: Used to pass data coming from the client, usually
            `request.POST` or equivalent.
        :param obj: If `formdata` is empty or not provided, this object is checked for
            attributes matching form field names, which will be used for field values.
            If the form has a ``get_<fieldname>`` method, it will be called with the
            object as an attribute and is expected to return the value
        :param data: If provided, must be a dictionary of data. This is only used if
            `formdata` is empty or not provided and `obj` does not contain an attribute
            named the same as the field.
        :param extra_filters: A dict mapping field attribute names to lists of extra
            filter functions to run. Extra filters run after filters passed when
            creating the field. If the form has ``filter_<fieldname>``, it is the last
            extra filter.
        :param kwargs: If `formdata` is empty or not provided and `obj` does not contain
            an attribute named the same as a field, form will assign the value of a
            matching keyword argument to the field, if one exists.

        This method overrides the default implementation in WTForms to support custom
        load methods.
        """
        formdata = self.meta.wrap_formdata(self, formdata)

        if data is not None:
            kwargs = dict(data, **kwargs)

        filters = extra_filters.copy() if extra_filters is not None else {}

        for name, field in self._fields.items():
            field_extra_filters = list(filters.get(name, []))

            inline_filter = getattr(self, f'filter_{name}', None)
            if inline_filter is not None:
                field_extra_filters.append(inline_filter)

            # This `if` condition is the only change from the WTForms source. It must be
            # synced with the `process` method in future WTForms releases.
            if obj is not None and hasattr(self, f'get_{name}'):
                data = getattr(self, f'get_{name}')(obj)
            elif obj is not None and hasattr(obj, name):
                data = getattr(obj, name)
            else:
                data = kwargs.get(name, unset_value)

            field.process(formdata, data, extra_filters=field_extra_filters)

    def validate(
        self,
        extra_validators: Optional[dict[str, ValidatorList]] = None,
        send_signals: bool = True,
    ) -> bool:
        """
        Validate a form.

        :param extra_validators: A dict of field name to list of extra validators
        :param send_signals: Raise :attr:`~baseframe.signals.form_validation_success` or
            :attr:`~baseframe.signals.form_validation_error` after validation

        Signal handlers may be used to record analytics. Baseframe provides default
        handlers that log to :class:`~baseframe.statsd.Statsd` if enabled for the app,
        tagging the names of erroring fields in case of errors.
        """
        success = super().validate(extra_validators)
        for attr in self.__returns__:
            if not hasattr(self, attr):
                setattr(self, attr, None)
        if send_signals:
            self.send_signals(success)
        return success

    def send_signals(self, success: Optional[bool] = None) -> None:
        if success is None:
            success = not self.errors
        if success:
            form_validation_success.send(self)
        else:
            form_validation_error.send(self)

    def errors_with_data(self) -> dict:
        return {
            name: {
                'data': f.data,
                'errors': [str(e) for e in f.errors],  # str(lazy_gettext) needed
            }
            for name, f in self._fields.items()
            if f.errors
        }


class FormGenerator:
    """
    Creates forms from a JSON-compatible dictionary structure.

    Consults an allowed set of fields, widgets, validators and filters.
    """

    def __init__(
        self,
        fields: Optional[dict[str, WTField]] = None,
        widgets: Optional[dict[str, WidgetRegistryEntry]] = None,
        validators: Optional[dict[str, ValidatorRegistryEntry]] = None,
        filters: Optional[dict[str, FilterRegistryEntry]] = None,
        default_field: str = 'StringField',
    ) -> None:
        # If using global defaults, make a copy in this class so that
        # they can be customised post-init without clobbering the globals
        self.fields = fields or dict(field_registry)
        self.widgets = widgets or dict(widget_registry)
        self.validators = validators or dict(validator_registry)
        self.filters = filters or dict(filter_registry)

        self.default_field = default_field

    # TODO: Make `formstruct` a TypedDict
    def generate(self, formstruct: dict) -> type[Form]:
        """Generate a dynamic form from the given data structure."""

        class DynamicForm(Form):
            pass

        for _fielddata in formstruct:
            fielddata = dict(_fielddata)  # Make a copy
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
                if isinstance(item, str) and item in validator_registry:
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
                if isinstance(item, str) and item in filter_registry:
                    filters.append(filter_registry[item][0]())
                else:
                    itemname = item.pop('type', None)
                    itemparams = {}
                    if itemname:
                        for paramname in item:
                            if paramname in filter_registry[itemname][1:]:
                                itemparams[paramname] = item[paramname]
                        filters.append(filter_registry[itemname][0](**itemparams))

            # TODO: Also validate the parameters in `fielddata`, like with validators
            # above
            setattr(
                DynamicForm,
                name,
                field_registry[type_](
                    validators=validators, filters=filters, **fielddata
                ),
            )
        return DynamicForm


class RecaptchaForm(Form):
    """Base class for forms that use Recaptcha."""

    recaptcha = bfields.RecaptchaField()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if not (
            current_app.config.get('RECAPTCHA_PUBLIC_KEY')
            and current_app.config.get('RECAPTCHA_PRIVATE_KEY')
        ):
            del self.recaptcha
