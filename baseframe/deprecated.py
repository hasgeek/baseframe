# -*- coding: utf-8 -*-

"""
Deprecated declarations. Will be removed in Baseframe 0.3.0
"""

from __future__ import absolute_import
from webassets import Bundle


# --- Legacy asset declarations below will be dropped in baseframe 0.3 --------

jquery_js = Bundle('baseframe/js/jquery-1.7.1.js',
                   filters='closure_js', output='js/baseframe-jquery.min.js')


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

baseframe_js = Bundle(  # jquery_js,  # Not required since baseframe.html now loads from CDN
                        bootstrap_js,
                        extra_js,
                        networkbar_js,
                        'baseframe/js/baseframe.js', debug=False,
                        filters='closure_js', output='js/baseframe-packed.js')

# Optional extras
mousetrap_js = Bundle('baseframe/js/mousetrap.js')
toastr_js = Bundle('baseframe/js/toastr.js')
expander_js = Bundle('baseframe/js/jquery.expander.js')
cookie_js = Bundle('baseframe/js/jquery.cookie.js')
timezone_js = Bundle('baseframe/js/detect_timezone.js')
socialite_js = Bundle('baseframe/js/socialite.js')
swfobject_js = Bundle('baseframe/js/swfobject.js')
parsley_js = Bundle('baseframe/js/parsley.js')
parsley_extend_js = Bundle('baseframe/js/parsley.extend.js')

# bootstrap_less = Bundle('baseframe/less/bootstrap/bootstrap.less',
#                         'baseframe/less/bootstrap/responsive.less',
#                         filters='less', output='baseframe/css/bootstrap.css',
#                         debug=False)

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
