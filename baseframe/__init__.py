# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
from datetime import datetime, timedelta
import requests
from pytz import timezone
from flask import (g, Blueprint, send_from_directory, render_template,
                    current_app, request, redirect, Markup)
from werkzeug.routing import NotFound, MethodNotAllowed, RequestRedirect
from coaster.views import render_with
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
    def init_app(self, app, requires=[], bundle_js=None, bundle_css=None, assetenv=None):
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
        app.register_blueprint(self)

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


baseframe = BaseframeBlueprint('baseframe', __name__,
    static_folder='static',
    static_url_path='/_baseframe',
    template_folder='templates')


@networkbar_cache.cached(key_prefix='networkbar_links')
def networkbar_links_fetcher():
    try:
        r = requests.get(current_app.config['NETWORKBAR_DATA'])
        return (r.json() if callable(r.json) else r.json).get('links', [])
    except:  # Catch all exceptions
        return []

def networkbar_links():
    links = current_app.config.get('NETWORKBAR_LINKS')
    if links:
        return links

    return networkbar_links_fetcher()


@baseframe.app_template_filter('render_field_options')
def render_field_options(field, **kwargs):
    """
    Remove HTML attributes with a value of None or False before rendering a field.
    """
    d = dict((k, v) for k, v in kwargs.items() if v is not None and v is not False)
    return field(**d)

@baseframe.app_template_filter('to_json')
def form_field_to_json(field, **kwargs):
    d = {}
    d['id'] = field.id
    d['label'] = field.label.text
    d['has_errors'] = bool(field.errors)
    d['errors'] = list(dict(error=e) for e in field.errors)
    d['is_listwidget'] = bool(hasattr(field.widget, 'html_tag') and field.widget.html_tag in ['ul', 'ol'])
    d['is_checkbox'] = (field.widget.input_type == 'checkbox')
    d['is_required'] = bool(field.flags.required)
    d['render_html'] = Markup(render_field_options(field, **kwargs))
    return d

@baseframe.app_context_processor
def baseframe_context():
    return {
        'networkbar_links': networkbar_links
    }


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


@baseframe.route('/favicon.ico')
def favicon():
    app_icon_path = current_app.static_folder
    # Does the app have a favicon.ico in /static?
    if not os.path.exists(os.path.join(app_icon_path, 'favicon.ico')):
        # Nope? Is it in /static/img?
        app_icon_path = os.path.join(current_app.static_folder, 'img')
        if not os.path.exists(os.path.join(app_icon_path, 'favicon.ico')):
            # Still nope? Serve default favicon from baseframe
            app_icon_path = os.path.join(baseframe.static_folder, 'img')
    return send_from_directory(app_icon_path,
      'favicon.ico', mimetype='image/vnd.microsoft.icon')


@baseframe.route('/humans.txt')
def humans():
    return send_from_directory(
        current_app.static_folder if os.path.exists(
            os.path.join(current_app.static_folder, 'humans.txt')) else baseframe.static_folder,
        'humans.txt', mimetype='text/plain')


@baseframe.route('/robots.txt')
def robots():
    return send_from_directory(
        current_app.static_folder if os.path.exists(
            os.path.join(current_app.static_folder, 'robots.txt')) else baseframe.static_folder,
        'robots.txt', mimetype='text/plain')


@baseframe.route('/_toastr_messages.js')
def toastr_messages_js():
    return current_app.response_class(render_template('toastr_messages.js'), mimetype='application/javascript')


@baseframe.route('/_editor.css')
def editorcss():
    response = current_app.response_class(render_template('editor.css'),
        mimetype='text/css',
        headers={'Expires': (datetime.utcnow() + timedelta(minutes=60)).strftime('%a, %d %b %Y %H:%M:%S GMT')})
    return response


@baseframe.app_errorhandler(404)
@render_with('404.html')
def error404(e):
    if request.path.endswith('/') and request.method == 'GET':
        newpath = request.path[:-1]
        try:
            adapter = current_app.url_map.bind_to_environ(request)
            matchinfo = adapter.match(newpath)
            if matchinfo[0] != request.endpoint:
                # Redirect only if it's not back to the same endpoint
                return redirect(request.url[:-1])
        except (NotFound, RequestRedirect, MethodNotAllowed):
            pass
    baseframe_translations.as_default()
    return {'error': "404 Not Found"}, 404


@baseframe.app_errorhandler(403)
@render_with('403.html')
def error403(e):
    baseframe_translations.as_default()
    return {'error': "403 Forbidden"}, 403


@baseframe.app_errorhandler(500)
@render_with('500.html')
def error500(e):
    baseframe_translations.as_default()
    return {'error': "500 Internal Server Error"}, 500


@baseframe.app_template_filter('age')
def age(dt):
    delta = datetime.utcnow() - dt
    if delta.days == 0:
        # < 1 day
        if delta.seconds < 10:
            return _(u"seconds ago")
        elif delta.seconds < 60:
            return _(u"%(num)s seconds ago", num=delta.seconds)
        elif delta.seconds < 120:
            return _(u"a minute ago")
        elif delta.seconds < 3600:  # < 1 hour
            return _(u"%(num)s minutes ago", num=int(delta.seconds / 60))
        elif delta.seconds < 7200:  # < 2 hours
            return _(u"an hour ago")
        else:
            return _("%(num)s hours ago", num=int(delta.seconds / 3600))
    elif delta.days == 1:
        return _(u"a day ago")
    elif delta.days < 30:
        return _(u"%(num)s days ago", num=delta.days)
    elif delta.days < 60:
        return _(u"a month ago")
    elif delta.days < 365:
        return _(u"%(num)s months ago", num=int(delta.days / 30))
    elif delta.days < 730:  # < 2 years
        return _(u"a year ago")
    else:
        return _(u"%(num)s years ago", num=int(delta.days / 365))


@baseframe.app_template_filter('usessl')
def usessl(url):
    """
    Convert a URL to https:// if SSL is enabled in site config
    """
    if not current_app.config.get('USE_SSL'):
        return url
    if url.startswith('//'):  # //www.example.com/path
        return 'https:' + url
    if url.startswith('/'):  # /path
        url = os.path.join(request.url_root, url[1:])
    if url.startswith('http:'):  # http://www.example.com
        url = 'https:' + url[5:]
    return url


@baseframe.app_template_filter('nossl')
def nossl(url):
    """
    Convert a URL to http:// if using SSL
    """
    if url.startswith('//'):
        return 'http:' + url
    if url.startswith('/') and request.url.startswith('https:'):  # /path and SSL is on
        url = os.path.join(request.url_root, url[1:])
    if url.startswith('https://'):
        return 'http:' + url[6:]
    return url


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
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response


# Replace gettext handlers for imports
b_ = _
b__ = __
from flask.ext.babelex import gettext as _, lazy_gettext as __

# Deprecated imports
from .deprecated import *
