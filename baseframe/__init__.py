# -*- coding: utf-8 -*-

import os
from flask import Blueprint, send_from_directory
from flaskext.assets import Bundle

__all__ = ['baseframe', 'baseframe_js']

baseframe = Blueprint('baseframe', __name__,
                      static_folder='static',
                      static_url_path='/baseframe',
                      template_folder='templates')

baseframe_js = Bundle('baseframe/js/foundation.js', 'baseframe/js/app.js',
                      filters='jsmin', output='js/packed.js')
baseframe_css = Bundle('baseframe/css/base.css',
                       filters='cssmin', output='css/packed.css')

@baseframe.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(baseframe.root_path, 'static', 'img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@baseframe.route('/humans.txt')
def humans():
    return send_from_directory(os.path.join(baseframe.root_path, 'static'),
                               'humans.txt', mimetype='text/plain')

@baseframe.route('/robots.txt')
def robots():
    return send_from_directory(os.path.join(baseframe.root_path, 'static'),
                               'robots.txt', mimetype='text/plain')
