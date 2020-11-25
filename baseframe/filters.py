from six.moves.urllib.parse import urlsplit, urlunsplit
import six

from datetime import datetime, timedelta
import os

from flask import Markup, request
from flask_babelhg import get_locale

from babel.dates import format_date, format_datetime, format_time
from furl import furl
from pytz import UTC

from coaster.gfm import markdown
from coaster.utils import md5sum, text_blocks

from . import b_ as _
from . import baseframe, cache, current_app, get_timezone
from .utils import request_timestamp
from .views import ext_assets


@baseframe.app_template_filter('age')
def age(dt):
    if dt.tzinfo is None:
        dt = UTC.localize(dt)
    delta = request_timestamp() - dt
    if delta.days == 0:
        # < 1 day
        if delta.seconds < 1:
            return _("now")
        if delta.seconds < 10:
            return _("seconds ago")
        elif delta.seconds < 60:
            return _("%(num)s seconds ago", num=delta.seconds)
        elif delta.seconds < 120:
            return _("a minute ago")
        elif delta.seconds < 3600:  # < 1 hour
            return _("%(num)s minutes ago", num=int(delta.seconds / 60))
        elif delta.seconds < 7200:  # < 2 hours
            return _("an hour ago")
        else:
            return _("%(num)s hours ago", num=int(delta.seconds / 3600))
    elif delta.days == 1:
        return _("a day ago")
    elif delta.days < 30:
        return _("%(num)s days ago", num=delta.days)
    elif delta.days < 60:
        return _("a month ago")
    elif delta.days < 365:
        return _("%(num)s months ago", num=int(delta.days / 30))
    elif delta.days < 730:  # < 2 years
        return _("a year ago")
    else:
        return _("%(num)s years ago", num=int(delta.days / 365))


@baseframe.app_template_filter('initials')
def initials(text):
    """
    Return first and last initials from the given input, meant for use as avatar stand-in.
    """
    if not text:
        return ''
    parts = text.split()
    if len(parts) > 1:
        return parts[0][0] + parts[-1][0]
    elif parts:
        return parts[0][0]
    else:
        return ''


@baseframe.app_template_filter('usessl')
def usessl(url):
    """
    Convert a URL to https:// if SSL is enabled in site config
    """
    if not current_app.config.get('USE_SSL'):
        return url
    if url.startswith('//'):  # //www.example.com/path
        return 'https:' + url
    if url.startswith('/'):  # /path
        url = os.path.join(request.url_root, url[1:])
    if url.startswith('http:'):  # http://www.example.com
        url = 'https:' + url[5:]
    return url


@baseframe.app_template_filter('nossl')
def nossl(url):
    """
    Convert a URL to http:// if using SSL
    """
    if url.startswith('//'):
        return 'http:' + url
    if url.startswith('/') and request.url.startswith('https:'):  # /path and SSL is on
        url = os.path.join(request.url_root, url[1:])
    if url.startswith('https://'):
        return 'http:' + url[6:]
    return url


@baseframe.app_template_filter('avatar_url')
def avatar_url(user, size=None):
    if isinstance(size, (list, tuple)):
        size = 'x'.join(size)
    if user.avatar:
        if size:
            # TODO: Use a URL parser
            if '?' in user.avatar:
                return user.avatar + '&size=' + six.text_type(size)
            else:
                return user.avatar + '?size=' + six.text_type(size)
        else:
            return user.avatar
    email = user.email
    if email:
        if isinstance(email, six.string_types):
            # Flask-Lastuser's User model has email as a string
            ehash = md5sum(user.email)
        else:
            # Lastuser's User model has email as a UserEmail object
            ehash = email.md5sum
        gravatar = '//www.gravatar.com/avatar/' + ehash + '?d=mm'
        if size:
            gravatar += '&s=' + six.text_type(size)
        return gravatar
    # Return Gravatar's missing man image
    return '//www.gravatar.com/avatar/00000000000000000000000000000000?d=mm'


@baseframe.app_template_filter('render_field_options')
def render_field_options(field, **kwargs):
    """
    Remove HTML attributes with a value of None or False before rendering a field.
    """
    d = {k: v for k, v in kwargs.items() if v is not None and v is not False}
    if hasattr(field, 'widget_attrs'):
        d.update(field.widget_attrs)
    return field(**d)


@baseframe.app_template_filter('to_json')
def form_field_to_json(field, **kwargs):
    d = {}
    d['id'] = field.id
    d['label'] = field.label.text
    d['has_errors'] = bool(field.errors)
    d['errors'] = [{'error': e} for e in field.errors]
    d['is_listwidget'] = bool(
        hasattr(field.widget, 'html_tag') and field.widget.html_tag in ['ul', 'ol']
    )
    try:
        d['is_checkbox'] = field.widget.input_type == 'checkbox'
    except AttributeError:
        d['is_checkbox'] = False
    d['is_required'] = bool(field.flags.required)
    d['render_html'] = Markup(render_field_options(field, **kwargs))
    return d


@baseframe.app_template_filter('markdown')
def field_markdown(field):
    html = markdown(field)
    return Markup(html)


@baseframe.app_template_filter('ext_asset_url')
def ext_asset_url(asset):
    """
    This filter makes ext_assets available to templates.
    """
    if isinstance(asset, six.string_types):
        return ext_assets([asset])
    else:
        return ext_assets(asset)


@baseframe.app_template_filter('firstline')
@cache.memoize(timeout=600)
def firstline(html):
    """
    Returns the first line from a HTML blob as plain text
    """
    result = text_blocks(html)
    if result:
        return result[0]


@baseframe.app_template_filter('cdata')
def cdata(text):
    """
    Convert text to a CDATA sequence
    """
    return Markup('<![CDATA[' + text.replace(']]>', ']]]]><![CDATA[>') + ']]>')


@baseframe.app_template_filter('shortdate')
def shortdate(value):
    if isinstance(value, datetime):
        tz = get_timezone()
        if value.tzinfo is None:
            dt = UTC.localize(value).astimezone(tz)
        else:
            dt = value.astimezone(tz)
        utc_now = request_timestamp().astimezone(tz)
    else:
        dt = value
        utc_now = request_timestamp().date()
    if dt > (
        utc_now
        - timedelta(days=int(current_app.config.get('SHORTDATE_THRESHOLD_DAYS', 0)))
    ):
        return dt.strftime('%e %b')
    else:
        # The string replace hack is to deal with inconsistencies in the underlying
        # implementation of strftime. See https://bugs.python.org/issue8304
        return six.text_type(dt.strftime("%e %b '%y")).replace("'", "’")


@baseframe.app_template_filter('longdate')
def longdate(value):
    if isinstance(value, datetime):
        if value.tzinfo is None:
            dt = UTC.localize(value).astimezone(get_timezone())
        else:
            dt = value.astimezone(get_timezone())
    else:
        dt = value
    return dt.strftime('%e %B %Y')


@baseframe.app_template_filter('date')
def date_filter(value, format='medium', locale=None, usertz=True):  # NOQA: A002
    if isinstance(value, datetime) and usertz:
        if value.tzinfo is None:
            dt = UTC.localize(value).astimezone(get_timezone())
        else:
            dt = value.astimezone(get_timezone())
    else:
        dt = value
    return format_date(
        dt, format=format, locale=locale if locale else get_locale()
    )  # NOQA: A002


@baseframe.app_template_filter('time')
def time_filter(value, format='short', locale=None, usertz=True):  # NOQA: A002
    # Default format = hh:mm
    if isinstance(value, datetime) and usertz:
        if value.tzinfo is None:
            dt = UTC.localize(value).astimezone(get_timezone())
        else:
            dt = value.astimezone(get_timezone())
    else:
        dt = value
    return format_time(
        dt, format=format, locale=locale if locale else get_locale()
    )  # NOQA: A002


@baseframe.app_template_filter('datetime')
def datetime_filter(value, format='medium', locale=None, usertz=True):  # NOQA: A002
    if isinstance(value, datetime) and usertz:
        if value.tzinfo is None:
            dt = UTC.localize(value).astimezone(get_timezone())
        else:
            dt = value.astimezone(get_timezone())
    else:
        dt = value
    return format_datetime(
        dt, format=format, locale=locale if locale else get_locale()
    )  # NOQA: A002


@baseframe.app_template_filter('timestamp')
def timestamp_filter(value):
    if isinstance(value, datetime):
        if six.PY2:
            ts = (value - datetime(1970, 1, 1)).total_seconds()
        else:
            ts = value.timestamp()
    else:
        ts = value
    return ts


@baseframe.app_template_filter('cleanurl')
def cleanurl_filter(url):
    if not isinstance(url, furl):
        url = furl(url)
    url.path.normalize()
    netloc = url.netloc.lstrip('www.') if url.netloc else url.netloc
    return furl().set(netloc=netloc, path=url.path).url.lstrip('//').rstrip('/')


@baseframe.app_template_filter('make_relative_url')
def make_relative_url(url):
    """Filter to discard scheme and netloc from a URL, used to undo _external=True"""
    return urlunsplit(urlsplit(url)._replace(scheme='', netloc=''))
