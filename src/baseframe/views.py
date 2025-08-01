"""Baseframe views and view support helpers."""
# ruff: noqa: ARG001

import os
import os.path
from datetime import timedelta
from typing import Any, Optional
from urllib.parse import urlparse

import requests
from flask import (
    Response,
    abort,
    current_app,
    render_template,
    request,
    send_from_directory,
)
from flask_assets import Bundle
from flask_wtf.csrf import generate_csrf

from coaster.assets import split_namespec
from coaster.auth import current_auth, request_has_auth
from coaster.utils import make_name
from coaster.views import ReturnRenderWith, render_with

from .assets import assets as assets_repo
from .blueprint import baseframe
from .extensions import networkbar_cache
from .utils import ctx_has_locale, request_checked_xhr, request_timestamp


@networkbar_cache.cached(key_prefix='networkbar_links')
def networkbar_links_fetcher() -> list:
    """Fetch networkbar links (helper for :func:`networkbar_links`)."""
    try:
        r = requests.get(current_app.config['NETWORKBAR_DATA'], timeout=30)
        return r.json().get('links', [])
    except requests.exceptions.RequestException:
        return []


def networkbar_links() -> list:
    """Return networkbar links."""
    links = current_app.config.get('NETWORKBAR_LINKS')
    if links:
        return links

    return networkbar_links_fetcher()


def asset_key(assets: list[str]) -> str:
    """Convert multiple version specs into a URL-friendly key."""
    return make_name(
        '-'.join(assets)
        .replace('==', '-eq-')
        .replace('>=', '-gte-')
        .replace('<=', '-lte-')
        .replace('>', '-gt-')
        .replace('<', '-lt-'),
        maxlength=250,
    )


def gen_assets_url(assets: list[str]) -> str:
    """Create an asset bundle and return URL (helper for :func:`ext_assets`)."""
    # TODO: write test for this function
    try:
        names = [split_namespec(a)[0] for a in assets]
    except ValueError:
        abort(400)

    is_js = all(name.endswith('.js') for name in names)
    is_css = all(name.endswith('.css') for name in names)
    output_name = asset_key(assets)
    gendir = os.path.join(current_app.static_folder, 'gen')  # type: ignore[arg-type]
    if not os.path.exists(gendir):
        os.mkdir(gendir)
    # File extensions are for upstream servers to serve the correct content type:
    if is_js:
        bundle = Bundle(
            assets_repo.require(*assets),
            output='gen/' + output_name + '.js',
            filters='rjsmin',
        )
    elif is_css:
        bundle = Bundle(
            assets_repo.require(*assets),
            output='gen/' + output_name + '.css',
            filters=['cssrewrite', 'cssmin'],
        )
    else:
        abort(400)

    # pylint: disable=possibly-used-before-assignment
    bundle.env = current_app.assets  # type: ignore[attr-defined]
    return bundle.urls()[0]


def ext_assets(assets: list[str]) -> str:
    """Return a URL to the required external assets."""
    # XXX: External assets are deprecated, so this function serves them as internal
    # assets
    return gen_assets_url(assets)


def asset_path(bundle_key: str) -> str:
    """Return URL path to an asset bundle."""
    asset_base_path = current_app.config.get('ASSET_BASE_PATH', '')
    asset_file = current_app.config.get('assets', {}).get(bundle_key)
    if not asset_file:
        raise LookupError(f"Missing asset file for {bundle_key}.")
    return os.path.join(asset_base_path, asset_file)


@baseframe.app_context_processor
def baseframe_context() -> dict[str, Any]:
    """Add Baseframe helper functions to Jinja2 template context."""
    return {'networkbar_links': networkbar_links, 'asset_path': asset_path}


@baseframe.route('/favicon.ico', subdomain='<subdomain>')
@baseframe.route('/favicon.ico', defaults={'subdomain': None})
def favicon(subdomain: Optional[str] = None) -> Response:
    """Render a favicon from the app's static folder, falling back to default icon."""
    app_icon_path: Optional[str] = None
    app_icon_folder = current_app.static_folder
    # Does the app have a favicon.ico in /static?
    if not os.path.exists(
        os.path.join(app_icon_folder, 'favicon.ico')  # type: ignore[arg-type]
    ):
        # Nope? Is it in /static/img?
        app_icon_path = os.path.join(
            current_app.static_folder or '',
            'img',
        )
        if not os.path.exists(os.path.join(app_icon_path, 'favicon.ico')):
            # Still nope? Serve default favicon from baseframe
            app_icon_path = os.path.join(
                baseframe.static_folder or '',
                'img',
            )
    if not app_icon_path:
        abort(404)
    return send_from_directory(
        app_icon_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )


@baseframe.route('/humans.txt', subdomain='<subdomain>')
@baseframe.route('/humans.txt', defaults={'subdomain': None})
def humans(subdomain: Optional[str] = None) -> Response:
    """Render humans.txt from app's static folder, falling back to default file."""
    return send_from_directory(
        (
            current_app.static_folder
            if os.path.exists(
                os.path.join(
                    current_app.static_folder or '',
                    'humans.txt',  # type: ignore[arg-type]
                )
            )
            else baseframe.static_folder
        ),
        'humans.txt',
        mimetype='text/plain',
    )


@baseframe.route('/robots.txt', subdomain='<subdomain>')
@baseframe.route('/robots.txt', defaults={'subdomain': None})
def robots(subdomain: Optional[str] = None) -> Response:
    """Render robots.txt from app's static folder, falling back to default file."""
    return send_from_directory(
        (
            current_app.static_folder
            if os.path.exists(
                os.path.join(
                    current_app.static_folder or '',
                    'robots.txt',  # type: ignore[arg-type]
                )
            )
            else baseframe.static_folder
        ),
        'robots.txt',
        mimetype='text/plain',
    )


@baseframe.route('/.well-known/<path:filename>', subdomain='<subdomain>')
@baseframe.route('/.well-known/<path:filename>', defaults={'subdomain': None})
def well_known(filename: str, subdomain: Optional[str] = None) -> Response:
    """Render .well-known folder contents from app's static folder."""
    well_known_path = os.path.join(
        current_app.static_folder or '',
        '.well-known',  # type: ignore[arg-type]
    )
    return send_from_directory(well_known_path, filename)


@baseframe.route('/api/baseframe/1/toastr_messages.js', subdomain='<subdomain>')
@baseframe.route('/api/baseframe/1/toastr_messages.js', defaults={'subdomain': None})
def toastr_messages_js(subdomain: Optional[str] = None) -> Response:
    """Return all pending flash messages as Toastr notifications."""
    return current_app.response_class(
        render_template('toastr_messages.js.jinja2'), mimetype='application/javascript'
    )


@baseframe.route('/api/baseframe/1/editor.css', subdomain='<subdomain>')
@baseframe.route('/api/baseframe/1/editor.css', defaults={'subdomain': None})
def editorcss(subdomain: Optional[str] = None) -> Response:
    """Render a minimal CSS file for TinyMCE's iframe-based editor."""
    return current_app.response_class(
        render_template('editor.css.jinja2'),
        mimetype='text/css',
        headers={
            'Expires': (request_timestamp() + timedelta(minutes=60)).strftime(
                '%a, %d %b %Y %H:%M:%S GMT'
            )
        },
    )


@baseframe.route('/api/baseframe/1/csrf/refresh', subdomain='<subdomain>')
@baseframe.route('/api/baseframe/1/csrf/refresh', defaults={'subdomain': None})
@render_with({'text/plain': lambda r: r['csrf_token']}, json=True)
def csrf_refresh(subdomain: Optional[str] = None) -> ReturnRenderWith:
    """Serve a refreshed CSRF token to ensure HTML forms never expire."""
    parsed_host = urlparse(request.url_root)
    origin = parsed_host.scheme + '://' + parsed_host.netloc
    # Origin is present in (a) cross-site requests and (b) same site requests in some
    # browsers. Therefore, if Origin is present, confirm it matches our domain
    if 'Origin' in request.headers and request.headers['Origin'] != origin:
        abort(403)

    return (
        {'csrf_token': generate_csrf()},
        200,
        {
            'Access-Control-Allow-Origin': origin,
            'Vary': 'Origin',
            'Expires': (request_timestamp() + timedelta(minutes=10)).strftime(
                '%a, %d %b %Y %H:%M:%S GMT'
            ),
        },
    )


@baseframe.after_app_request
def process_response(response: Response) -> Response:
    """Process response objects to add additional headers."""
    if (
        request.endpoint in ('static', 'baseframe.static')
        and 'Access-Control-Allow-Origin' not in response.headers
    ):
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

    # If request_is_xhr() was called, add a Vary header for that
    if request_checked_xhr():
        response.vary.add('X-Requested-With')

    # Prevent pages from being placed in an iframe. If the response already
    # set has a value for this option, let it pass through
    if 'X-Frame-Options' in response.headers:
        frameoptions = response.headers.get('X-Frame-Options')
        if not frameoptions or frameoptions == 'ALLOW':
            # 'ALLOW' is an unofficial signal from the app to Baseframe.
            # It signals us to remove the header and not set a default
            response.headers.pop('X-Frame-Options')
    elif request_has_auth() and getattr(current_auth, 'login_required', False):
        # Protect only login_required pages from appearing in frames
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'

    # In memoriam. http://www.gnuterrypratchett.com/
    response.headers['X-Clacks-Overhead'] = 'GNU Terry Pratchett'

    return response
