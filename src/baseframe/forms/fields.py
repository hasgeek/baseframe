"""Form fields."""
# ruff: noqa: ARG002
# pylint: disable=attribute-defined-outside-init,unused-argument

from __future__ import annotations

import itertools
from collections.abc import Iterable, Mapping
from datetime import datetime, tzinfo
from decimal import Decimal, InvalidOperation as DecimalError
from typing import Any, Callable, Optional, Protocol, Union, cast, runtime_checkable
from urllib.parse import urljoin

import bleach
import wtforms
from dateutil import parser
from flask import current_app, json
from flask_wtf import RecaptchaField as RecaptchaFieldBase
from pytz import timezone as pytz_timezone, utc
from werkzeug.datastructures import MultiDict
from wtforms import Form as WTForm
from wtforms.fields import (
    DateTimeField as DateTimeFieldBase,
    Field,
    FieldList,
    FileField,
    Label,
    SelectField as SelectFieldBase,
    SelectMultipleField,
    SubmitField,
    TextAreaField as TextAreaFieldBase,
)
from wtforms.utils import unset_value
from wtforms.widgets import Select as OriginalSelectWidget

from ..extensions import _, __, get_timezone
from ..utils import request_timestamp
from .parsleyjs import StringField, TextAreaField, URLField
from .typing import ReturnIterChoices, ValidatorList
from .validators import Recaptcha, StopValidation, ValidationError
from .widgets import (
    CoordinatesInput,
    DateTimeInput,
    ImgeeWidget,
    RadioMatrixInput,
    Select2Widget,
    SelectWidget,
    TinyMce4,
)

__all__ = [
    'SANITIZE_ATTRIBUTES',
    'SANITIZE_TAGS',
    'AnnotatedTextField',
    'AutocompleteField',
    'AutocompleteMultipleField',
    'CoordinatesField',
    'DateTimeField',
    'EnumSelectField',
    'Field',
    'FieldList',
    'FileField',
    'FormField',
    'GeonameSelectField',
    'GeonameSelectMultiField',
    'ImgeeField',
    'JsonField',
    'Label',
    'MarkdownField',
    'RadioMatrixField',
    'RecaptchaField',
    'SelectField',
    'SelectMultipleField',
    'StylesheetField',
    'SubmitField',
    'TextListField',
    'TinyMce4Field',
    'UserSelectField',
    'UserSelectMultiField',
]

# Default tags and attributes to allow in HTML sanitization
SANITIZE_TAGS = [
    'p',
    'br',
    'strong',
    'em',
    'sup',
    'sub',
    'h3',
    'h4',
    'h5',
    'h6',
    'ul',
    'ol',
    'li',
    'a',
    'blockquote',
    'code',
]
SANITIZE_ATTRIBUTES = {'a': ['href', 'title', 'target']}


@runtime_checkable
class GeonameidProtocol(Protocol):
    geonameid: str


class RecaptchaField(RecaptchaFieldBase):
    """RecaptchaField with an improved validator."""

    def __init__(
        self,
        label: str = '',
        validators: Optional[ValidatorList] = None,
        **kwargs: Any,
    ) -> None:
        validators = validators or [Recaptcha()]
        super().__init__(label, validators, **kwargs)


# This class borrowed from https://github.com/industrydive/wtforms_extended_selectfield
class SelectField(SelectFieldBase):
    """
    Add support of ``optgroup`` grouping to the default ``SelectField`` from WTForms.

    Here is an example of how the data is laid out::

        (
            ("Fruits", (('apple', "Apple"), ('peach', "Peach"), ('pear', "Pear"))),
            (
                "Vegetables",
                (
                    ('cucumber', "Cucumber"),
                    ('potato', "Potato"),
                    ('tomato', "Tomato"),
                ),
            ),
            ('other', "None of the above"),
        )

    It's a little strange that the tuples are (value, label) except for groups which are
    (Group Label, list of tuples) but this is how Django does it too.
    https://docs.djangoproject.com/en/dev/ref/models/fields/#choices
    """

    widget = SelectWidget()

    def pre_validate(self, form: WTForm) -> None:
        """Don't forget to also validate values from embedded lists."""
        for item1, item2 in self.choices:
            if isinstance(item2, (list, tuple)):
                # group_label = item1
                group_items = item2
                for val, _label in group_items:
                    if val == self.data:
                        return
            else:
                val = item1
                # label = item2
                if val == self.data:
                    return
        raise StopValidation(_("Not a valid choice"))


class TinyMce4Field(TextAreaField):
    """Rich text field using TinyMCE 4."""

    data: Optional[str]
    widget = TinyMce4()

    def __init__(
        self,
        *args: Any,
        content_css: Optional[Union[str, Callable[[], str]]] = None,
        linkify: bool = True,
        nofollow: bool = True,
        tinymce_options: Optional[dict[str, Any]] = None,
        sanitize_tags: Optional[list[str]] = None,
        sanitize_attributes: Optional[dict[str, list[str]]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        # Clone the dict to preserve local edits
        tinymce_options = {} if tinymce_options is None else dict(tinymce_options)

        # Set defaults for TinyMCE
        tinymce_options.setdefault(
            'plugins', 'autolink autoresize link lists paste searchreplace'
        )
        tinymce_options.setdefault(
            'toolbar',
            'bold italic | bullist numlist | link unlink | searchreplace undo redo',
        )
        tinymce_options.setdefault('width', '100%')
        tinymce_options.setdefault('height', '200')
        tinymce_options.setdefault('autoresize_min_height', '159')
        tinymce_options.setdefault('autoresize_max_height', '200')
        tinymce_options.setdefault(
            'valid_elements',
            'p,br,strong/b,em/i,sup,sub,h3,h4,h5,h6,ul,ol,li,a[!href|title|target]'
            ',blockquote,code',
        )
        tinymce_options.setdefault('statusbar', False)
        tinymce_options.setdefault('menubar', False)
        tinymce_options.setdefault('resize', True)
        tinymce_options.setdefault('relative_urls', False)
        tinymce_options.setdefault('remove_script_host', False)

        # Remove options that cannot be set by callers
        tinymce_options.pop('content_css', None)
        tinymce_options.pop('script_url', None)
        tinymce_options.pop('setup', None)

        if sanitize_tags is None:
            sanitize_tags = SANITIZE_TAGS
        if sanitize_attributes is None:
            sanitize_attributes = SANITIZE_ATTRIBUTES

        self.linkify = linkify
        self.nofollow = nofollow
        self.tinymce_options = tinymce_options

        self._content_css = content_css
        self.sanitize_tags = sanitize_tags
        self.sanitize_attributes = sanitize_attributes

    @property
    def content_css(self) -> Optional[str]:
        if callable(self._content_css):
            return self._content_css()
        return self._content_css

    def process_formdata(self, valuelist: list[str]) -> None:
        """Process incoming data from request form."""
        super().process_formdata(valuelist)
        # Sanitize data
        self.data = bleach.clean(
            self.data or '',
            strip=True,
            tags=self.sanitize_tags,
            attributes=self.sanitize_attributes,
        )
        if self.linkify:
            if self.nofollow:
                self.data = bleach.linkify(self.data or '')
            else:
                self.data = bleach.linkify(self.data or '', callbacks=[])


class DateTimeField(DateTimeFieldBase):
    """
    A text field which stores a `datetime.datetime` matching a format.

    This field only handles UTC timestamps, but renders to UI in the user's timezone,
    as specified in the timezone parameter. If not specified, the timezone is guessed
    from the runtime environment.

    :param str label: Label to display against the field
    :param list validators: List of validators
    :param str display_format: Datetime format string
    :param str timezone: Timezone used for user input
    :param str message: Message for when the date/time could not be parsed
    :param bool naive: If `True` (default), timezone info is stripped from the return
        data
    """

    widget = DateTimeInput()
    data: Optional[datetime]
    default_message = __("This date/time could not be recognized")
    _timezone: tzinfo

    def __init__(
        self,
        *args: Any,
        display_format: str = '%Y-%m-%dT%H:%M',
        timezone: Union[str, tzinfo, None] = None,
        message: Optional[str] = None,
        naive: bool = True,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.display_format = display_format
        self.timezone = timezone  # type: ignore[assignment]
        self.message = message if message is not None else self.default_message
        self.naive = naive

    @property
    def timezone(self) -> tzinfo:
        return self._timezone

    @timezone.setter
    def timezone(self, value: Union[str, tzinfo, None]) -> None:
        if value is None:
            value = get_timezone()
        if isinstance(value, str):
            self._timezone = pytz_timezone(value)
        else:
            self._timezone = value

        # A note on DST:

        # During a DST transition, the clock is set back by an hour. A naive timestamp
        # within this hour will be ambiguous about whether it is referring to the time
        # pre-transition or post-transition. pytz expects us to clarify using the is_dst
        # flag. Ideally, we should ask the user, but this is tricky: the question only
        # applies for time within that hour, so the front-end should detect it and then
        # prompt the user. Transitions happen late at night and it is very unlikely in
        # our use cases that a user will want to select a time during that period.

        # Therefore, we simply assume that whatever is the current zone when the widget
        # is rendered is also the zone in which ambiguous time is specified.

        # Related: now.tzname() will return 'IST' all year for timezone 'Asia/Kolkata',
        # while for 'America/New_York' it will be 'EST' or 'EDT'. We will be showing the
        # user the current name even though they may be inputting a future date that is
        # in the other zone. OTOH, Indian users will recognise 'IST' but not
        # 'Asia/Kolkata', since India does not have multiple timezones and a user may be
        # left wondering why they are specifying time in a distant city.

        # Using 'tzname' instead of 'zone' optimises for Indian users, but we will have
        # to revisit this as we expand to a global footprint.

        now = request_timestamp().astimezone(self.timezone)
        self.tzname = now.tzname()
        self.is_dst = bool(now.dst())

    def _value(self) -> str:
        if self.data:
            if self.data.tzinfo is None:
                # We got a naive datetime from the calling app. Assume UTC
                data = utc.localize(self.data).astimezone(self.timezone)
            else:
                # We got a tz-aware datetime. Cast into the required timezone
                data = self.data.astimezone(self.timezone)
            value = data.strftime(self.display_format)
        else:
            value = ''
        return value

    def process_formdata(self, valuelist: list[str]) -> None:
        """Process incoming data from request form."""
        if valuelist:
            # We received a timestamp from the browser. Parse and save it
            data: Optional[datetime] = None
            # `valuelist` will contain `date` and `time` as two separate values
            # if the widget is rendered as two parts. If so, parse each at a time
            # and use it as a default to replace values from the next value.  If the
            # front-end renders a single widget, the entire content will be parsed once.
            for value in valuelist:
                if value.strip():
                    try:
                        # `dateutil` cannot handle ISO and European-style dates at the
                        # same time, so `dayfirst` MUST be False. Setting it to True
                        # will interpret YYYY-DD-MM instead of YYYY-MM-DD. Bug report:
                        # https://github.com/dateutil/dateutil/issues/402
                        data = parser.parse(
                            value, default=data, ignoretz=False, dayfirst=False
                        )
                    except (ValueError, OverflowError, TypeError):
                        # TypeError is not a documented error for `parser.parse`, but
                        # the DateTimeField implementation in `wtforms_dateutil` says
                        # it can happen due to a known bug
                        raise ValidationError(self.message) from None
            if data is not None:
                if data.tzinfo is None:
                    # NOTE: localize is implemented separately in the sub-classes of
                    # tzinfo: in UTC, StaticTzInfo and DstTzInfo. We've told mypy
                    # we take the base type, so we need to ask it to ignore the missing
                    # function there
                    data = self.timezone.localize(  # type: ignore[attr-defined]
                        data, is_dst=self.is_dst
                    ).astimezone(utc)
                else:
                    data = data.astimezone(utc)
                # If the app wanted a naive datetime, strip the timezone info
                if self.naive:
                    # XXX: cast required because mypy misses the `not None` test above
                    data = cast(datetime, data).replace(tzinfo=None)
            self.data = data
        else:
            self.data = None


class TextListField(TextAreaFieldBase):
    """A list field that renders as a textarea with one line per list item."""

    def _value(self) -> str:
        if self.data:
            return '\r\n'.join(self.data)
        return ''

    def process_formdata(self, valuelist: list[str]) -> None:
        """Process incoming data from request form."""
        if valuelist and valuelist[0]:
            self.data = (
                valuelist[0].replace('\r\n', '\n').replace('\r', '\n').split('\n')
            )
        else:
            self.data = []


class UserSelectFieldBase:
    """Select a user."""

    data: Optional[list[Any]]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.lastuser = kwargs.pop('lastuser', None)
        if self.lastuser is None:
            if hasattr(current_app, 'login_manager'):
                self.lastuser = current_app.login_manager
            else:
                raise RuntimeError("App does not have Lastuser as .login_manager")

        self.usermodel = kwargs.pop(
            'usermodel', self.lastuser.usermanager.usermodel if self.lastuser else None
        )
        self.separator = kwargs.pop('separator', ',')
        if self.lastuser:
            self.autocomplete_endpoint = self.lastuser.autocomplete_endpoint
            self.getuser_endpoint = self.lastuser.getuser_endpoint
        else:
            self.autocomplete_endpoint = kwargs.pop('autocomplete_endpoint')()
            self.getuser_endpoint = kwargs.pop('getuser_endpoint')()
        super().__init__(*args, **kwargs)

    def iter_choices(self) -> ReturnIterChoices:
        """Iterate over choices."""
        if self.data:
            for user in self.data:
                yield (user.userid, user.pickername, True, {})

    def process_formdata(self, valuelist: list[str]) -> None:
        """Process incoming data from request form."""
        super().process_formdata(valuelist)  # type: ignore[misc]
        userids = valuelist
        # Convert strings in userids into User objects
        users = []
        if userids:
            if self.lastuser and not getattr(
                self.lastuser, 'is_master_data_source', False
            ):
                usersdata = self.lastuser.getuser_by_userids(userids)
                # TODO: Move all of this inside the getuser method with user=True,
                # create=True
                for userinfo in usersdata:
                    if userinfo['type'] == 'user':
                        user = self.usermodel.query.filter_by(
                            userid=userinfo['buid']
                        ).first()
                        if not user:
                            # New user in this app. Don't set username right now. It's
                            # not relevant until first login and we don't want to deal
                            # with conflicts. We don't add this user to the session. The
                            # view is responsible for that (using SQLAlchemy cascades
                            # when assigning users to a collection).
                            user = self.usermodel(
                                userid=userinfo['buid'], fullname=userinfo['title']
                            )
                        users.append(user)
            else:
                users = self.usermodel.all(buids=userids)
        self.data = users


class UserSelectField(UserSelectFieldBase, StringField):
    """Render a user select field that allows one user to be selected."""

    data: Optional[Any]
    multiple = False
    widget = Select2Widget()
    widget_autocomplete = True

    def _value(self) -> str:
        """Render value for HTML."""
        if self.data:
            return self.data.userid
        return ''

    def iter_choices(self) -> ReturnIterChoices:
        """Iterate over choices."""
        if self.data:
            yield (self.data.userid, self.data.pickername, True, {})

    def process_formdata(self, valuelist: list[str]) -> None:
        """Process incoming data from request form."""
        super().process_formdata(valuelist)
        if self.data:
            self.data = self.data[0]
        else:
            self.data = None


class UserSelectMultiField(UserSelectFieldBase, StringField):
    """Render a user select field that allows multiple users to be selected."""

    data = list[type]
    multiple = True
    widget = Select2Widget()
    widget_autocomplete = True


class AutocompleteFieldBase:
    """Autocomplete a field."""

    data: Optional[Union[str, list[str]]]

    def __init__(
        self,
        *args: Any,
        autocomplete_endpoint: str,
        results_key: str = 'results',
        separator: str = ',',
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.autocomplete_endpoint = autocomplete_endpoint
        self.results_key = results_key
        self.separator = separator
        self.choices = ()  # Disregard server-side choices

    def iter_choices(self) -> ReturnIterChoices:
        """Iterate over choices."""
        if self.data:
            for user in self.data:
                yield (str(user), str(user), True, {})

    def process_formdata(self, valuelist: list[str]) -> None:
        """Process incoming data from request form."""
        super().process_formdata(valuelist)  # type: ignore[misc]
        # Convert strings into Tag objects
        self.data = valuelist

    def pre_validate(self, form: WTForm) -> None:
        """Do not validate data."""
        return


class AutocompleteField(AutocompleteFieldBase, StringField):
    """
    Select field that sources choices from a JSON API endpoint.

    Does not validate choices server-side.
    """

    data: Optional[str]
    multiple = False
    widget = Select2Widget()
    widget_autocomplete = True

    def _value(self) -> str:
        if self.data:
            return self.data
        return ''

    def process_formdata(self, valuelist: list[str]) -> None:
        """Process incoming data from request form."""
        super().process_formdata(valuelist)
        if self.data:
            self.data = self.data[0]
        else:
            self.data = None


class AutocompleteMultipleField(AutocompleteFieldBase, StringField):
    """
    Multiple select field that sources choices from a JSON API endpoint.

    Does not validate choices server-side.
    """

    data: Optional[list[str]]
    multiple = True
    widget = Select2Widget()
    widget_autocomplete = True


class GeonameSelectFieldBase:
    """Select a geoname location."""

    data: Optional[Union[str, list[str], GeonameidProtocol, list[GeonameidProtocol]]]

    def __init__(self, *args: Any, separator: str = ',', **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.separator = separator
        server = current_app.config.get('HASCORE_SERVER', 'https://hasgeek.com/api')
        self.autocomplete_endpoint = urljoin(server, '/1/geo/autocomplete')
        self.getname_endpoint = urljoin(server, '/1/geo/get_by_names')

    def iter_choices(self) -> ReturnIterChoices:
        """Iterate over choices."""
        if self.data:
            if isinstance(self.data, (str, GeonameidProtocol)):
                yield (str(self.data), str(self.data), True, {})
            else:
                for item in self.data:
                    yield (str(item), str(item), True, {})

    def process_formdata(self, valuelist: list[str]) -> None:
        """Process incoming data from request form."""
        super().process_formdata(valuelist)  # type: ignore[misc]
        # TODO: Convert strings into GeoName objects
        self.data = valuelist


class GeonameSelectField(GeonameSelectFieldBase, StringField):
    """Render a geoname select field that allows one geoname to be selected."""

    data: Optional[Union[str, GeonameidProtocol]]
    multiple = False
    widget = Select2Widget()
    widget_autocomplete = True

    def _value(self) -> str:
        if self.data:
            if isinstance(self.data, GeonameidProtocol):
                return self.data.geonameid
            return self.data
        return ''

    def process_formdata(self, valuelist: list[str]) -> None:
        """Process incoming data from request form."""
        super().process_formdata(valuelist)
        if self.data:
            if isinstance(self.data, (list, tuple)):
                self.data = self.data[0]
        else:
            self.data = None


class GeonameSelectMultiField(GeonameSelectFieldBase, StringField):
    """Render a geoname select field that allows multiple geonames to be selected."""

    data: Optional[Union[list[str], list[GeonameidProtocol]]]
    multiple = True
    widget = Select2Widget()
    widget_autocomplete = True


class AnnotatedTextField(StringField):
    """Text field with prefix and suffix annotations."""

    def __init__(
        self,
        *args: Any,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.prefix = prefix
        self.suffix = suffix


class MarkdownField(TextAreaField):
    """TextArea field which has class='markdown'."""

    def __call__(self, *args: Any, **kwargs: Any) -> str:
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = (c + ' markdown').strip()
        return super().__call__(*args, **kwargs)


class StylesheetField(wtforms.TextAreaField):
    """TextArea field which has class='stylesheet'."""

    def __call__(self, *args: Any, **kwargs: Any) -> str:
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = (c + ' stylesheet').strip()
        return super().__call__(*args, **kwargs)


class ImgeeField(URLField):
    """
    A URLField which lets the user choose an image from Imgee and returns the URL.

    Example usage::

        image = ImgeeField(
            label=__("Logo"),
            description=__("Your company logo here"),
            validators=[validators.DataRequired()],
            profile='foo',
            img_label='logos',
            img_size='100x75',
        )
    """

    widget = ImgeeWidget()

    def __init__(
        self,
        *args: Any,
        profile: Optional[Union[str, Callable[[], str]]] = None,
        img_label: Optional[str] = None,
        img_size: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.profile = profile
        self.img_label = img_label
        self.img_size = img_size

    def __call__(self, *args: Any, **kwargs: Any) -> str:
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = (c + ' imgee__url-holder').strip()
        if self.profile:
            kwargs['data-profile'] = (
                self.profile() if callable(self.profile) else self.profile
            )
        if self.img_label:
            kwargs['data-img-label'] = self.img_label
        if self.img_size:
            kwargs['data-img-size'] = self.img_size
        return super().__call__(*args, **kwargs)


class FormField(wtforms.FormField):
    """FormField that removes CSRF in sub-forms."""

    def process(self, *args: Any, **kwargs: Any) -> None:
        super().process(*args, **kwargs)
        if hasattr(self.form, 'csrf_token'):
            del self.form.csrf_token


class CoordinatesField(wtforms.Field):
    """Adds latitude and longitude fields and returns them as a tuple."""

    data: Optional[tuple[Optional[Decimal], Optional[Decimal]]]
    widget = CoordinatesInput()

    def process_formdata(self, valuelist: list[str]) -> None:
        """Process incoming data from request form."""
        latitude: Optional[Decimal]
        longitude: Optional[Decimal]

        if valuelist and len(valuelist) == 2:
            try:
                latitude = Decimal(valuelist[0])
            except (DecimalError, TypeError):
                latitude = None
            try:
                longitude = Decimal(valuelist[1])
            except (DecimalError, TypeError):
                longitude = None

            self.data = latitude, longitude
        else:
            self.data = None, None

    def _value(self) -> tuple[str, str]:
        """Return HTML render value."""
        if self.data is not None:
            return (
                str(self.data[0]) if self.data[0] is not None else '',
                str(self.data[1]) if self.data[1] is not None else '',
            )
        return '', ''


class RadioMatrixField(wtforms.Field):
    """
    Presents a matrix of questions (rows) and choices (columns).

    Saves each row as either an attr or a dict key on the target field in the object.
    """

    data: dict[str, Any]
    widget = RadioMatrixInput()

    def __init__(
        self,
        *args: Any,
        coerce: Callable[[Any], Any] = str,
        fields: Iterable[tuple[str, str]] = (),
        choices: Iterable[tuple[str, str]] = (),
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.coerce = coerce
        self.fields = fields
        self.choices = choices

    def process(
        self,
        formdata: MultiDict,
        data: Any = unset_value,
        extra_filters: Optional[Iterable[Callable[[Any], Any]]] = None,
    ) -> None:
        self.process_errors = []
        if data is unset_value:
            data = self.default() if callable(self.default) else self.default

        self.object_data = data

        try:
            self.process_data(data)
        except ValueError as exc:
            self.process_errors.append(exc.args[0])

        if formdata:
            raw_data = {}
            for fname, _ftitle in self.fields:
                if fname in formdata:
                    raw_data[fname] = formdata[fname]
            self.raw_data = raw_data
            self.process_formdata(raw_data)

        try:
            for filt in itertools.chain(self.filters, extra_filters or []):
                self.data = filt(self.data)
        except ValueError as exc:
            self.process_errors.append(exc.args[0])

    def process_data(self, value: Any) -> None:
        """Process incoming data from Python."""
        if value:
            self.data = {fname: getattr(value, fname) for fname, _ftitle in self.fields}
        else:
            self.data = {}

    def process_formdata(self, valuelist: dict[str, Any]) -> None:
        """Process incoming data from request form."""
        self.data = {key: self.coerce(value) for key, value in valuelist.items()}

    def populate_obj(self, obj: Any, name: str) -> None:
        # 'name' is the name of this field in the form. Ignore it for RadioMatrixField

        for fname, _ftitle in self.fields:
            if fname in self.data:
                setattr(obj, fname, self.data[fname])


_invalid_marker = object()


class EnumSelectField(SelectField):
    """
    SelectField that populates choices from a LabeledEnum.

    The LabeledEnum must use (value, name, title) tuples for all elements in the enum.
    Only name and title are exposed to the form, keeping value private.

    Takes a ``lenum`` argument instead of ``choices``::

        class MyForm(forms.Form):
            field = forms.EnumSelectField(
                __("My Field"), lenum=MY_ENUM, default=MY_ENUM.CHOICE
            )
    """

    widget = OriginalSelectWidget()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.lenum = kwargs.pop('lenum')
        kwargs['choices'] = self.lenum.nametitles()

        super().__init__(*args, **kwargs)

    def iter_choices(self) -> ReturnIterChoices:
        """Iterate over choices."""
        selected_name = self.lenum[self.data].name if self.data is not None else None
        for name, title in self.choices:
            yield (name, title, name == selected_name, {})

    def process_data(self, value: Any) -> None:
        """Process incoming data from Python."""
        if value is None:
            self.data = None
        elif value in self.lenum:
            self.data = value
        else:
            raise KeyError(_("Value not in LabeledEnum"))

    def process_formdata(self, valuelist: list[str]) -> None:
        """Process incoming data from request form."""
        if valuelist:
            try:
                value = self.lenum.value_for(self.coerce(valuelist[0]))
                if value is None:
                    value = _invalid_marker
                self.data = value
            except ValueError as exc:
                raise ValueError(
                    self.gettext('Invalid Choice: could not coerce')
                ) from exc

    def pre_validate(self, form: WTForm) -> None:
        if self.data is _invalid_marker:
            raise StopValidation(self.gettext('Not a valid choice'))


class JsonField(wtforms.TextAreaField):
    """
    A field to accept JSON input, stored internally as a Python-native type.

    ::

        class MyForm(forms.Form):
            field = forms.JsonField(__("My Field"), default={})

    The standard WTForms field arguments are accepted. Additionally:

    :param require_dict: Require a dict as the data value (default `True`)
    :param encode_kwargs: Additional arguments for :meth:`json.dumps` (default
        ``{'sort_keys': True, 'indent': 2}``)
    :param decode_kwargs: Additional arguments for :meth:`json.loads` (default ``{}``)
    """

    default_encode_kwargs: dict[str, Any] = {'sort_keys': True, 'indent': 2}
    default_decode_kwargs: dict[str, Any] = {}

    def __init__(
        self,
        *args: Any,
        require_dict: bool = True,
        encode_kwargs: Optional[dict[str, Any]] = None,
        decode_kwargs: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.require_dict = require_dict
        self.encode_args = (
            encode_kwargs if encode_kwargs is not None else self.default_encode_kwargs
        )
        self.decode_args = (
            decode_kwargs if decode_kwargs is not None else self.default_decode_kwargs
        )

    def __call__(self, *args: Any, **kwargs: Any) -> str:
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = (c + ' json').strip()
        return super().__call__(*args, **kwargs)

    def _value(self) -> str:
        """
        Render the internal Python value as a JSON string.

        Special-case `None` to return an empty string instead of a JSON ``null``.
        """
        if self.raw_data:
            # If we've received data from a form, render it as is. This allows
            # invalid JSON to be presented back to the user for correction.
            return self.raw_data[0]
        if self.data is not None:
            # Use Flask's JSON module to apply any custom JSON implementation as used
            # by the app
            return json.dumps(self.data, ensure_ascii=False, **self.encode_args)
        return ''

    def process_data(self, value: Any) -> None:
        """Process incoming data from Python."""
        if value is not None and self.require_dict and not isinstance(value, Mapping):
            raise ValueError(_("Field value must be a dictionary"))

        # TODO: Confirm this value can be rendered as JSON.
        # We're ignoring it for now because :meth:`_value` will trip on it
        # when the form is rendered, and the likelihood of this field being
        # used without being rendered is low.

        self.data = value

    def process_formdata(self, valuelist: list[str]) -> None:
        """Process incoming data from request form."""
        if valuelist:
            value = valuelist[0]
            if not value:
                self.data = self.default
                return
            # ValueError raised by this method will be captured as a field validator
            # error by WTForms
            try:
                data = json.loads(value, **self.decode_args)
            except ValueError as exc:
                raise ValueError(
                    _("Invalid JSON: {message}").format(message=exc.args[0])
                ) from None
            if self.require_dict and not isinstance(data, Mapping):
                raise ValueError(
                    _("The JSON data must be a hash object enclosed in {}")
                )
            self.data = data
