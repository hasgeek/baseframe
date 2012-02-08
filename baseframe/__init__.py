# -*- coding: utf-8 -*-

import os
from flask import Blueprint, send_from_directory
from flask.ext.assets import Bundle

__all__ = ['baseframe', 'baseframe_js', 'baseframe_css']

baseframe = Blueprint('baseframe', __name__,
                      static_folder='static',
                      static_url_path='/baseframe',
                      template_folder='templates')

jquery_js = Bundle('baseframe/js/jquery-1.7.1.js',
                   filters='jsmin', output='baseframe/js/jquery.min.js')

foundation_js = Bundle('baseframe/js/foundation/jquery.customforms.js',
                       'baseframe/js/foundation/jquery.orbit-1.4.0.js',
                       'baseframe/js/foundation/jquery.placeholder.js',
                       'baseframe/js/foundation/jquery.reveal.js',
                       'baseframe/js/foundation/jquery.tooltips.js',
                       filters='jsmin', output='baseframe/js/foundation.min.js')

baseframe_js = Bundle('baseframe/js/foundation/modernizr.foundation.js',
                      jquery_js, foundation_js,
                      'baseframe/js/networkbar.js',
                      'baseframe/js/baseframe.js',
                      filters='jsmin', output='baseframe/js/packed.js')

# Sass templates are compiled to CSS externally to avoid Sass as a dependency
# in deployment.
baseframe_css = Bundle('baseframe/css/baseframe.css',
                       filters='cssmin', output='baseframe/css/packed.css')


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
