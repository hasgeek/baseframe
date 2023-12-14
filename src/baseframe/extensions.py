"""Standard extensions to add to the Flask app."""
# pyright: reportMissingImports = false

import os.path
import typing as t
from datetime import tzinfo
from typing import cast

from flask import current_app, request
from flask_babel import Babel, Domain
from flask_caching import Cache
from pytz import timezone, utc

from coaster.auth import current_auth

from .statsd import Statsd

try:
    from flask_debugtoolbar import DebugToolbarExtension
except ImportError:
    DebugToolbarExtension = None
try:
    # pylint: disable=unused-import
    from flask_debugtoolbar_lineprofilerpanel.profile import line_profile
except ImportError:
    line_profile = None

__all__ = [
    'asset_cache',
    'babel',
    'baseframe_translations',
    'cache',
    'get_timezone',
    'get_user_locale',
    'networkbar_cache',
    'statsd',
]


DEFAULT_LOCALE = 'en'

networkbar_cache = Cache(with_jinja2_ext=False)
asset_cache = Cache(with_jinja2_ext=False)
cache = Cache()
babel = Babel()
statsd = Statsd()
if DebugToolbarExtension is not None:  # pragma: no cover
    toolbar = DebugToolbarExtension()
else:  # pragma: no cover
    toolbar = None

baseframe_translations = Domain(
    os.path.join(os.path.dirname(__file__), 'translations'), domain='baseframe'
)
_ = cast(t.Callable[..., str], baseframe_translations.gettext)
__ = cast(t.Callable[..., str], baseframe_translations.lazy_gettext)


def get_user_locale() -> str:
    """Get user's locale if available on the user object, else from the request."""
    # If this app and request have a user that specifies a locale, use it
    user = current_auth.actor  # Use 'actor' instead of 'user' to support anon users
    if user is not None and hasattr(user, 'locale') and user.locale:
        return user.locale
    # Otherwise try to guess the language from the user accept
    # header the browser transmits. We support a few in this
    # example. The best match wins.

    # Only en/hi are supported at the moment. Variants like en_IN/en_GB
    # are not explicitly supported and will default to 'en'. These will
    # need to be explicitly added in the future.
    return (
        request.accept_languages.best_match(['hi', 'en']) if request else None
    ) or DEFAULT_LOCALE


def get_timezone(default: t.Union[None, tzinfo, str] = None) -> tzinfo:
    """Return a timezone suitable for the current context."""
    # If this app and request have a user, return user's timezone,
    # else return app default timezone
    if (
        current_auth.actor is not None
    ):  # Use 'actor' instead of 'user' to support anon users
        user = current_auth.actor
        for attr in ('tz', 'timezone'):
            tz = getattr(user, attr, None)
            if tz:
                if isinstance(tz, str):
                    return timezone(tz)
                return tz

    if default is not None:
        if isinstance(default, str):
            return timezone(default)
        return default
    return current_app.config.get('tz') or utc
