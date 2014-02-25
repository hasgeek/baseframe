# -*- coding: utf-8 -*-

from . import baseframe, networkbar_cache
from .forms import Form
import os
import requests
from datetime import datetime, timedelta
from flask import current_app, send_from_directory, render_template


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


@baseframe.app_context_processor
def baseframe_context():
    return {
        'networkbar_links': networkbar_links,
        'csrf_form': Form(),
    }


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


@baseframe.route('/api/baseframe/1/toastr_messages.js')
def toastr_messages_js():
    return current_app.response_class(render_template('toastr_messages.js'), mimetype='application/javascript')


@baseframe.route('/api/baseframe/1/editor.css')
def editorcss():
    response = current_app.response_class(render_template('editor.css'),
        mimetype='text/css',
        headers={'Expires': (datetime.utcnow() + timedelta(minutes=60)).strftime('%a, %d %b %Y %H:%M:%S GMT')})
    return response