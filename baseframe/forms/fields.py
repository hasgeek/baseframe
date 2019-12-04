# -*- coding: utf-8 -*-

from six.moves.urllib.parse import urljoin
import six

from decimal import Decimal
from decimal import InvalidOperation as DecimalError

from flask import current_app
from flask_wtf import RecaptchaField
from wtforms.compat import text_type
from wtforms.fields import FileField
from wtforms.fields import SelectField as SelectFieldBase
from wtforms.fields import SelectMultipleField, SubmitField
from wtforms.utils import unset_value
from wtforms.widgets import Select as OriginalSelectWidget
import wtforms

from pytz import UTC
from pytz import timezone as pytz_timezone
import bleach
import simplejson as json

from .. import _, get_timezone
from ..utils import request_timestamp
from .parsleyjs import StringField, TextAreaField, URLField
from .widgets import (
    CoordinatesInput,
    DateTimeInput,
    RadioMatrixInput,
    Select2Widget,
    SelectWidget,
    TinyMce3,
    TinyMce4,
)

__all__ = [
    # Imported from WTForms
    'FileField',
    'SelectMultipleField',
    'SubmitField',
    'RecaptchaField',
    # Baseframe fields (many of these are extensions of WTForms fields)
    'AnnotatedTextField',
    'AutocompleteField',
    'AutocompleteMultipleField',
    'CoordinatesField',
    'DateTimeField',
    'EnumSelectField',
    'FormField',
    'GeonameSelectField',
    'GeonameSelectMultiField',
    'ImgeeField',
    'JsonField',
    'MarkdownField',
    'RadioMatrixField',
    'RichTextField',
    'SANITIZE_ATTRIBUTES',
    'SANITIZE_TAGS',
    'SelectField',
    'StylesheetField',
    'TextListField',
    'TinyMce3Field',
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


# This class borrowed from https://github.com/industrydive/wtforms_extended_selectfield
class SelectField(SelectFieldBase):
    """
    Add support of ``optgroup`` grouping to default WTForms's ``SelectField`` class.
    Here is an example of how the data is laid out.
        (
            ("Fruits", (
                ('apple', "Apple"),
                ('peach', "Peach"),
                ('pear', "Pear")
            )),
            ("Vegetables", (
                ('cucumber', "Cucumber"),
                ('potato', "Potato"),
                ('tomato', "Tomato"),
            )),
            ('other', "None of the above")
        )
    It's a little strange that the tuples are (value, label) except for groups which are (Group Label, list of tuples)
    but this is actually how Django does it too https://docs.djangoproject.com/en/dev/ref/models/fields/#choices
    """

    widget = SelectWidget()

    def pre_validate(self, form):
        """
        Don't forget to also validate values from embedded lists.
        """
        for item1, item2 in self.choices:
            if isinstance(item2, (list, tuple)):
                # group_label = item1
                group_items = item2
                for val, label in group_items:
                    if val == self.data:
                        return
            else:
                val = item1
                # label = item2
                if val == self.data:
                    return
        raise ValueError(_("Not a valid choice!"))


class TinyMce3Field(TextAreaField):
    """
    Rich text field using TinyMCE 3.
    """

    widget = TinyMce3()

    def __init__(
        self,
        # WTForms fields
        label=u'',
        validators=None,
        filters=(),
        description=u'',
        id=None,  # NOQA: A002
        default=None,
        widget=None,
        _form=None,
        _name=None,
        _prefix='',
        # Additional fields
        content_css=None,
        linkify=True,
        nofollow=True,
        tinymce_options=None,
        sanitize_tags=None,
        sanitize_attributes=None,
        **kwargs
    ):

        super(TinyMce3Field, self).__init__(
            label=label,
            validators=validators,
            filters=filters,
            description=description,
            id=id,
            default=default,
            widget=widget,
            _form=_form,
            _name=_name,
            _prefix=_prefix,
            **kwargs
        )

        if tinymce_options is None:
            tinymce_options = {}
        else:
            # Clone the dict to preserve local edits
            tinymce_options = dict(tinymce_options)

        # Set defaults for TinyMCE
        tinymce_options.setdefault('theme', 'advanced')
        tinymce_options.setdefault('plugins', '')
        tinymce_options.setdefault(
            'theme_advanced_buttons1',
            'bold,italic,|,sup,sub,|,bullist,numlist,|,link,unlink,|,blockquote,|,removeformat,code',
        )
        tinymce_options.setdefault('theme_advanced_buttons2', '')
        tinymce_options.setdefault('theme_advanced_buttons3', '')
        tinymce_options.setdefault('blockformats', 'p,h3,h4,h5,h6,blockquote,dt,dd')
        tinymce_options.setdefault('width', '100%')
        tinymce_options.setdefault('height', '159')
        tinymce_options.setdefault(
            'valid_elements',
            'p,br,strong/b,em/i,sup,sub,h3,h4,h5,h6,ul,ol,li,a[!href|title|target],blockquote,code',
        )
        tinymce_options.setdefault('theme_advanced_toolbar_location', 'top')
        tinymce_options.setdefault('theme_advanced_toolbar_align', 'left')
        tinymce_options.setdefault('theme_advanced_statusbar_location', 'bottom')
        tinymce_options.setdefault('theme_advanced_resizing', True)
        tinymce_options.setdefault('theme_advanced_path', False)
        tinymce_options.setdefault('relative_urls', False)

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
    def content_css(self):
        if callable(self._content_css):
            return self._content_css()
        else:
            return self._content_css

    def process_formdata(self, valuelist):
        super(TinyMce3Field, self).process_formdata(valuelist)
        # Sanitize data
        self.data = bleach.clean(
            self.data,
            strip=True,
            tags=self.sanitize_tags,
            attributes=self.sanitize_attributes,
        )
        if self.linkify:
            if self.nofollow:
                self.data = bleach.linkify(self.data)
            else:
                self.data = bleach.linkify(self.data, callbacks=[])


class TinyMce4Field(TextAreaField):
    """
    Rich text field using TinyMCE 4.
    """

    widget = TinyMce4()

    def __init__(
        self,
        # WTForms fields
        label=u'',
        validators=None,
        filters=(),
        description=u'',
        id=None,  # NOQA: A002
        default=None,
        widget=None,
        _form=None,
        _name=None,
        _prefix='',
        # Additional fields
        content_css=None,
        linkify=True,
        nofollow=True,
        tinymce_options=None,
        sanitize_tags=None,
        sanitize_attributes=None,
        **kwargs
    ):

        super(TinyMce4Field, self).__init__(
            label=label,
            validators=validators,
            filters=filters,
            description=description,
            id=id,
            default=default,
            widget=widget,
            _form=_form,
            _name=_name,
            _prefix=_prefix,
            **kwargs
        )

        if tinymce_options is None:
            tinymce_options = {}
        else:
            # Clone the dict to preserve local edits
            tinymce_options = dict(tinymce_options)

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
            'p,br,strong/b,em/i,sup,sub,h3,h4,h5,h6,ul,ol,li,a[!href|title|target],blockquote,code',
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
    def content_css(self):
        if callable(self._content_css):
            return self._content_css()
        else:
            return self._content_css

    def process_formdata(self, valuelist):
        super(TinyMce4Field, self).process_formdata(valuelist)
        # Sanitize data
        self.data = bleach.clean(
            self.data,
            strip=True,
            tags=self.sanitize_tags,
            attributes=self.sanitize_attributes,
        )
        if self.linkify:
            if self.nofollow:
                self.data = bleach.linkify(self.data)
            else:
                self.data = bleach.linkify(self.data, callbacks=[])


#: Compatibility name
RichTextField = TinyMce3Field


class DateTimeField(wtforms.fields.DateTimeField):
    """
    A text field which stores a `datetime.datetime` matching a format.

    :param str label: Label to display against the field
    :param list validators: List of validators
    :param str format: Datetime format string
    :param str timezone: Timezone used for user input
    :param bool naive: If `True` (default), timezone info is stripped from the return data
    """

    widget = DateTimeInput()

    def __init__(
        self,
        label=None,
        validators=None,
        format='%Y-%m-%d %H:%M',  # NOQA: A002
        timezone=None,
        naive=True,
        **kwargs
    ):
        super(DateTimeField, self).__init__(label, validators, **kwargs)
        self.format = format
        self.timezone = timezone() if callable(timezone) else timezone
        self.naive = naive
        self._timezone_converted = None

    @property
    def timezone(self):
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        if value is None:
            value = get_timezone()
        if isinstance(value, six.string_types):
            self.tz = pytz_timezone(value)
            self._timezone = value
        else:
            self.tz = value
            self._timezone = self.tz.zone

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

        now = request_timestamp().astimezone(self.tz)
        self.tzname = now.tzname()
        self.is_dst = bool(now.dst())

    def _value(self):
        if self.data:
            if self.data.tzinfo is None:
                # We got a naive datetime from the calling app. Assume UTC
                data = UTC.localize(self.data).astimezone(self.tz)
            else:
                # We got a tz-aware datetime. Cast into the required timezone
                data = self.data.astimezone(self.tz)
            value = data.strftime(self.format)
        else:
            value = ''
        return value

    def process_formdata(self, valuelist):
        # We received a naive timestamp from the browser. Save it
        super(DateTimeField, self).process_formdata(valuelist)
        # The received timestamp hasn't been localized to the expected timezone yet
        self._timezone_converted = False

    def pre_validate(self, form):
        if self.data and self._timezone_converted is False:
            # Convert from user timezone back to UTC
            self.data = self.tz.localize(self.data, is_dst=self.is_dst).astimezone(UTC)
            # If the app wanted a naive datetime, strip the timezone info
            if self.naive:
                self.data = self.data.replace(tzinfo=None)
            self._timezone_converted = True


class TextListField(wtforms.fields.TextAreaField):
    """
    A list field that renders as a textarea with one line per list item.
    """

    def _value(self):
        if self.data:
            return u'\r\n'.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            self.data = [
                x
                for x in valuelist[0]
                .replace('\r\n', '\n')
                .replace('\r', '\n')
                .split('\n')
            ]
        else:
            self.data = []


class UserSelectFieldBase(object):
    """
    Select a user
    """

    def __init__(self, *args, **kwargs):
        self.lastuser = kwargs.pop('lastuser', current_app.login_manager)
        self.usermodel = kwargs.pop(
            'usermodel', self.lastuser.usermanager.usermodel if self.lastuser else None
        )
        self.separator = kwargs.pop('separator', ',')
        if self.lastuser:
            self.autocomplete_endpoint = self.lastuser.endpoint_url(
                current_app.lastuser_config['getuser_autocomplete_endpoint']
            )
            self.getuser_endpoint = self.lastuser.endpoint_url(
                current_app.lastuser_config['getuser_userids_endpoint']
            )
        else:
            self.autocomplete_endpoint = kwargs.pop('autocomplete_endpoint')()
            self.getuser_endpoint = kwargs.pop('getuser_endpoint')()
        super(UserSelectFieldBase, self).__init__(*args, **kwargs)

    def iter_choices(self):
        if self.data:
            return [(u.userid, u.pickername, True) for u in self.data]

    def process_formdata(self, valuelist):
        retval = super(UserSelectFieldBase, self).process_formdata(valuelist)
        userids = valuelist
        # Convert strings in userids into User objects
        users = []
        if userids:
            if self.lastuser:
                usersdata = self.lastuser.getuser_by_userids(userids)
                # TODO: Move all of this inside the getuser method with user=True, create=True
                for userinfo in usersdata:
                    if userinfo['type'] == 'user':
                        user = self.usermodel.query.filter_by(
                            userid=userinfo['buid']
                        ).first()
                        if not user:
                            # New user in this app. Don't set username right now. It's not relevant
                            # until first login and we don't want to deal with conflicts.
                            # We don't add this user to the session. The view is responsible for that
                            # (using SQLAlchemy cascades when assigning users to a collection)
                            user = self.usermodel(
                                userid=userinfo['buid'], fullname=userinfo['title']
                            )
                        users.append(user)
            else:
                users = self.usermodel.all(userids=userids)
        self.data = users
        return retval


class UserSelectField(UserSelectFieldBase, StringField):
    """
    Render a user select field that allows one user to be selected.
    """

    multiple = False
    widget = Select2Widget()

    def _value(self):
        if self.data:
            return self.data.userid
        else:
            return ''

    def iter_choices(self):
        if self.data:
            return [(self.data.userid, self.data.pickername, True)]

    def process_formdata(self, valuelist):
        retval = super(UserSelectField, self).process_formdata(valuelist)
        if self.data:
            self.data = self.data[0]
        else:
            self.data = None
        return retval


class UserSelectMultiField(UserSelectFieldBase, StringField):
    """
    Render a user select field that allows multiple users to be selected.
    """

    multiple = True
    widget = Select2Widget()


class AutocompleteFieldBase(object):
    """
    Autocomplete a field.
    """

    def __init__(self, *args, **kwargs):
        self.autocomplete_endpoint = kwargs.pop('autocomplete_endpoint')
        self.results_key = kwargs.pop('results_key', 'results')
        self.separator = kwargs.pop('separator', ',')
        super(AutocompleteFieldBase, self).__init__(*args, **kwargs)
        self.choices = ()  # Disregard server-side choices

    def iter_choices(self):
        if self.data:
            return [(six.text_type(u), six.text_type(u), True) for u in self.data]

    def process_formdata(self, valuelist):
        retval = super(AutocompleteFieldBase, self).process_formdata(valuelist)
        # Convert strings into Tag objects
        self.data = valuelist
        return retval

    def pre_validate(self, form):
        """Do not validate data"""
        return


class AutocompleteField(AutocompleteFieldBase, StringField):
    """
    Select field that sources choices from a JSON API endpoint.
    Does not validate choices server-side.
    """

    multiple = False
    widget = Select2Widget()

    def _value(self):
        if self.data:
            return self.data
        else:
            return None

    def process_formdata(self, valuelist):
        retval = super(AutocompleteField, self).process_formdata(valuelist)
        if self.data:
            self.data = self.data[0]
        else:
            self.data = None
        return retval


class AutocompleteMultipleField(AutocompleteFieldBase, StringField):
    """
    Multiple select field that sources choices from a JSON API endpoint.
    Does not validate choices server-side.
    """

    multiple = True
    widget = Select2Widget()


class GeonameSelectFieldBase(object):
    """
    Select a geoname location
    """

    def __init__(self, *args, **kwargs):
        self.separator = kwargs.pop('separator', ',')
        server = current_app.config.get('HASCORE_SERVER', 'https://api.hasgeek.com/')
        self.autocomplete_endpoint = urljoin(server, '/1/geo/autocomplete')
        self.getname_endpoint = urljoin(server, '/1/geo/get_by_names')

        super(GeonameSelectFieldBase, self).__init__(*args, **kwargs)

    def iter_choices(self):
        if self.data:
            return [(six.text_type(u), six.text_type(u), True) for u in self.data]

    def process_formdata(self, valuelist):
        retval = super(GeonameSelectFieldBase, self).process_formdata(valuelist)
        # Convert strings into GeoName objects
        self.data = valuelist
        return retval


class GeonameSelectField(GeonameSelectFieldBase, StringField):
    """
    Render a geoname select field that allows one geoname to be selected.
    """

    multiple = False
    widget = Select2Widget()

    def _value(self):
        if self.data:
            return self.data.geonameid
        else:
            return None

    def process_formdata(self, valuelist):
        retval = super(GeonameSelectField, self).process_formdata(valuelist)
        if self.data:
            self.data = self.data[0]
        else:
            self.data = None
        return retval


class GeonameSelectMultiField(GeonameSelectFieldBase, StringField):
    """
    Render a geoname select field that allows multiple geonames to be selected.
    """

    multiple = True
    widget = Select2Widget()


class AnnotatedTextField(StringField):
    """
    Text field with prefix and suffix annotations.
    """

    def __init__(self, *args, **kwargs):
        self.prefix = kwargs.pop('prefix', None)
        self.suffix = kwargs.pop('suffix', None)
        super(AnnotatedTextField, self).__init__(*args, **kwargs)


class MarkdownField(TextAreaField):
    """
    TextArea field which has class='markdown'.
    """

    def __call__(self, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = "%s %s" % (c, 'markdown') if c else 'markdown'
        return super(MarkdownField, self).__call__(**kwargs)


class StylesheetField(wtforms.TextAreaField):
    """
    TextArea field which has class='stylesheet'.
    """

    def __call__(self, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = "%s %s" % (c, 'stylesheet') if c else 'stylesheet'
        return super(StylesheetField, self).__call__(**kwargs)


class ImgeeField(URLField):
    """
    A URLField which lets the user choose an image from Imgee. The field is filled
    with the url of the image chosen.

    Example usage:
    image = ImgeeField(label='Logo', description='Your company logo here',
            validators=[validators.DataRequired()],
            profile='foo', img_label='logos', img_size='100x75')
        )
    """

    def __init__(
        self,
        label='',
        validators=None,
        profile=None,
        img_label=None,
        img_size=None,
        **kwargs
    ):
        super(ImgeeField, self).__init__(label, validators, **kwargs)
        self.profile = profile
        self.img_label = img_label
        self.img_size = img_size

    def __call__(self, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = (
            "%s %s" % (c.strip(), 'imgee-url-holder') if c else 'imgee-url-holder'
        ).strip()
        if self.profile:
            kwargs['data-profile'] = (
                self.profile() if callable(self.profile) else self.profile
            )
        if self.img_label:
            kwargs['data-img-label'] = self.img_label
        if self.img_size:
            kwargs['data-img-size'] = self.img_size
        return super(ImgeeField, self).__call__(**kwargs)


class FormField(wtforms.FormField):
    """
    FormField that removes CSRF in sub-forms.
    """

    def process(self, *args, **kwargs):
        retval = super(FormField, self).process(*args, **kwargs)
        if hasattr(self.form, 'csrf_token'):
            del self.form.csrf_token
        return retval


class CoordinatesField(wtforms.Field):
    """
    Adds latitude and longitude fields and returns them as a tuple.
    """

    widget = CoordinatesInput()

    def process_formdata(self, valuelist):
        if valuelist and len(valuelist) == 2:
            try:
                latitude = Decimal(valuelist[0])
            except DecimalError:
                latitude = None
            try:
                longitude = Decimal(valuelist[1])
            except DecimalError:
                longitude = None

            self.data = latitude, longitude
        else:
            self.data = None, None

    def _value(self):
        if self.data is not None and self.data != (None, None):
            return text_type(self.data[0]), text_type(self.data[1])
        else:
            return '', ''


class RadioMatrixField(wtforms.Field):
    """
    Presents a matrix of questions (rows) and choices (columns). Saves each row as either
    an attr or a dict key on the target field in the object.
    """

    widget = RadioMatrixInput()

    def __init__(
        self,
        label=None,
        validators=None,
        coerce=text_type,  # NOQA: A002
        fields=(),
        choices=(),
        **kwargs
    ):
        super(RadioMatrixField, self).__init__(label, validators, **kwargs)
        self.coerce = coerce
        self.fields = fields
        self.choices = choices
        self._obj = None

    def process(self, formdata, data=unset_value):
        self.process_errors = []
        if data is unset_value:
            try:
                data = self.default()
            except TypeError:
                data = self.default

        self.object_data = data

        try:
            self.process_data(data)
        except ValueError as e:
            self.process_errors.append(e.args[0])

        if formdata:
            raw_data = {}
            for fname, ftitle in self.fields:
                if fname in formdata:
                    raw_data[fname] = formdata[fname]
            self.raw_data = raw_data
            self.process_formdata(raw_data)

        try:
            for filt in self.filters:
                self.data = filt(self.data)
        except ValueError as e:
            self.process_errors.append(e.args[0])

    def process_data(self, data):
        if data:
            self.data = {fname: getattr(data, fname) for fname, ftitle in self.fields}
        else:
            self.data = {}

    def process_formdata(self, raw_data):
        self.data = {key: self.coerce(value) for key, value in raw_data.items()}

    def populate_obj(self, obj, name):
        # 'name' is the name of this field in the form. Ignore it for RadioMatrixField

        for fname, ftitle in self.fields:
            if fname in self.data:
                setattr(obj, fname, self.data[fname])


_invalid_marker = object()


class EnumSelectField(SelectField):
    """
    SelectField that populates choices from a LabeledEnum that uses
    (value, name, title) tuples for all elements in the enum. Only name and
    title are exposed to the form, keeping value private.

    Takes a ``lenum`` argument instead of ``choices``::

        class MyForm(forms.Form):
            field = forms.EnumSelectField(__("My Field"), lenum=MY_ENUM, default=MY_ENUM.CHOICE)

    """

    widget = OriginalSelectWidget()

    def __init__(self, *args, **kwargs):
        self.lenum = kwargs.pop('lenum')
        kwargs['choices'] = self.lenum.nametitles()

        super(EnumSelectField, self).__init__(*args, **kwargs)

    def iter_choices(self):
        selected_name = self.lenum[self.data].name if self.data is not None else None
        for name, title in self.choices:
            yield (name, title, name == selected_name)

    def process_data(self, value):
        if value is None:
            self.data = None
        elif value in self.lenum:
            self.data = value
        else:
            raise KeyError(_("Value not in LabeledEnum"))

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                value = self.lenum.value_for(self.coerce(valuelist[0]))
                if value is None:
                    value = _invalid_marker
                self.data = value
            except ValueError:
                raise ValueError(self.gettext('Invalid Choice: could not coerce'))

    def pre_validate(self, form):
        if self.data is _invalid_marker:
            raise ValueError(self.gettext('Not a valid choice'))


class JsonField(wtforms.TextAreaField):
    """
    A field to accept JSON input, stored internally as a Python-native type.
    By default, requires the JSON root object to be a dictionary/hash.

    ::

        class MyForm(forms.Form):
            field = forms.JsonField(__("My Field"), default={})

    :param str label: Field label
    :param list validators: List of field validators, passed on to WTForms
    :param bool require_dict: Require a dictionary as the data value (default `True`)
    :param book use_decimal: Use decimals instead of floats (default `True`)
    :param kwargs: Additional field arguments, passed on to WTForms
    """

    prettyprint_args = {'sort_keys': True, 'indent': 2}

    def __init__(
        self, label='', validators=None, require_dict=True, use_decimal=True, **kwargs
    ):
        self.require_dict = require_dict
        self.use_decimal = use_decimal
        super(JsonField, self).__init__(label, validators, **kwargs)

    def _value(self):
        """
        Render the internal Python value as a JSON string.
        Specialcase `None` to return an empty string instead of a JSON ``null``.
        """
        if self.raw_data:
            # If we've received data from a form, render it as is. This allows
            # invalid JSON to be presented back to the user for correction.
            return self.raw_data[0]
        elif self.data is not None:
            return json.dumps(
                self.data,
                use_decimal=self.use_decimal,
                ensure_ascii=False,
                **self.prettyprint_args
            )
        return u''

    def process_data(self, value):
        if value is not None and self.require_dict and not isinstance(value, dict):
            raise ValueError(_("Field value must be a dictionary"))

        # TODO: Confirm this value can be rendered as JSON.
        # We're ignoring it for now because :meth:`_value` will trip on it
        # when the form is rendered, and the likelihood of this field being
        # used without being rendered is low.

        self.data = value

    def process_formdata(self, valuelist):
        if valuelist:
            value = valuelist[0]
            if not value:
                self.data = self.default
                return
            try:
                data = json.loads(value, use_decimal=self.use_decimal)
            except ValueError as e:
                raise ValueError(_("Invalid JSON: {0!r}").format(e))
            if self.require_dict:
                if not isinstance(data, dict):
                    raise ValueError(_("The JSON root must be a hash object"))
            self.data = data
