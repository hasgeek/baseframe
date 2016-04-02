# -*- coding: utf-8 -*-

import os
import requests
from datetime import datetime, timedelta
from urlparse import urlparse, urljoin
from flask import current_app, send_from_directory, render_template, abort, request
from flask.ext.assets import Bundle
from flask.ext.wtf.csrf import generate_csrf
from coaster.utils import make_name
from coaster.assets import split_namespec
from coaster.views import render_with
from . import baseframe, networkbar_cache, asset_cache, assets as assets_repo


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


def asset_key(assets):
    return make_name('-'.join(assets).replace(
        '==', '-eq-').replace('>=', '-gte-').replace('<=', '-lte-').replace('>', '-gt-').replace('<', '-lt-'),
        maxlength=250)


def gen_assets_url(assets):
    try:
        names = [split_namespec(a)[0] for a in assets]
    except ValueError:
        abort(400)

    is_js = reduce(lambda status, name: status and name.endswith('.js'), names, True)
    is_css = reduce(lambda status, name: status and name.endswith('.css'), names, True)
    output_name = asset_key(assets)
    gendir = os.path.join(current_app.static_folder, 'gen')
    if not os.path.exists(gendir):
        os.mkdir(gendir)
    # The file extensions here are for upstream servers to serve the correct content type:
    if is_js:
        # TODO: Move this !jquery.js to somewhere more relevant
        bundle = Bundle(assets_repo.require(*(['!jquery.js'] + assets)),
            output='gen/' + output_name + '.js', filters='uglipyjs')
    elif is_css:
        bundle = Bundle(assets_repo.require(*assets),
            output='gen/' + output_name + '.css', filters=['cssrewrite', 'cssmin'])
    else:
        abort(400)

    bundle.env = current_app.assets
    return bundle.urls()[0]


def ext_assets(assets):
    key = asset_key(assets)
    url = asset_cache.get('assets/' + key)
    if url:
        return url
    if current_app.config.get('ASSET_SERVER'):
        try:
            r = requests.get(urljoin(current_app.config['ASSET_SERVER'], 'asset'),
                params={'a': assets},
                allow_redirects=False)
            if r.status_code in (301, 302, 303, 307):
                url = r.headers['location']
            else:  # XXX: What broke and failed to do a 3xx?
                url = r.url
            asset_cache.set('assets/' + key, url, timeout=current_app.config.get('ASSET_TIMEOUT', 60))
            return url
        except requests.exceptions.ConnectionError:
            return gen_assets_url(assets)
    else:
        return gen_assets_url(assets)


@baseframe.app_context_processor
def baseframe_context():
    return {
        'networkbar_links': networkbar_links,
        'csrf_token': generate_csrf,
    }


@baseframe.route('/favicon.ico', subdomain='<subdomain>')
@baseframe.route('/favicon.ico', defaults={'subdomain': None})
def favicon(subdomain=None):
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


@baseframe.route('/humans.txt', subdomain='<subdomain>')
@baseframe.route('/humans.txt', defaults={'subdomain': None})
def humans(subdomain=None):
    return send_from_directory(
        current_app.static_folder if os.path.exists(
            os.path.join(current_app.static_folder, 'humans.txt')) else baseframe.static_folder,
        'humans.txt', mimetype='text/plain')


@baseframe.route('/robots.txt', subdomain='<subdomain>')
@baseframe.route('/robots.txt', defaults={'subdomain': None})
def robots(subdomain=None):
    return send_from_directory(
        current_app.static_folder if os.path.exists(
            os.path.join(current_app.static_folder, 'robots.txt')) else baseframe.static_folder,
        'robots.txt', mimetype='text/plain')


@baseframe.route('/api/baseframe/1/toastr_messages.js', subdomain='<subdomain>')
@baseframe.route('/api/baseframe/1/toastr_messages.js', defaults={'subdomain': None})
def toastr_messages_js(subdomain=None):
    return current_app.response_class(render_template('toastr_messages.js'), mimetype='application/javascript')


@baseframe.route('/api/baseframe/1/editor.css', subdomain='<subdomain>')
@baseframe.route('/api/baseframe/1/editor.css', defaults={'subdomain': None})
def editorcss(subdomain=None):
    response = current_app.response_class(render_template('editor.css'),
        mimetype='text/css',
        headers={'Expires': (datetime.utcnow() + timedelta(minutes=60)).strftime('%a, %d %b %Y %H:%M:%S GMT')})
    return response


@baseframe.route('/api/baseframe/1/csrf/refresh', subdomain='<subdomain>')
@baseframe.route('/api/baseframe/1/csrf/refresh', defaults={'subdomain': None})
@render_with({
    'text/plain': lambda r: r['csrf_token'],
    }, json=True, jsonp=False)
def csrf_refresh(subdomain=None):
    parsed_host = urlparse(request.url_root)
    origin = parsed_host.scheme + u'://' + parsed_host.netloc
    if 'Origin' in request.headers:
        # Origin is present in (a) cross-site requests and (b) same site requests in some browsers.
        # Therefore, if Origin is present, confirm it matches our domain.
        if request.headers['Origin'] != origin:
            abort(403)

    return {'csrf_token': generate_csrf()}, 200, {
        'Access-Control-Allow-Origin': origin,
        'Vary': 'Origin',
        'Expires': (datetime.utcnow() + timedelta(minutes=10)).strftime('%a, %d %b %Y %H:%M:%S GMT')
        }
