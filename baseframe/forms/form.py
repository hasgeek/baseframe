"""Form base class and redefined fields with ParsleyJS support."""

from threading import Lock
import typing as t
import uuid

from flask import current_app
from flask_wtf import FlaskForm as BaseForm
from wtforms.utils import unset_value
import wtforms

from ..extensions import __, asset_cache
from ..signals import form_validation_error, form_validation_success
from . import fields as bfields
from . import filters as bfilters
from . import parsleyjs as bparsleyjs
from . import validators as bvalidators

__all__ = [
    'field_registry',
    'widget_registry',
    'validator_registry',
    'Form',
    'FormGenerator',
    'RecaptchaForm',
]

# Use a hardcoded list to control what is available to user-facing apps
field_registry: t.Dict[str, t.Type] = {
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

widget_registry: t.Dict[str, t.Tuple] = {}

validator_registry: t.Dict[
    str,
    t.Union[
        t.Tuple[t.Callable],
        t.Tuple[t.Callable, str],
        t.Tuple[t.Callable, str, str],
        t.Tuple[t.Callable, str, str, str],
    ],
] = {
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

filter_registry: t.Dict[str, t.Union[t.Tuple[t.Callable], t.Tuple[t.Callable, str]]] = {
    'lower': (bfilters.lower,),
    'upper': (bfilters.upper,),
    'strip': (bfilters.strip, 'chars'),
    'lstrip': (bfilters.lstrip, 'chars'),
    'rstrip': (bfilters.rstrip, 'chars'),
    'none_if_empty': (bfilters.none_if_empty,),
}


_nonce_lock = Lock()


def _nonce_cache_key(nonce: str) -> str:
    return 'form_nonce/' + nonce


def _nonce_validator(form, field) -> None:
    # Check for already-used form nonce
    if field.data:
        with _nonce_lock:
            # nonce_lock prevents parallel requests from attempting to use the same
            # nonce in a multi-threaded deployment. As a thread lock, it is ineffective
            # in a multi-process deployment, as is typical when using uwsgi or gunicorn.
            nonce_cache_key = _nonce_cache_key(field.data)
            nonce_cache_hit = asset_cache.get(nonce_cache_key)
            if nonce_cache_hit is not None:
                raise bvalidators.StopValidation(form.form_nonce_error)
            # Mark this nonce as used for 10 seconds
            asset_cache.set(_nonce_cache_key(field.data), True, 10)
        # Set a new nonce. This is a conscious deviation from the convention for
        # validators, which are expected to validate but not modify the data, leaving
        # that to filters. However, filters run before validators, and the form nonce
        # is nonsense data that will be imminently discarded, so this is okay here.
        field.data = field.default()


class Form(BaseForm):
    """Form with additional methods."""

    __expects__: t.Iterable[str] = ()
    __returns__: t.Iterable[str] = ()

    form_nonce = bfields.NonceField(
        "Nonce", validators=[_nonce_validator], default=lambda: uuid.uuid4().hex
    )
    form_nonce_error = __("This form has already been submitted")

    def __init_subclass__(cls, **kwargs) -> None:
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

    def __init__(self, *args, **kwargs) -> None:
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
        self.set_queries()

    def __json__(self):
        """Render this form as JSON."""
        return [field.__json__() for field in self._fields.values()]

    def populate_obj(self, obj) -> None:
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
        self, formdata=None, obj=None, data=None, extra_filters=None, **kwargs
    ) -> None:
        """
        Take form, object data, and keyword arg input and have the fields process them.

        :param formdata: Used to pass data coming from the enduser, usually
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
            field_extra_filters = filters.get(name, [])

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
        extra_validators: t.Optional[
            t.Dict[str, t.Callable[[wtforms.Form, wtforms.Field], None]]
        ] = None,
        send_signals: bool = True,
    ) -> bool:
        success = super().validate(extra_validators)
        for attr in self.__returns__:
            if not hasattr(self, attr):
                setattr(self, attr, None)
        if send_signals:
            self.send_signals(success)
        return success

    def send_signals(self, success: t.Optional[bool] = None) -> None:
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

    def set_queries(self) -> None:
        """
        Set queries/choices as may be required for fields.

        This is an overridable method and is typically required on forms that use
        QuerySelectField or QuerySelectMultipleField, or have select fields with choices
        that are only available at runtime.
        """


class FormGenerator:
    """
    Creates forms from a JSON-compatible dictionary structure.

    Consults an allowed set of fields, widgets, validators and filters.
    """

    def __init__(
        self,
        fields=None,
        widgets=None,
        validators=None,
        filters=None,
        default_field='StringField',
    ) -> None:
        # If using global defaults, make a copy in this class so that
        # they can be customised post-init without clobbering the globals
        self.fields = fields or dict(field_registry)
        self.widgets = widgets or dict(widget_registry)
        self.validators = validators or dict(validator_registry)
        self.filters = filters or dict(filter_registry)

        self.default_field = default_field

    def generate(self, formstruct: dict) -> t.Type[Form]:
        """Generate a dynamic form from the given data structure."""

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

            # TODO: Also validate the parameters in fielddata, like with validators
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

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not (
            current_app.config.get('RECAPTCHA_PUBLIC_KEY')
            and current_app.config.get('RECAPTCHA_PRIVATE_KEY')
        ):
            del self.recaptcha
