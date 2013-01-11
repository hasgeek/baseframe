# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
from flask import Blueprint, send_from_directory, render_template, current_app
from flask.ext.assets import Bundle

__all__ = ['baseframe', 'baseframe_js', 'baseframe_css']

baseframe = Blueprint('baseframe', __name__,
                      static_folder='static',
                      static_url_path='/_baseframe',
                      template_folder='templates')

jquery_js = Bundle('baseframe/js/jquery-1.7.1.js',
                   filters='jsmin', output='js/baseframe-jquery.min.js')


bootstrap_js = Bundle('baseframe/js/bootstrap/bootstrap-alert.js',
                      'baseframe/js/bootstrap/bootstrap-button.js',
#                      'baseframe/js/bootstrap/bootstrap-carousel.js',
#                      'baseframe/js/bootstrap/bootstrap-collapse.js',
                      'baseframe/js/bootstrap/bootstrap-dropdown.js',
                      'baseframe/js/bootstrap/bootstrap-modal.js',
                      'baseframe/js/bootstrap/bootstrap-tooltip.js',
#                      'baseframe/js/bootstrap/bootstrap-popover.js',
#                      'baseframe/js/bootstrap/bootstrap-scrollspy.js',
                      'baseframe/js/bootstrap/bootstrap-tab.js',
                      'baseframe/js/bootstrap/bootstrap-transition.js',
#                      'baseframe/js/bootstrap/bootstrap-typeahead.js',
                      )


extra_js = Bundle('baseframe/js/jquery.form.js',
                  'baseframe/js/tiny_mce/jquery.tinymce.js',
                  'baseframe/js/bootstrap-datepicker.js',
                  'baseframe/js/jquery.timepicker.js',
                  # 'baseframe/js/chosen.jquery.js',
                  'baseframe/js/select2.js',
                  )

networkbar_js = Bundle('baseframe/js/networkbar.js')

baseframe_js = Bundle(jquery_js,
                      bootstrap_js,
                      extra_js,
                      networkbar_js,
                      'baseframe/js/baseframe.js', debug=False,
                      filters='jsmin', output='js/baseframe-packed.js')

# Optional extras
mousetrap_js = Bundle('baseframe/js/mousetrap.js')
toastr_js = Bundle('baseframe/js/toastr.js')
expander_js = Bundle('baseframe/js/jquery.expander.js')
cookie_js = Bundle('baseframe/js/jquery.cookie.js')
timezone_js = Bundle('baseframe/js/detect_timezone.js')
socialite_js = Bundle('baseframe/js/socialite.js')
swfobject_js = Bundle('baseframe/js/swfobject.js')

#bootstrap_less = Bundle('baseframe/less/bootstrap/bootstrap.less',
#                        'baseframe/less/bootstrap/responsive.less',
#                        filters='less', output='baseframe/css/bootstrap.css',
#                        debug=False)

networkbar_css = Bundle('baseframe/css/networkbar.css')
baseframe_css = Bundle(  # bootstrap_less,
                       'baseframe/css/bootstrap.css',   # Externally compiled with Less
                       'baseframe/css/responsive.css',  # Externally compiled with Less
                       # 'baseframe/css/chosen.css',      # Companion to chosen.jquery.js
                       'baseframe/css/select2.css',     # Companion to select2.js
                       'baseframe/css/jquery.timepicker.css',  # For timepicker
                       'baseframe/css/baseframe.css',   # Externally compiled with Compass
                       networkbar_css,                  # Externally compiled with Compass
                       filters='cssmin',
                       output='css/baseframe-packed.css')

# Optional extras
toastr_css = Bundle('baseframe/css/toastr.css')
animate_css = Bundle('baseframe/css/animate.css')


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
def error404(e):
    return render_template('404.html'), 404


@baseframe.app_errorhandler(403)
def error403(e):
    return render_template('403.html'), 403


@baseframe.app_errorhandler(500)
def error500(e):
    return render_template('500.html'), 500


@baseframe.after_app_request
def process_response(response):
    # Prevent pages from being placed in an iframe. If the response already
    # set has a value for this option, let it pass through
    if 'X-Frame-Options' in response.headers:
        frameoptions = response.headers.get('X-Frame-Options')
        if not frameoptions or frameoptions == 'ALLOW':
            response.headers.pop('X-Frame-Options')
    else:
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response
