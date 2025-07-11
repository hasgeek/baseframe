"""Baseframe init."""

from typing import cast

from flask_assets import Bundle
from flask_babel import gettext, lazy_gettext

from . import (
    blueprint,
    deprecated,
    errors,
    extensions,
    filters,
    forms,
    signals,
    utils,
    views,
)
from ._version import __version__, __version_info__
from .assets import Version, assets
from .blueprint import baseframe
from .deprecated import baseframe_css, baseframe_js
from .extensions import GetTextProtocol, babel, baseframe_translations, cache, statsd
from .utils import (
    ctx_has_locale,
    localize_timezone,
    localized_country_list,
    request_checked_xhr,
    request_is_xhr,
)

# Pretend these return str, not Any or LazyString
_ = cast(GetTextProtocol, gettext)
__ = cast(GetTextProtocol, lazy_gettext)

# TODO: baseframe_js and baseframe_css are defined in deprecated.py
# and pending removal after an audit of all apps
__all__ = [
    'Bundle',
    'Version',
    '_',
    '__',
    '__version__',
    '__version_info__',
    'assets',
    'babel',
    'baseframe',
    'baseframe_css',
    'baseframe_js',
    'baseframe_translations',
    'blueprint',
    'cache',
    'ctx_has_locale',
    'deprecated',
    'errors',
    'extensions',
    'filters',
    'forms',
    'localize_timezone',
    'localized_country_list',
    'request_checked_xhr',
    'request_is_xhr',
    'signals',
    'statsd',
    'utils',
    'views',
]
