"""Baseframe init."""

from typing import Callable, cast

from flask_babel import gettext, lazy_gettext

from ._version import __version__, __version_info__
from .assets import Version, assets
from .blueprint import *  # NOQA
from .deprecated import *  # NOQA
from .extensions import *  # NOQA
from .filters import *  # NOQA
from .utils import *  # NOQA
from .views import *  # NOQA

from . import forms  # isort:skip

# Pretend these return str, not Any or LazyString
_ = cast(Callable[..., str], gettext)
__ = cast(Callable[..., str], lazy_gettext)

# TODO: baseframe_js and baseframe_css are defined in deprecated.py
# and pending removal after an audit of all apps
__all__ = [  # noqa: F405
    '_',
    '__',
    '__version__',
    '__version_info__',
    'assets',
    'babel',
    'baseframe',
    'baseframe_css',
    'baseframe_js',
    'cache',
    'forms',
    'localize_timezone',
    'localized_country_list',
    'request_is_xhr',
    'statsd',
    'Version',
]
