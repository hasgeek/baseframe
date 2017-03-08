# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal, InvalidOperation as DecimalError
from urlparse import urljoin
from pytz import utc, timezone as pytz_timezone
from flask import current_app
import wtforms
from wtforms.fields import SelectField as SelectFieldBase, SelectMultipleField, SubmitField, FileField
from wtforms.compat import text_type
from wtforms.utils import unset_value
import bleach

from .. import _, get_timezone
from .widgets import TinyMce3, TinyMce4, DateTimeInput, HiddenInput, CoordinatesInput, RadioMatrixInput, SelectWidget
from .parsleyjs import TextAreaField, StringField, URLField

__all__ = ['SANITIZE_TAGS', 'SANITIZE_ATTRIBUTES',
    'TinyMce3Field', 'TinyMce4Field', 'RichTextField', 'DateTimeField', 'HiddenMultiField', 'TextListField',
    'AnnotatedTextField', 'MarkdownField', 'StylesheetField', 'ImgeeField',
    'FormField', 'UserSelectField', 'UserSelectMultiField', 'GeonameSelectField', 'GeonameSelectMultiField',
    'CoordinatesField', 'RadioMatrixField', 'AutocompleteField', 'AutocompleteMultipleField', 'SelectField',
    # Imported from WTForms:
    'SelectMultipleField', 'SubmitField', 'FileField']


# Default tags and attributes to allow in HTML sanitization
SANITIZE_TAGS = ['p', 'br', 'strong', 'em', 'sup', 'sub', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'a',
    'blockquote', 'code']
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

    def __init__(self,
            # WTForms fields
            label=u'',
            validators=None,
            filters=(),
            description=u'',
            id=None,
            default=None,
            widget=None,
            _form=None,
            _name=None,
            _prefix='',

            # Additional fields
            content_css=None,
            linkify=True, nofollow=True,
            tinymce_options=None,
            sanitize_tags=None, sanitize_attributes=None, **kwargs):

        super(TinyMce3Field, self).__init__(label=label, validators=validators, filters=filters,
            description=description, id=id, default=default, widget=widget, _form=_form, _name=_name,
            _prefix=_prefix, **kwargs)

        if tinymce_options is None:
            tinymce_options = {}
        else:
            # Clone the dict to preserve local edits
            tinymce_options = dict(tinymce_options)

        # Set defaults for TinyMCE
        tinymce_options.setdefault('theme', "advanced")
        tinymce_options.setdefault('plugins', "")
        tinymce_options.setdefault('theme_advanced_buttons1',
            "bold,italic,|,sup,sub,|,bullist,numlist,|,link,unlink,|,blockquote,|,removeformat,code")
        tinymce_options.setdefault('theme_advanced_buttons2', "")
        tinymce_options.setdefault('theme_advanced_buttons3', "")
        tinymce_options.setdefault('blockformats', "p,h3,h4,h5,h6,blockquote,dt,dd")
        tinymce_options.setdefault('width', "100%")
        tinymce_options.setdefault('height', "159")
        tinymce_options.setdefault('valid_elements',
            "p,br,strong/b,em/i,sup,sub,h3,h4,h5,h6,ul,ol,li,a[!href|title|target],blockquote,code")
        tinymce_options.setdefault('theme_advanced_toolbar_location', "top")
        tinymce_options.setdefault('theme_advanced_toolbar_align', "left")
        tinymce_options.setdefault('theme_advanced_statusbar_location', "bottom")
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
        self.data = bleach.clean(self.data, strip=True,
            tags=self.sanitize_tags,
            attributes=self.sanitize_attributes)
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

    def __init__(self,
            # WTForms fields
            label=u'',
            validators=None,
            filters=(),
            description=u'',
            id=None,
            default=None,
            widget=None,
            _form=None,
            _name=None,
            _prefix='',

            # Additional fields
            content_css=None,
            linkify=True, nofollow=True,
            tinymce_options=None,
            sanitize_tags=None, sanitize_attributes=None, **kwargs):

        super(TinyMce4Field, self).__init__(label=label, validators=validators, filters=filters,
            description=description, id=id, default=default, widget=widget, _form=_form, _name=_name,
            _prefix=_prefix, **kwargs)

        if tinymce_options is None:
            tinymce_options = {}
        else:
            # Clone the dict to preserve local edits
            tinymce_options = dict(tinymce_options)

        # Set defaults for TinyMCE
        tinymce_options.setdefault('plugins', "autolink autoresize link lists paste searchreplace")
        tinymce_options.setdefault('toolbar', "bold italic | bullist numlist | link unlink | searchreplace undo redo")
        tinymce_options.setdefault('width', "100%")
        tinymce_options.setdefault('height', "400")
        tinymce_options.setdefault('valid_elements',
            "p,br,strong/b,em/i,sup,sub,h3,h4,h5,h6,ul,ol,li,a[!href|title|target],blockquote,code")
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
        self.data = bleach.clean(self.data, strip=True,
            tags=self.sanitize_tags,
            attributes=self.sanitize_attributes)
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
    """
    widget = DateTimeInput()

    def __init__(self, label=None, validators=None,
            format='%Y-%m-%d %H:%M', timezone=None, **kwargs):
        super(DateTimeField, self).__init__(label, validators, **kwargs)
        self.format = format
        self.timezone = timezone() if callable(timezone) else timezone
        self._timezone_converted = None

    @property
    def timezone(self):
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        if value is None:
            value = get_timezone()
        if isinstance(value, basestring):
            self.tz = pytz_timezone(value)
            self._timezone = value
        else:
            self.tz = value
            self._timezone = self.tz.zone
        now = utc.localize(datetime.utcnow()).astimezone(self.tz)
        self.tzname = now.tzname()
        self.is_dst = bool(now.dst())

    def _value(self):
        if self.data:
            if self.data.tzinfo is None:
                # We got a naive datetime from the calling app. Assume UTC
                data = self.tz.normalize(utc.localize(self.data).astimezone(self.tz))
            else:
                # We got a tz-aware datetime. Cast into the required timezone
                data = self.tz.normalize(self.data.astimezone(self.tz))
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
        if self._timezone_converted is False:
            # Convert from user timezone back to UTC, then discard tzinfo
            self.data = self.tz.localize(self.data, is_dst=self.is_dst).astimezone(utc).replace(tzinfo=None)
            self._timezone_converted = True


class HiddenMultiField(wtforms.fields.StringField):
    """
    A hidden field that stores multiple comma-separated values, meant to be
    used as an Ajax widget target. The optional ``separator`` parameter
    can be used to specify an alternate separator character (default ``','``).
    """
    widget = HiddenInput()

    def __init__(self, *args, **kwargs):
        self.separator = kwargs.pop('separator', ',')
        super(HiddenMultiField, self).__init__(*args, **kwargs)

    def _value(self):
        if self.data:
            return self.separator.join(self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        retval = super(HiddenMultiField, self).process_formdata(valuelist)
        if not self.data:
            self.data = []  # Calling ''.split(',') will give us [''] which is not "falsy"
        else:
            self.data = self.data.split(self.separator)
        return retval


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
            self.data = [x for x in valuelist[0].replace('\r\n', '\n').replace('\r', '\n').split('\n')]
        else:
            self.data = []


class UserSelectFieldBase(object):
    """
    Select a user
    """
    def __init__(self, *args, **kwargs):
        self.usermodel = kwargs.pop('usermodel')
        self.lastuser = kwargs.pop('lastuser')
        self.separator = kwargs.pop('separator', ',')
        if self.lastuser:
            self.autocomplete_endpoint = self.lastuser.endpoint_url(self.lastuser.getuser_autocomplete_endpoint)
            self.getuser_endpoint = self.lastuser.endpoint_url(self.lastuser.getuser_userids_endpoint)
        else:
            self.autocomplete_endpoint = kwargs.pop('autocomplete_endpoint')()
            self.getuser_endpoint = kwargs.pop('getuser_endpoint')()
        super(UserSelectFieldBase, self).__init__(*args, **kwargs)

    def _value(self):
        if self.data:
            return self.separator.join([u.userid for u in self.data])
        else:
            return ''

    def process_formdata(self, valuelist):
        retval = super(UserSelectFieldBase, self).process_formdata(valuelist)
        if self.data:
            userids = self.data.split(self.separator)
        else:
            userids = []  # Calling ''.split(',') will give us [''] which is an invalid userid
        # Convert strings in userids into User objects
        users = []
        if userids:
            if self.lastuser:
                usersdata = self.lastuser.getuser_by_userids(userids)
                # TODO: Move all of this inside the getuser method with user=True, create=True
                for userinfo in usersdata:
                    if userinfo['type'] == 'user':
                        user = self.usermodel.query.filter_by(userid=userinfo['buid']).first()
                        if not user:
                            # New user in this app. Don't set username right now. It's not relevant
                            # until first login and we don't want to deal with conflicts.
                            # We don't add this user to the session. The view is responsible for that
                            # (using SQLAlchemy cascades when assigning users to a collection)
                            user = self.usermodel(userid=userinfo['buid'], fullname=userinfo['title'])
                        users.append(user)
            else:
                users = self.usermodel.all(userids=userids)

        self.data = users
        return retval


class UserSelectField(UserSelectFieldBase, StringField):
    """
    Render a user select field that allows one user to be selected.
    """
    widget = HiddenInput()
    multiple = False

    def _value(self):
        if self.data:
            return self.data.userid
        else:
            return ''

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
    widget = HiddenInput()
    multiple = True


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

    def pre_validate(self, form):
        """Do not validate data"""
        return


class AutocompleteField(AutocompleteFieldBase, StringField):
    """
    Select field that sources choices from a JSON API endpoint.
    Does not validate choices server-side.
    """
    widget = HiddenInput()
    multiple = False


class AutocompleteMultipleField(AutocompleteFieldBase, StringField):
    """
    Multiple select field that sources choices from a JSON API endpoint.
    Does not validate choices server-side.
    """
    widget = HiddenInput()
    multiple = True

    def _value(self):
        if self.data:
            return self.separator.join(self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        retval = super(AutocompleteMultipleField, self).process_formdata(valuelist)
        if self.data:
            self.data = self.data.split(self.separator)
        else:
            self.data = []  # Calling ''.split(',') will give us [''] which is an invalid userid
        return retval


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

    def _value(self):
        if self.data:
            return self.separator.join([unicode(l) for l in self.data])
        else:
            return ''

    def process_formdata(self, valuelist):
        retval = super(GeonameSelectFieldBase, self).process_formdata(valuelist)
        if self.data:
            geonameids = self.data.split(self.separator)
        else:
            geonameids = []  # Calling ''.split(',') will give us [''] which is an invalid geonameid
        self.data = geonameids
        return retval


class GeonameSelectField(GeonameSelectFieldBase, StringField):
    """
    Render a geoname select field that allows one geoname to be selected.
    """
    widget = HiddenInput()

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
    widget = HiddenInput()


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
    def __init__(self, label='', validators=None, profile=None, img_label=None, img_size=None, **kwargs):
        super(ImgeeField, self).__init__(label, validators, **kwargs)
        self.profile = profile
        self.img_label = img_label
        self.img_size = img_size

    def __call__(self, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = ("%s %s" % (c.strip(), 'imgee-url-holder') if c else 'imgee-url-holder').strip()
        if self.profile:
            kwargs['data-profile'] = self.profile() if callable(self.profile) else self.profile
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

    def __init__(self, label=None, validators=None, coerce=text_type, fields=(), choices=(), **kwargs):
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
            for filter in self.filters:
                self.data = filter(self.data)
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
