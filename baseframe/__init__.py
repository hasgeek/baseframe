# -*- coding: utf-8 -*-

from __future__ import absolute_import
from pytz import timezone, UTC
from flask import g, Blueprint, request, current_app
from coaster.assets import split_namespec
from flask.ext.wtf import CSRFProtect
from flask.ext.assets import Environment, Bundle
from flask.ext.cache import Cache
from flask.ext.dogpile_cache import DogpileCache
from flask.ext.babelex import Babel, Domain

try:
    from flask.ext.debugtoolbar import DebugToolbarExtension
except ImportError:
    DebugToolbarExtension = None
try:
    from flask_debugtoolbar_lineprofilerpanel.profile import line_profile
except ImportError:
    line_profile = None

from ._version import *  # NOQA
from .assets import assets, Version
from . import translations

__all__ = ['baseframe', 'baseframe_js', 'baseframe_css', 'assets', 'Version', '_', '__']

networkbar_cache = Cache(with_jinja2_ext=False)
asset_cache = Cache(with_jinja2_ext=False)
cache = Cache()
dogpile = DogpileCache()
babel = Babel()
csrf = CSRFProtect()
if DebugToolbarExtension is not None:
    toolbar = DebugToolbarExtension()
else:
    toolbar = None


DEFAULT_DOGPILE_CONFIG = {
    'DOGPILE_CACHE_BACKEND': 'dogpile.cache.redis',
    'DOGPILE_CACHE_URLS': '127.0.0.1:6379',
    'DOGPILE_CACHE_REGIONS': [('default', 3600)]
}

baseframe_translations = Domain(translations.__path__[0], domain='baseframe')
_ = baseframe_translations.gettext
__ = baseframe_translations.lazy_gettext


def _select_jinja_autoescape(filename):
    """
    Returns `True` if autoescaping should be active for the given template name.
    """
    if filename is None:
        return False
    return filename.endswith(('.html', '.htm', '.xml', '.xhtml',
        '.html.jinja', '.html.jinja2', '.xml.jinja', '.xml.jinja2', '.xhtml.jinja', '.xhtml.jinja2'))


class BaseframeBlueprint(Blueprint):
    def init_app(self, app, requires=[], ext_requires=[], bundle_js=None, bundle_css=None, assetenv=None,
            enable_csrf=False):
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
        :param bool enable_csrf: Enable global CSRF for all requests in your app
        """
        app.jinja_env.add_extension('jinja2.ext.do')
        app.jinja_env.autoescape = _select_jinja_autoescape
        if app.config.get('SERVER_NAME'):
            subdomain = app.config.get('STATIC_SUBDOMAIN', 'static')
            app.add_url_rule('/static/<path:filename>', endpoint='static',
                view_func=app.send_static_file, subdomain=subdomain)
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
                    for alist, ilist, ext in [(sub_js, ignore_js, '.js'), (sub_css, ignore_css, '.css')]:
                        if name + ext in assets:
                            alist.append(name + ext + unicode(spec))
                            ilist.append('!' + name + ext)
                if sub_js:
                    ext_js.append(sub_js)
                if sub_css:
                    ext_css.append(sub_css)
        else:
            requires = [item for itemgroup in ext_requires
                for item in (itemgroup if isinstance(itemgroup, (list, tuple)) else [itemgroup])] + requires

        app.config['ext_js'] = ext_js
        app.config['ext_css'] = ext_css

        assets_js = []
        assets_css = []
        for item in requires:
            name, spec = split_namespec(item)
            for alist, ext in [(assets_js, '.js'), (assets_css, '.css')]:
                if name + ext in assets:
                    alist.append(name + ext + unicode(spec))
        js_all = Bundle(assets.require(*(ignore_js + assets_js)),
            filters='uglipyjs', output='js/baseframe-packed.js')
        css_all = Bundle(assets.require(*(ignore_css + assets_css)),
            filters=['cssrewrite', 'cssmin'], output='css/baseframe-packed.css')
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

        for config_key, config_value in DEFAULT_DOGPILE_CONFIG.items():
            app.config.setdefault(config_key, config_value)
        dogpile.init_app(app)

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
                        'flask_debugtoolbar_lineprofilerpanel.panels.LineProfilerPanel')
            toolbar.init_app(app)
        if enable_csrf:
            csrf.init_app(app)

        # If this app has a Lastuser extension registered, give it a cache
        lastuser = getattr(app, 'extensions', {}).get('lastuser')
        if lastuser and hasattr(lastuser, 'init_cache'):
            lastuser.init_cache(cache)

        app.config['tz'] = timezone(app.config.get('TIMEZONE', 'UTC'))

        if 'NETWORKBAR_DATA' not in app.config:
            app.config['NETWORKBAR_DATA'] = 'https://api.hasgeek.com/1/networkbar/networkbar.json'

        if isinstance(app.config.get('NETWORKBAR_DATA'), (list, tuple)):
            app.config['NETWORKBAR_LINKS'] = app.config['NETWORKBAR_DATA']

    def register(self, app, options, first_registration=False):
        """
        Called by :meth:`Flask.register_blueprint` to register a blueprint
        on the application.  This can be overridden to customize the register
        behavior.  Keyword arguments from
        :func:`~flask.Flask.register_blueprint` are directly forwarded to this
        method in the `options` dictionary.
        """
        self._got_registered_once = True
        state = self.make_setup_state(app, options, first_registration)
        if self.has_static_folder:
            state.add_url_rule(self.static_url_path + '/<path:filename>',
                               view_func=self.send_static_file,
                               endpoint='static', subdomain=options.get('static_subdomain'))

        for deferred in self.deferred_functions:
            deferred(state)


baseframe = BaseframeBlueprint('baseframe', __name__,
    static_folder='static',
    static_url_path='/_baseframe',
    template_folder='templates')


@babel.localeselector
def get_locale():
    # If a user is logged in and the user object specifies a locale, use it
    user = getattr(g, 'user', None)
    if user is not None and hasattr(user, 'locale') and user.locale:
        return user.locale
    # Otherwise try to guess the language from the user accept
    # header the browser transmits. We support a few in this
    # example. The best match wins.

    # FIXME: Do this properly. Don't use a random selection of languages
    return request.accept_languages.best_match(['de', 'fr', 'es', 'hi', 'te', 'ta', 'kn', 'ml', 'en'])


@babel.timezoneselector
def get_timezone():
    # If this app supports user logins (ie, g.user exists) and
    # a user is logged in (ie, g.user is not None), return user's timezone
    # else return app default timezone
    user = getattr(g, 'user', None)
    if user is not None:
        if hasattr(user, 'tz'):
            return user.tz
        elif hasattr(user, 'timezone'):
            return timezone(user.timezone)
    return current_app.config.get('tz') or UTC


def localize_timezone(datetime, tz=None):
    if not datetime.tzinfo:
        datetime = UTC.localize(datetime)
    if not tz:
        tz = get_timezone()
    if isinstance(tz, basestring):
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

    if 'Vary' in response.headers:
        vary_values = [item.strip() for item in response.headers['Vary'].split(',')]
        if 'Accept-Language' not in vary_values:
            vary_values.append('Accept-Language')
        if 'Cookie' not in vary_values:
            vary_values.append('Cookie')
        response.headers['Vary'] = ', '.join(vary_values)
    else:
        response.headers['Vary'] = 'Accept-Language, Cookie'

    # Prevent pages from being placed in an iframe. If the response already
    # set has a value for this option, let it pass through
    if 'X-Frame-Options' in response.headers:
        frameoptions = response.headers.get('X-Frame-Options')
        if not frameoptions or frameoptions == 'ALLOW':
            response.headers.pop('X-Frame-Options')
    else:
        if hasattr(g, 'login_required') and g.login_required:
            # Protect only login_required pages from appearing in frames
            response.headers['X-Frame-Options'] = 'SAMEORIGIN'

    # In memoriam. http://www.gnuterrypratchett.com/
    response.headers['X-Clacks-Overhead'] = 'GNU Terry Pratchett'

    return response


# Replace gettext handlers for imports
b_ = _
b__ = __
from flask.ext.babelex import gettext as _, lazy_gettext as __

from .views import *    # NOQA
from .errors import *   # NOQA
from .filters import *  # NOQA

# Deprecated imports
from .deprecated import *  # NOQA
