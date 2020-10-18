# -*- coding: utf-8 -*-

from __future__ import absolute_import
import six
import six.moves.collections_abc as abc

from datetime import date, datetime, time
import gettext
import json
import os.path
import types

from flask import Blueprint, current_app, request
from flask.json import JSONEncoder as JSONEncoderBase
from flask_assets import Bundle, Environment
from flask_babelhg import Babel, Domain, ctx_has_locale
from flask_babelhg.speaklater import is_lazy_string

from babel import Locale
from flask_caching import Cache
from furl import furl
from pytz import UTC, timezone
from pytz.tzinfo import BaseTzInfo
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.rq import RqIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
import pycountry
import sentry_sdk

from coaster.app import RotatingKeySecureCookieSessionInterface
from coaster.assets import split_namespec
from coaster.auth import current_auth, request_has_auth
from coaster.sqlalchemy import MarkdownComposite

from . import translations
from ._version import __version__, __version_info__
from .assets import Version, assets
from .statsd import Statsd

try:
    from flask_debugtoolbar import DebugToolbarExtension
except ImportError:
    DebugToolbarExtension = None
try:
    from flask_debugtoolbar_lineprofilerpanel.profile import line_profile
except ImportError:
    line_profile = None
try:
    import newrelic.agent
except ImportError:
    newrelic = None


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

networkbar_cache = Cache(with_jinja2_ext=False)
asset_cache = Cache(with_jinja2_ext=False)
cache = Cache()
babel = Babel()
statsd = Statsd()
if DebugToolbarExtension is not None:  # pragma: no cover
    toolbar = DebugToolbarExtension()
else:  # pragma: no cover
    toolbar = None


THEME_FILES = {
    'bootstrap3': {
        'ajaxform.html.jinja2': 'baseframe/bootstrap3/ajaxform.html.jinja2',
        'autoform.html.jinja2': 'baseframe/bootstrap3/autoform.html.jinja2',
        'delete.html.jinja2': 'baseframe/bootstrap3/delete.html.jinja2',
        'message.html.jinja2': 'baseframe/bootstrap3/message.html.jinja2',
        'redirect.html.jinja2': 'baseframe/bootstrap3/redirect.html.jinja2',
    },
    'mui': {
        'ajaxform.html.jinja2': 'baseframe/mui/ajaxform.html.jinja2',
        'autoform.html.jinja2': 'baseframe/mui/autoform.html.jinja2',
        'delete.html.jinja2': 'baseframe/mui/delete.html.jinja2',
        'message.html.jinja2': 'baseframe/mui/message.html.jinja2',
        'redirect.html.jinja2': 'baseframe/mui/redirect.html.jinja2',
    },
}

baseframe_translations = Domain(translations.__path__[0], domain='baseframe')
_ = baseframe_translations.gettext
__ = baseframe_translations.lazy_gettext


class JSONEncoder(JSONEncoderBase):
    """
    Custom JSON encoder that adds support to types that are not supported
    by Flask's JSON encoder. Eg: lazy_gettext
    """

    def default(self, o):
        if is_lazy_string(o):
            return six.text_type(o)
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


def _select_jinja_autoescape(filename):
    """
    Returns `True` if autoescaping should be active for the given template name.
    """
    if filename is None:
        return False
    return filename.endswith(
        (
            '.html',
            '.htm',
            '.xml',
            '.xhtml',
            '.html.jinja',
            '.html.jinja2',
            '.xml.jinja',
            '.xml.jinja2',
            '.xhtml.jinja',
            '.xhtml.jinja2',
        )
    )


def request_is_xhr():
    """
    True if the request was triggered via a JavaScript XMLHttpRequest. This only works
    with libraries that support the `X-Requested-With` header and set it to
    "XMLHttpRequest".  Libraries that do that are prototype, jQuery and Mochikit and
    probably some more. This function was ported from Werkzeug after being removed from
    there, as legacy apps may still be using jQuery.
    """
    return request.environ.get('HTTP_X_REQUESTED_WITH', '').lower() == 'xmlhttprequest'


class BaseframeBlueprint(Blueprint):
    def init_app(
        self,
        app,
        requires=[],
        ext_requires=[],
        bundle_js=None,
        bundle_css=None,
        assetenv=None,
        theme='bootstrap3',
        asset_modules=(),
    ):
        """
        Initialize an app and load necessary assets.

        :param requires: List of required assets. If an asset has both .js
            and .css components, both will be added to the requirement list.
            Loaded assets will be minified and concatenated into the app's
            ``static/js`` and ``static/css`` folders. If an asset has problems
            with either of these, it should be loaded pre-bundled via the
            ``bundle_js`` and ``bundle_css`` parameters.
        :param ext_requires: Same as requires, but will be loaded from
            an external cookiefree server if ``ASSET_SERVER`` is in config,
            before the reqular requires list. Assets are loaded as part of
            ``requires`` if there is no asset server
        :param bundle_js: Bundle of additional JavaScript
        :param bundle_css: Bundle of additional CSS
        :param assetenv: Environment for assets (in case your app needs a custom environment)
        """
        # Initialize Sentry logging
        if app.config.get('SENTRY_URL'):
            sentry_sdk.init(
                dsn=app.config['SENTRY_URL'],
                integrations=[
                    FlaskIntegration(),
                    RqIntegration(),
                    SqlalchemyIntegration(),
                ],
            )

        # Setup secret key rotation
        if app.config['SECRET_KEY']:  # Always present as it's a default
            if not app.config.get('SECRET_KEYS'):
                app.logger.debug("Setting SECRET_KEYS from SECRET_KEY")
                app.config['SECRET_KEYS'] = [app.config['SECRET_KEY']]
        elif app.config.get('SECRET_KEYS'):
            app.logger.debug("Setting SECRET_KEY from first item in SECRET_KEYS")
            app.config['SECRET_KEY'] = app.config['SECRET_KEYS'][0]
        if app.config.get('SECRET_KEY') != app.config.get('SECRET_KEYS', [None])[0]:
            raise ValueError("App has misconfigured secret keys")
        app.session_interface = RotatingKeySecureCookieSessionInterface()

        # Default .js and tracking file for Matomo
        if app.config.get('MATOMO_URL') and app.config.get('MATOMO_ID'):
            app.config.setdefault('MATOMO_JS', 'matomo.js')
            app.config.setdefault('MATOMO_FILE', 'matomo.php')

        statsd.init_app(app)

        # Since Flask 0.11, templates are no longer auto reloaded.
        # Setting the config alone doesn't seem to work, so we explicitly
        # set the jinja environment here.
        if app.config.get('TEMPLATES_AUTO_RELOAD') or (
            app.config.get('TEMPLATES_AUTO_RELOAD') is None and app.config.get('DEBUG')
        ):
            app.jinja_env.auto_reload = True
        app.jinja_env.add_extension('jinja2.ext.do')
        app.jinja_env.autoescape = _select_jinja_autoescape
        app.jinja_env.globals['request_is_xhr'] = request_is_xhr
        if app.subdomain_matching:
            # Does this app want a static subdomain? (Default: yes, 'static').
            # Apps can disable this by setting STATIC_SUBDOMAIN = None.
            # Since Werkzeug internally uses '' instead of None, but takes None
            # as the default parameter, we remap '' to None in our config
            subdomain = app.config.get('STATIC_SUBDOMAIN', 'static') or None
            if subdomain:
                for rule in app.url_map.iter_rules('static'):
                    # For safety, seek out and update the static route added by Flask.
                    # Do not touch additional static routes added by the app or other
                    # blueprints
                    if not rule.subdomain:  # Will be '' not None
                        rule.subdomain = subdomain
                        rule.refresh()
                        break
        else:
            subdomain = None

        ignore_js = ['!jquery.js']
        ignore_css = []
        ext_js = []
        ext_css = []
        if app.config.get('ASSET_SERVER'):
            for itemgroup in ext_requires:
                sub_js = []
                sub_css = []
                if not isinstance(itemgroup, (list, tuple)):
                    itemgroup = [itemgroup]
                for item in itemgroup:
                    name, spec = split_namespec(item)
                    for alist, ilist, ext in [
                        (sub_js, ignore_js, '.js'),
                        (sub_css, ignore_css, '.css'),
                    ]:
                        if name + ext in assets:
                            alist.append(name + ext + six.text_type(spec))
                            ilist.append('!' + name + ext)
                if sub_js:
                    ext_js.append(sub_js)
                if sub_css:
                    ext_css.append(sub_css)
        else:
            requires = [
                item
                for itemgroup in ext_requires
                for item in (
                    itemgroup if isinstance(itemgroup, (list, tuple)) else [itemgroup]
                )
            ] + requires

        app.config['ext_js'] = ext_js
        app.config['ext_css'] = ext_css

        assets_js = []
        assets_css = []
        for item in requires:
            name, spec = split_namespec(item)
            for alist, ext in [(assets_js, '.js'), (assets_css, '.css')]:
                if name + ext in assets:
                    alist.append(name + ext + six.text_type(spec))
        js_all = Bundle(
            assets.require(*(ignore_js + assets_js)),
            filters='uglipyjs',
            output='js/baseframe-packed.js',
        )
        css_all = Bundle(
            assets.require(*(ignore_css + assets_css)),
            filters=['cssrewrite', 'cssmin'],
            output='css/baseframe-packed.css',
        )
        if bundle_js:
            js_all = Bundle(js_all, bundle_js)
        if bundle_css:
            css_all = Bundle(css_all, bundle_css)

        if assetenv is None:
            app.assets = Environment(app)
        else:
            app.assets = assetenv
        app.assets.register('js_jquery', assets.require('jquery.js'))
        app.assets.register('js_all', js_all)
        app.assets.register('css_all', css_all)
        app.register_blueprint(self, static_subdomain=subdomain)

        for module_name in asset_modules:
            try:
                module = __import__(module_name)
                module.blueprint.init_app(app)
                app.register_blueprint(
                    module.blueprint,
                    url_prefix="/_baseframe",
                    static_subdomain=subdomain,
                )
            except ImportError:
                app.logger.warning("Unable to import asset module: %s", module_name)

        # Optional config for a client app to use a manifest file
        # to load fingerprinted assets
        # If used with webpack, the client app is expected to specify its own webpack.config.js
        # Set `ASSETS_MANIFEST_PATH` in `app.config` to the path for `manifest.json`.
        # Eg: "static/build/manifest.json"
        # Set `ASSET_BASE_PATH` in `app.config` to the path in which the compiled assets are present.
        # Eg: "static/build"
        if app.config.get('ASSET_MANIFEST_PATH'):
            # Load assets into config from a manifest file
            with app.open_resource(app.config['ASSET_MANIFEST_PATH']) as f:
                asset_bundles = json.loads(f.read())
                if app.config.get('assets'):
                    raise ValueError(
                        "Loading assets via a manifest file needs the `ASSETS` config key to be unused"
                    )
                app.config['assets'] = {}
                for asset_key, asset_path in asset_bundles['assets'].items():
                    app.config['assets'][asset_key] = asset_path

        app.config.setdefault('CACHE_KEY_PREFIX', 'flask_cache_' + app.name + '/')
        nwcacheconfig = dict(app.config)
        nwcacheconfig['CACHE_KEY_PREFIX'] = 'networkbar_'
        if 'CACHE_TYPE' not in nwcacheconfig:
            nwcacheconfig['CACHE_TYPE'] = 'simple'

        acacheconfig = dict(app.config)
        acacheconfig['CACHE_KEY_PREFIX'] = 'asset_'
        if 'CACHE_TYPE' not in acacheconfig:
            acacheconfig['CACHE_TYPE'] = 'simple'

        networkbar_cache.init_app(app, config=nwcacheconfig)
        asset_cache.init_app(app, config=acacheconfig)
        cache.init_app(app)

        babel.init_app(app)
        if toolbar is not None:
            if 'DEBUG_TB_PANELS' not in app.config:
                app.config['DEBUG_TB_PANELS'] = [
                    'flask_debugtoolbar.panels.versions.VersionDebugPanel',
                    'flask_debugtoolbar.panels.timer.TimerDebugPanel',
                    'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
                    'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
                    'flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel',
                    'flask_debugtoolbar.panels.template.TemplateDebugPanel',
                    'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
                    'flask_debugtoolbar.panels.logger.LoggingPanel',
                    'flask_debugtoolbar.panels.route_list.RouteListDebugPanel',
                    'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
                ]
                if line_profile is not None:
                    app.config['DEBUG_TB_PANELS'].append(
                        'flask_debugtoolbar_lineprofilerpanel.panels.LineProfilerPanel'
                    )
            toolbar.init_app(app)

        app.json_encoder = JSONEncoder
        # If this app has a Lastuser extension registered, give it a cache
        lastuser = getattr(app, 'extensions', {}).get('lastuser')
        if lastuser and hasattr(lastuser, 'init_cache'):
            lastuser.init_cache(app=app, cache=cache)

        app.config['tz'] = timezone(app.config.get('TIMEZONE', 'UTC'))

        if theme not in THEME_FILES:
            raise ValueError("Unrecognised theme: %s" % theme)
        app.config['theme'] = theme

        if 'NETWORKBAR_DATA' not in app.config:
            app.config[
                'NETWORKBAR_DATA'
            ] = 'https://api.hasgeek.com/1/networkbar/networkbar.json'

        if isinstance(app.config.get('NETWORKBAR_DATA'), (list, tuple)):
            app.config['NETWORKBAR_LINKS'] = app.config['NETWORKBAR_DATA']

        app.config.setdefault('RECAPTCHA_DATA_ATTRS', {})
        app.config['RECAPTCHA_DATA_ATTRS'].setdefault(
            'callback', 'onInvisibleRecaptchaSubmit'
        )
        app.config['RECAPTCHA_DATA_ATTRS'].setdefault('size', 'invisible')

        if newrelic and os.path.isfile('newrelic.ini'):
            newrelic.agent.initialize('newrelic.ini')
            app.logger.debug("Successfully initiated Newrelic")
        elif not newrelic:
            app.logger.debug("Did not find `newrelic` package, skipping it")
        else:
            app.logger.debug(
                "Did not find New Relic settings file newrelic.ini, skipping it"
            )

    def register(self, app, options, first_registration=False):
        """
        Called by :meth:`Flask.register_blueprint` to register all views
        and callbacks registered on the blueprint with the application. Creates
        a :class:`.BlueprintSetupState` and calls each :meth:`record` callback
        with it.

        :param app: The application this blueprint is being registered with.
        :param options: Keyword arguments forwarded from
            :meth:`~Flask.register_blueprint`.
        :param first_registration: Whether this is the first time this
            blueprint has been registered on the application.
        """
        self._got_registered_once = True
        state = self.make_setup_state(app, options, first_registration)

        if self.has_static_folder:
            state.add_url_rule(
                self.static_url_path + '/<path:filename>',
                view_func=self.send_static_file,
                endpoint='static',
                subdomain=options.get('static_subdomain'),
            )

        for deferred in self.deferred_functions:
            deferred(state)


baseframe = BaseframeBlueprint(
    'baseframe',
    __name__,
    static_folder='static',
    static_url_path='/_baseframe',
    template_folder='templates',
)


@babel.localeselector
def get_locale():
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
def get_timezone():
    # If this app and request have a user, return user's timezone,
    # else return app default timezone
    if (
        current_auth.actor is not None
    ):  # Use 'actor' instead of 'user' to support anon users
        user = current_auth.actor
        if hasattr(user, 'tz'):
            return user.tz
        elif hasattr(user, 'timezone') and user.timezone:
            if isinstance(user.timezone, six.string_types):
                return timezone(user.timezone)
            else:
                return user.timezone
    return current_app.config.get('tz') or UTC


def localized_country_list():
    """
    Returns a list of country codes (ISO3166-1 alpha-2) and country names,
    localized to the user's locale as determined by :func:`get_locale`.

    The localized list is cached for 24 hours.
    """
    return _localized_country_list_inner(get_locale())


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
        if six.PY2:
            countries = [
                (
                    pycountry_locale.gettext(country.name).decode('utf-8'),
                    country.alpha_2,
                )
                for country in pycountry.countries
            ]
        else:
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
    if isinstance(tz, six.string_types):
        tz = timezone(tz)
    return datetime.astimezone(tz)


@baseframe.after_app_request
def process_response(response):
    if request.endpoint in ('static', 'baseframe.static'):
        if 'Access-Control-Allow-Origin' not in response.headers:
            # This is required for webfont resources
            # Note: We do not serve static assets in production, nginx does.
            # That means this piece of code will never be called in production.
            response.headers['Access-Control-Allow-Origin'] = '*'

    # If Babel was accessed in this request, the response's contents will vary with
    # the accepted language
    if ctx_has_locale():
        response.vary.add('Accept-Language')
    # If current_auth was accessed during this request, it is sensitive to the lastuser
    # cookie
    if request_has_auth():
        response.vary.add('Cookie')

    # Prevent pages from being placed in an iframe. If the response already
    # set has a value for this option, let it pass through
    if 'X-Frame-Options' in response.headers:
        frameoptions = response.headers.get('X-Frame-Options')
        if not frameoptions or frameoptions == 'ALLOW':
            # 'ALLOW' is an unofficial signal from the app to Baseframe.
            # It signals us to remove the header and not set a default
            response.headers.pop('X-Frame-Options')
    else:
        if request_has_auth() and getattr(current_auth, 'login_required', False):
            # Protect only login_required pages from appearing in frames
            response.headers['X-Frame-Options'] = 'SAMEORIGIN'

    # In memoriam. http://www.gnuterrypratchett.com/
    response.headers['X-Clacks-Overhead'] = 'GNU Terry Pratchett'

    return response


# Replace gettext handlers for imports
b_ = _
b__ = __
from flask_babelhg import gettext as _  # isort:skip
from flask_babelhg import lazy_gettext as __  # isort:skip

from .utils import *  # NOQA # isort:skip
from .views import *  # NOQA # isort:skip
from .errors import *  # NOQA # isort:skip
from .filters import *  # NOQA # isort:skip

# Deprecated imports
from .deprecated import *  # NOQA # isort:skip
