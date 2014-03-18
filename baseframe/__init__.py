# -*- coding: utf-8 -*-

from __future__ import absolute_import
from pytz import timezone
from flask import g, Blueprint, request
from coaster.assets import split_namespec
from flask.ext.assets import Environment, Bundle
from flask.ext.cache import Cache
from flask.ext.babelex import Babel, Domain
from flask.ext.mustache import FlaskMustache
from ._version import *
from .assets import assets, Version
from . import translations

__all__ = ['baseframe', 'baseframe_js', 'baseframe_css', 'assets', 'Version', '_', '__']

networkbar_cache = Cache(with_jinja2_ext=False)
cache = Cache()
babel = Babel()

baseframe_translations = Domain(translations.__path__[0], domain='baseframe')
_ = baseframe_translations.gettext
__ = baseframe_translations.lazy_gettext


class BaseframeBlueprint(Blueprint):
    def init_app(self, app, requires=[], bundle_js=None, bundle_css=None, assetenv=None,
            static_subdomain=None):
        """
        Initialize an app and load necessary assets.

        :param requires: List of required assets. If an asset has both .js
        and .css components, both will be added to the requirement list.
        Loaded assets will be minified and concatenated into the app's
        ``static/js`` and ``static/css`` folders. If an asset has problems
        with either of these, it should be loaded pre-bundled via the
        ``bundle_js`` and ``bundle_css`` parameters.
        :param bundle_js: Bundle of additional JavaScript.
        :param bundle_css: Bundle of additional CSS.
        :param static_subdomain: Serve static files from this subdomain
        """
        assets_js = []
        assets_css = []
        for item in requires:
            name, spec = split_namespec(item)
            for alist, ext in [(assets_js, '.js'), (assets_css, '.css')]:
                if name + ext in assets:
                    alist.append(name + ext + unicode(spec))
        js_all = Bundle(assets.require('!jquery.js', *assets_js),
            filters='closure_js', output='js/baseframe-packed.js')
        css_all = Bundle(assets.require(*assets_css),
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
        app.register_blueprint(self, static_subdomain=static_subdomain)

        app.config.setdefault('CACHE_KEY_PREFIX', 'flask_cache_' + app.name)
        nwcacheconfig = dict(app.config)
        nwcacheconfig['CACHE_KEY_PREFIX'] = 'networkbar_'
        if 'CACHE_TYPE' not in nwcacheconfig:
            nwcacheconfig['CACHE_TYPE'] = 'simple'

        networkbar_cache.init_app(app, config=nwcacheconfig)
        cache.init_app(app)
        babel.init_app(app)
        FlaskMustache(app)

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
    if user is not None and hasattr(user, 'locale'):
        return user.locale
    # Otherwise try to guess the language from the user accept
    # header the browser transmits. We support a few in this
    # example. The best match wins.

    # FIXME: Do this properly. Don't use a random selection of languages
    return request.accept_languages.best_match(['de', 'fr', 'es', 'hi', 'te', 'ta', 'kn', 'ml', 'en'])


@babel.timezoneselector
def get_timezone():
    # If this app supports user logins (ie, g.user exists) and
    # a user is logged in (ie, g.user is not None), return timezone
    user = getattr(g, 'user', None)
    if user is not None:
        return timezone(user.timezone)


@baseframe.after_app_request
def process_response(response):
    # Prevent pages from being placed in an iframe. If the response already
    # set has a value for this option, let it pass through
    if 'X-Frame-Options' in response.headers:
        frameoptions = response.headers.get('X-Frame-Options')
        # FIXME: There has to be a better way to signal this.
        if not frameoptions or frameoptions == 'ALLOW':
            response.headers.pop('X-Frame-Options')
    else:
        if hasattr(g, 'login_required') and g.login_required:
            # Protect logged-in-only pages from appearing in frames
            response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response


# Replace gettext handlers for imports
b_ = _
b__ = __
from flask.ext.babelex import gettext as _, lazy_gettext as __

from .views import *
from .errors import *
from .filters import *

# Deprecated imports
from .deprecated import *
