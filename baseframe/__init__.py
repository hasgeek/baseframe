from flask_babelhg import gettext as _
from flask_babelhg import lazy_gettext as __

from ._version import __version__, __version_info__
from .assets import Version, assets
from .blueprint import *  # NOQA
from .deprecated import *  # NOQA
from .errors import *  # NOQA
from .filters import *  # NOQA
from .utils import *  # NOQA
from .views import *  # NOQA

# TODO: baseframe_js and baseframe_css are defined in deprecated.py
# and pending removal after an audit of all apps
__all__ = [  # NOQA: F405
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
    'localize_timezone',
    'localized_country_list',
    'request_is_xhr',
    'statsd',
    'Version',
]
