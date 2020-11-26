import json
import os.path

from flask import Blueprint
from flask_assets import Bundle, Environment
from flask_babelhg import get_locale

from pytz import timezone
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.rq import RqIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
import sentry_sdk

from coaster.app import RotatingKeySecureCookieSessionInterface
from coaster.assets import split_namespec

from .assets import assets
from .extensions import asset_cache, babel, cache, networkbar_cache, statsd, toolbar
from .utils import JSONEncoder, request_is_xhr

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

__all__ = ['baseframe']

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
        app.jinja_env.globals['get_locale'] = get_locale
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
                            alist.append(name + ext + str(spec))
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
                    alist.append(name + ext + str(spec))
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
                for _asset_key, _asset_path in asset_bundles['assets'].items():
                    app.config['assets'][_asset_key] = _asset_path

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


baseframe: BaseframeBlueprint = BaseframeBlueprint(
    'baseframe',
    __name__,
    static_folder='static',
    static_url_path='/_baseframe',
    template_folder='templates',
)
