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

bootstrap_js = Bundle('baseframe/js/bootstrap/bootstrap-alert.js',
                      'baseframe/js/bootstrap/bootstrap-button.js',
                      'baseframe/js/bootstrap/bootstrap-carousel.js',
                      'baseframe/js/bootstrap/bootstrap-collapse.js',
                      'baseframe/js/bootstrap/bootstrap-dropdown.js',
                      'baseframe/js/bootstrap/bootstrap-modal.js',
                      'baseframe/js/bootstrap/bootstrap-tooltip.js',
                      'baseframe/js/bootstrap/bootstrap-popover.js',
                      'baseframe/js/bootstrap/bootstrap-scrollspy.js',
                      'baseframe/js/bootstrap/bootstrap-tab.js',
                      'baseframe/js/bootstrap/bootstrap-transition.js',
                      'baseframe/js/bootstrap/bootstrap-typeahead.js',
                      filters='jsmin', output='baseframe/js/bootstrap.min.js')

baseframe_js = Bundle(jquery_js,
                      bootstrap_js,
                      filters='jsmin', output='baseframe/js/baseframe.min.js')


bootstrap_less = Bundle('baseframe/less/bootstrap/bootstrap.less',
                        'baseframe/less/bootstrap/responsive.less',
                        filters='less', output='baseframe/css/bootstrap.css',
                        debug=False)

baseframe_less = Bundle('baseframe/less/baseframe.less',
                        filters='less', output='baseframe/css/baseframe.css',
                        debug=False)

baseframe_css = Bundle(bootstrap_less,
                       baseframe_less,
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
