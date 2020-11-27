import os.path

from flask import current_app, request
from flask_babelhg import Babel, Domain

from flask_caching import Cache
from pytz import timezone, utc
from pytz.tzinfo import BaseTzInfo

from coaster.auth import current_auth

from .statsd import Statsd

try:
    from flask_debugtoolbar import DebugToolbarExtension
except ImportError:
    DebugToolbarExtension = None
try:
    from flask_debugtoolbar_lineprofilerpanel.profile import line_profile
except ImportError:
    line_profile = None

__all__ = ['networkbar_cache', 'asset_cache', 'cache', 'babel', 'statsd']

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
_ = baseframe_translations.gettext
__ = baseframe_translations.lazy_gettext


@babel.localeselector
def get_user_locale() -> str:
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
    return (request and request.accept_languages.best_match(['hi', 'en'])) or 'en'


@babel.timezoneselector
def get_timezone() -> BaseTzInfo:
    # If this app and request have a user, return user's timezone,
    # else return app default timezone
    if (
        current_auth.actor is not None
    ):  # Use 'actor' instead of 'user' to support anon users
        user = current_auth.actor
        if hasattr(user, 'tz'):
            return user.tz
        elif hasattr(user, 'timezone') and user.timezone:
            if isinstance(user.timezone, str):
                return timezone(user.timezone)
            else:
                return user.timezone
    return current_app.config.get('tz') or utc
