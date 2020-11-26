from datetime import date, datetime, time
import collections.abc as abc
import gettext
import types

from flask import g, request
from flask.json import JSONEncoder as JSONEncoderBase
from flask_babelhg.speaklater import is_lazy_string as is_lazy_string_hg
from speaklater import is_lazy_string as is_lazy_string_sl

from babel import Locale
from furl import furl
from mxsniff import MXLookupException, mxsniff
from pytz import UTC, timezone
from pytz.tzinfo import BaseTzInfo
import pycountry

from coaster.sqlalchemy import MarkdownComposite
from coaster.utils import md5sum, utcnow

from .extensions import asset_cache, cache, get_timezone, get_user_locale

__all__ = [
    'request_timestamp',
    'is_public_email_domain',
    'localized_country_list',
    'localize_timezone',
    'request_is_xhr',
]


class JSONEncoder(JSONEncoderBase):
    """
    Custom JSON encoder that adds support to types that are not supported
    by Flask's JSON encoder. Eg: lazy_gettext
    """

    def default(self, o):
        if is_lazy_string(o):
            return str(o)
        if isinstance(o, BaseTzInfo):
            return o.zone
        if isinstance(o, (date, datetime, time)):
            return o.isoformat()
        if isinstance(o, Locale):
            return str(o)
        if isinstance(o, abc.Mapping):
            return dict(o)
        if isinstance(o, furl):
            return o.url
        if isinstance(o, (types.GeneratorType, abc.Set)):
            return list(o)
        if isinstance(o, MarkdownComposite):
            return {'text': o.text, 'html': o.html}
        return super(JSONEncoder, self).default(o)


def request_timestamp():
    """
    Return a UTC timestamp for the request
    """
    if not g:
        return utcnow()
    ts = getattr(g, 'request_timestamp', None)
    if ts is None:
        ts = utcnow()
        g.request_timestamp = ts
    return ts


def is_public_email_domain(email_or_domain, default=None, timeout=30):
    """
    Checks if the given domain (or domain of given email) is known to offer public email accounts.
    All MX lookup results are cached for one day. An exception is raised if timeout happens
    before the check is completed or domain lookup fails, and no default is provided.

    :param email_or_domain: Email address or domain name to check
    :param default: Default value to return in case domain lookup fails
    :param timeout: Lookup timeout
    :raises MXLookupException: If a DNS lookup error happens and no default is specified
    """
    cache_key = 'mxrecord/' + md5sum(email_or_domain)

    try:
        sniffedmx = asset_cache.get(cache_key)
    except ValueError:  # Possible error from Py2 vs Py3 pickle mismatch
        sniffedmx = None

    if sniffedmx is None or not isinstance(sniffedmx, dict):
        # Cache entry missing or corrupted; fetch a new result and update cache
        try:
            sniffedmx = mxsniff(email_or_domain, timeout=timeout)
            asset_cache.set(cache_key, sniffedmx, timeout=86400)  # cache for a day
        except MXLookupException as e:
            # Domain lookup failed
            if default is None:
                raise e
            else:
                return default

    if any(p['public'] for p in sniffedmx['providers']):
        return True
    else:
        return False


def localized_country_list():
    """
    Returns a list of country codes (ISO3166-1 alpha-2) and country names,
    localized to the user's locale as determined by :func:`get_user_locale`.

    The localized list is cached for 24 hours.
    """
    return _localized_country_list_inner(get_user_locale())


@cache.memoize(timeout=86400)
def _localized_country_list_inner(locale):
    """
    Inner function supporting :func:`localized_country_list`.
    """
    if locale == 'en':
        countries = [(country.name, country.alpha_2) for country in pycountry.countries]
    else:
        pycountry_locale = gettext.translation(
            'iso3166-1', pycountry.LOCALES_DIR, languages=[locale]
        )
        countries = [
            (pycountry_locale.gettext(country.name), country.alpha_2)
            for country in pycountry.countries
        ]
    countries.sort()
    return [(code, name) for (name, code) in countries]


def localize_timezone(datetime, tz=None):
    """
    Convert a datetime into the user's timezone, or into the specified
    timezone. Naive datetimes are assumed to be in UTC.
    """
    if not datetime.tzinfo:
        datetime = UTC.localize(datetime)
    if not tz:
        tz = get_timezone()
    if isinstance(tz, str):
        tz = timezone(tz)
    return datetime.astimezone(tz)


def is_lazy_string(string):
    # Some lazy strings are from the speaklater library, some from Flask-Babelhg's fork
    return is_lazy_string_hg(string) or is_lazy_string_sl(string)


def request_is_xhr():
    """
    True if the request was triggered via a JavaScript XMLHttpRequest. This only works
    with libraries that support the `X-Requested-With` header and set it to
    "XMLHttpRequest".  Libraries that do that are prototype, jQuery and Mochikit and
    probably some more. This function was ported from Werkzeug after being removed from
    there, as legacy apps may still be using jQuery.
    """
    return request.environ.get('HTTP_X_REQUESTED_WITH', '').lower() == 'xmlhttprequest'
