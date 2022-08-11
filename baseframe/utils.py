from datetime import datetime, time, tzinfo
from decimal import Decimal
from typing import Any, List, Optional, Tuple, Union
import collections.abc as abc
import gettext
import types

from flask import g, json, request

from babel import Locale
from furl import furl
from mxsniff import mxsniff

try:
    from mxsniff import MxLookupError
except ImportError:
    from mxsniff import MXLookupException as MxLookupError

from pytz import timezone, utc
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
    'request_checked_xhr',
]


class JSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder.

    Adds support for additional types not covered by Flask's JSON encoder.
    """

    def default(self, o: Any) -> Union[int, str, float, Decimal, list, dict, None]:
        if hasattr(o, '__json__'):
            return o.__json__()
        if isinstance(o, (furl, Locale)):
            return str(o)
        if isinstance(o, BaseTzInfo):
            return o.zone
        if isinstance(o, tzinfo):  # Check after BaseTzInfo as that is a subclass
            return str(o)
        if isinstance(o, (datetime, time)):  # date is processed by Flask's default
            return o.isoformat()
        if isinstance(o, abc.Mapping):
            return dict(o)
        if isinstance(o, (types.GeneratorType, abc.Set)):
            return list(o)
        if isinstance(o, MarkdownComposite):
            return {'text': o.text, 'html': o.html}
        return super().default(o)


def request_timestamp() -> datetime:
    """Return a consistent UTC timestamp for the lifetime of the ongoing request."""
    if not g:
        return utcnow()
    ts = getattr(g, 'request_timestamp', None)
    if ts is None:
        ts = utcnow()
        g.request_timestamp = ts
    return ts


def is_public_email_domain(
    email_or_domain: str, default: Optional[bool] = None, timeout: int = 30
) -> bool:
    """
    Return True if the given email domain is known to offer public email accounts.

    Looks up a list of known public email providers, both directly via their domains
    (for popular domains like gmail.com) and via their MX records for services offering
    email on multiple domains. All MX lookup results are cached for one day. An
    exception is raised if timeout happens before the check is completed or domain
    lookup fails, and no default is provided.

    :param email_or_domain: Email address or domain name to check
    :param default: Default value to return in case domain lookup fails
    :param timeout: Lookup timeout in seconds
    :raises MxLookupError: If a DNS lookup error happens and no default is specified
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
        except MxLookupError:
            # Domain lookup failed
            if default is None:
                raise
            return default

    if any(p['public'] for p in sniffedmx['providers']):
        return True
    return False


def localized_country_list() -> List[Tuple[str, str]]:
    """
    Return a list of countries localized to the current user's locale.

    Contains a tuple of country codes (ISO3166-1 alpha-2) and localized country names.
    The localized list is cached for 24 hours.
    """
    return _localized_country_list_inner(get_user_locale())


@cache.memoize(timeout=86400)
def _localized_country_list_inner(locale: str) -> List[Tuple[str, str]]:
    """Return localized country list (helper for :func:`localized_country_list`)."""
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


def localize_timezone(dt: datetime, tz: Union[None, str, tzinfo] = None) -> datetime:
    """
    Convert a datetime into the specified timezone, defaulting to user's timezone.

    Naive datetimes are assumed to be in UTC.
    """
    if not dt.tzinfo:
        dt = utc.localize(dt)
    if not tz:
        tz = get_timezone()
    if isinstance(tz, str):
        tz = timezone(tz)
    return dt.astimezone(tz)


# pylint: disable=protected-access
def request_is_xhr() -> bool:
    """
    Return True if the request was triggered via a JavaScript XMLHttpRequest.

    This only works with libraries that support the "X-Requested-With" header and set it
    to "XMLHttpRequest". Prototype, jQuery and Mochikit do this. This function was
    ported from Werkzeug after being removed from there, as legacy apps may still be
    using jQuery.
    """
    request._checked_xhr = True  # type: ignore[attr-defined]
    return request.environ.get('HTTP_X_REQUESTED_WITH', '').lower() == 'xmlhttprequest'


def request_checked_xhr() -> bool:
    """Confirm if XHR header was checked for during this request."""
    return getattr(request, '_checked_xhr', False)
