from datetime import date, datetime, time, timedelta
from typing import Any, List, Tuple, Union
from urllib.parse import urlsplit, urlunsplit
import os.path

from flask import current_app, request
from flask_babelhg import Locale, get_locale
from markupsafe import Markup

from babel.dates import format_date, format_datetime, format_time, format_timedelta
from furl import furl
from pytz import utc
import grapheme

from coaster.gfm import markdown
from coaster.utils import compress_whitespace, md5sum, text_blocks

from .blueprint import baseframe
from .extensions import DEFAULT_LOCALE, _, cache
from .utils import get_timezone, request_timestamp
from .views import ext_assets


@baseframe.app_template_filter('age')
def age(dt: datetime) -> str:
    """Render a datetime as an age from present time."""
    if dt.tzinfo is None:
        dt = utc.localize(dt)
    delta = request_timestamp() - dt
    if delta.days == 0:
        # < 1 day
        if delta.seconds < 1:
            return _("now")
        if delta.seconds < 10:
            return _("seconds ago")
        if delta.seconds < 60:
            return _("%(num)s seconds ago", num=delta.seconds)
        if delta.seconds < 120:
            return _("a minute ago")
        if delta.seconds < 3600:  # < 1 hour
            return _("%(num)s minutes ago", num=int(delta.seconds / 60))
        if delta.seconds < 7200:  # < 2 hours
            return _("an hour ago")
        return _("%(num)s hours ago", num=int(delta.seconds / 3600))
    if delta.days == 1:
        return _("a day ago")
    if delta.days < 30:
        return _("%(num)s days ago", num=delta.days)
    if delta.days < 60:
        return _("a month ago")
    if delta.days < 365:
        return _("%(num)s months ago", num=int(delta.days / 30))
    if delta.days < 730:  # < 2 years
        return _("a year ago")
    return _("%(num)s years ago", num=int(delta.days / 365))


@baseframe.app_template_filter('initials')
def initials(text: str) -> str:
    """Return up to two initials from the given string, for a default avatar image."""
    if not text:
        return ''
    parts = text.split()
    if len(parts) > 1:
        return parts[0][0] + parts[-1][0]
    if parts:
        return parts[0][0]
    return ''


@baseframe.app_template_filter('avatar_type')
def avatar_type(text: str, types: int = 6) -> str:
    """Return an int from 1 to types based on initials from the given string"""
    initial = initials(text)
    parts = initial.split()
    stringTotal = ord(parts[0][0])
    if len(parts) > 1:
        stringTotal += ord(parts[0][1])
    return stringTotal % types or types


@baseframe.app_template_filter('usessl')
def usessl(url: str) -> str:
    """Convert a URL to https:// if SSL is enabled in site config."""
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
def nossl(url: str) -> str:
    """Convert a URL to http:// if using SSL."""
    if url.startswith('//'):
        return 'http:' + url
    if url.startswith('/') and request.url.startswith('https:'):  # /path and SSL is on
        url = os.path.join(request.url_root, url[1:])
    if url.startswith('https://'):
        return 'http:' + url[6:]
    return url


# TODO: Move this into Hasjob as it's not used elsewhere
@baseframe.app_template_filter('avatar_url')
def avatar_url(user: Any, size: Union[str, List[int], Tuple[int, int]] = None) -> str:
    """Generate an avatar for the given user."""
    if isinstance(size, (list, tuple)):
        size = 'x'.join(str(s) for s in size)
    if user.avatar:
        if size:
            # TODO: Use a URL parser
            if '?' in user.avatar:
                return user.avatar + '&size=' + str(size)
            else:
                return user.avatar + '?size=' + str(size)
        else:
            return user.avatar
    email = user.email
    if email:
        if isinstance(email, str):
            # Flask-Lastuser's User model has email as a string
            ehash = md5sum(user.email)
        else:
            # Lastuser's User model has email as a UserEmail object
            ehash = email.md5sum
        gravatar = '//www.gravatar.com/avatar/' + ehash + '?d=mm'
        if size:
            gravatar += '&s=' + str(size)
        return gravatar
    # Return Gravatar's missing man image
    return '//www.gravatar.com/avatar/00000000000000000000000000000000?d=mm'


@baseframe.app_template_filter('render_field_options')
def render_field_options(field, **kwargs) -> str:
    """Remove HTML attributes with falsy values before rendering a field."""
    d = {k: v for k, v in kwargs.items() if v is not None and v is not False}
    if field.render_kw:
        d.update(field.render_kw)
    return field(**d)


# TODO: Only used in renderfield.mustache. Re-check whether this is necessary at all.
@baseframe.app_template_filter('to_json')
def form_field_to_json(field, **kwargs) -> dict:
    """Render a form field as JSON."""
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
def field_markdown(text: str) -> Markup:
    """Render text as Markdown."""
    return Markup(markdown(text))


@baseframe.app_template_filter('ext_asset_url')
def ext_asset_url(asset: Union[str, List[str]]) -> str:
    """Return external asset URL for use in templates."""
    if isinstance(asset, str):
        return ext_assets([asset])
    else:
        return ext_assets(asset)


@baseframe.app_template_filter('firstline')
@cache.memoize(timeout=600)
def firstline(html: str) -> str:
    """
    Return the first line from a HTML blob as plain text.

    .. deprecated: 2021-03-25
        Use :func:`preview` instead.
    """
    result = text_blocks(html)
    if result:
        return compress_whitespace(result[0])
    return ''


@baseframe.app_template_filter('preview')
@cache.memoize(timeout=600)
def preview(html: str, min: int = 50, max: int = 158) -> str:  # NOQA: A002
    """
    Return a preview of a HTML blob as plain text, for use as a description tag.

    This function will attempt to return a HTML paragraph at a time, to avoid truncating
    sentences. Multiple paragraphs will be used if they are under min characters.

    :param str html: HTML text to generate a preview from
    :param int min: Minimum number of characters in the preview (default 50)
    :param int max: Maximum number of characters in the preview (default 158,
        recommended for Google)
    """
    # Get the max length we're interested in, for efficiency in grapheme counts. A large
    # blob of text can impair performance if we're only interested in a small preview.
    # `max` can be < `min` when the caller specifies a custom `max` without `min`
    max_length = (max if max > min else min) + 1
    blocks = text_blocks(html)
    if blocks:
        text = compress_whitespace(blocks.pop(0))
        length = grapheme.length(text, max_length)
        while blocks and length < min:
            text += ' ' + compress_whitespace(blocks.pop(0))
            length = grapheme.length(text, max_length)
        if length > max:
            text = grapheme.slice(text, 0, max - 1) + '…'
        return text
    return ''


@baseframe.app_template_filter('cdata')
def cdata(text: str) -> str:
    """Convert text to a CDATA sequence."""
    return Markup('<![CDATA[' + text.replace(']]>', ']]]]><![CDATA[>') + ']]>')


# TODO: Used only in Hasjob. Move there?
@baseframe.app_template_filter('shortdate')
def shortdate(value: Union[datetime, date]) -> str:
    """Render a date in short form (deprecated for lack of i18n support)."""
    dt: Union[datetime, date]
    utc_now: Union[datetime, date]
    if isinstance(value, datetime):
        tz = get_timezone()
        if value.tzinfo is None:
            dt = utc.localize(value).astimezone(tz)
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
        return str(dt.strftime("%e %b '%y")).replace("'", "’")


# TODO: Only used in Hasjob. Move there?
@baseframe.app_template_filter('longdate')
def longdate(value: Union[datetime, date]) -> str:
    """Render a date in long form (deprecated for lack of i18n support)."""
    dt: Union[datetime, date]
    if isinstance(value, datetime):
        if value.tzinfo is None:
            dt = utc.localize(value).astimezone(get_timezone())
        else:
            dt = value.astimezone(get_timezone())
    else:
        dt = value
    return dt.strftime('%e %B %Y')


@baseframe.app_template_filter('date')
def date_filter(
    value: Union[datetime, date],
    format: str = 'medium',  # NOQA: A002  # skipcq: PYL-W0622
    locale: Union[Locale, str] = None,
    usertz: bool = True,
) -> str:
    """Render a localized date."""
    dt: Union[datetime, date]
    if isinstance(value, datetime) and usertz:
        if value.tzinfo is None:
            dt = utc.localize(value).astimezone(get_timezone())
        else:
            dt = value.astimezone(get_timezone())
    else:
        dt = value
    return format_date(
        dt, format=format, locale=locale if locale else get_locale() or DEFAULT_LOCALE
    )


@baseframe.app_template_filter('time')
def time_filter(
    value: Union[datetime, time],
    format: str = 'short',  # NOQA: A002  # skipcq: PYL-W0622
    locale: Union[Locale, str] = None,
    usertz: bool = True,
) -> str:
    """Render a localized time."""
    # Default format = hh:mm
    dt: Union[datetime, time]
    if isinstance(value, datetime) and usertz:
        if value.tzinfo is None:
            dt = utc.localize(value).astimezone(get_timezone())
        else:
            dt = value.astimezone(get_timezone())
    else:
        dt = value
    return format_time(
        dt, format=format, locale=locale if locale else get_locale() or DEFAULT_LOCALE
    )


@baseframe.app_template_filter('datetime')
def datetime_filter(
    value: Union[datetime, date, time],
    format: str = 'medium',  # NOQA: A002  # skipcq: PYL-W0622
    locale: Union[Locale, str] = None,
    usertz: bool = True,
) -> str:
    """Render a localized date and time."""
    dt: Union[datetime, date, time]
    if isinstance(value, datetime) and usertz:
        if value.tzinfo is None:
            dt = utc.localize(value).astimezone(get_timezone())
        else:
            dt = value.astimezone(get_timezone())
    else:
        dt = value
    return format_datetime(
        dt, format=format, locale=locale if locale else get_locale() or DEFAULT_LOCALE
    )


@baseframe.app_template_filter('timestamp')
def timestamp_filter(value: datetime) -> float:
    """Render a POSIX timestamp."""
    if not value.tzinfo:
        return utc.localize(value).timestamp()
    return value.timestamp()


@baseframe.app_template_filter('timedelta')
def timedelta_filter(
    delta: Union[int, timedelta, datetime],
    granularity: str = 'second',
    threshold: float = 0.85,
    add_direction: bool = False,
    format: str = 'long',  # NOQA: A002  # skipcq: PYL-W0622
    locale: Union[Locale, str] = None,
) -> str:
    """
    Render a timedelta or int (representing seconds) as a duration.

    :param delta: A timedelta object representing the time difference to format, or the
        delta in seconds as an int value
    :param granularity: Determines the smallest unit that should be displayed, the value
        can be one of “year”, “month”, “week”, “day”, “hour”, “minute” or “second”
    :param threshold: Factor that determines at which point the presentation switches to
        the next higher unit
    :param add_direction: If this flag is set to True the return value will include
        directional information. For instance a positive timedelta will include the
        information about it being in the future, a negative will be information about
        the value being in the past. If a datetime is provided for delta, add_direction
        will be forced to True
    :param format: The format, can be “narrow”, “short” or “long”
    :param locale: A Locale object or a locale identifier (defaults to current locale)
    """
    if isinstance(delta, datetime):
        # Convert datetimes into a timedelta from present and turn on add_direction
        if not delta.tzinfo:
            delta = utc.localize(delta)
        delta = delta - request_timestamp()
        add_direction = True
    return format_timedelta(
        delta,
        granularity=granularity,
        threshold=threshold,
        add_direction=add_direction,
        format=format,
        locale=locale if locale else get_locale() or DEFAULT_LOCALE,
    )


@baseframe.app_template_filter('cleanurl')
def cleanurl_filter(url: Union[str, furl]) -> str:
    """Clean a URL visually by removing defaults like scheme and the ``www`` prefix."""
    if not isinstance(url, furl):
        url = furl(url)
    url.path.normalize()
    if url.netloc is not None and url.netloc.startswith('www.'):
        netloc = url.netloc[4:]
    else:
        netloc = url.netloc
    return furl().set(netloc=netloc, path=url.path).url.lstrip('//').rstrip('/')


@baseframe.app_template_filter('make_relative_url')
def make_relative_url(url: str) -> str:
    """Discard scheme and netloc from a URL, used to undo _external=True."""
    return urlunsplit(urlsplit(url)._replace(scheme='', netloc=''))
