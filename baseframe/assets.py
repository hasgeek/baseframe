# -*- coding: utf-8 -*-

from __future__ import absolute_import
from coaster.assets import VersionedAssets, Version

__version = '0.2.14'

#: Semantic-versioned assets
assets = VersionedAssets()


assets['jquery.js'][Version('1.7.1')] = 'baseframe/js/jquery-1.7.1.js'
assets['jquery.js'][Version('1.8.3')] = 'baseframe/js/jquery-1.8.3.js'

assets['baseframe-networkbar.js'][Version(__version)] = 'baseframe/js/networkbar.js'
assets['baseframe-networkbar.css'][Version(__version)] = 'baseframe/css/networkbar.css'
assets['baseframe-base.js'][Version(__version)] = 'baseframe/js/baseframe.js'
assets['baseframe-base.css'][Version(__version)] = 'baseframe/css/baseframe.css'

# Bootstrap 2.0.1
assets['bootstrap.css'][Version('2.0.1')] = 'baseframe/css/bootstrap.css'
assets['bootstrap-responsive.css'][Version('2.0.1')] = 'baseframe/css/responsive.css'
assets['bootstrap-alert.js'][Version('2.0.1')] = ('jquery.js', 'baseframe/js/bootstrap/bootstrap-alert.js')
assets['bootstrap-button.js'][Version('2.0.1')] = ('jquery.js', 'baseframe/js/bootstrap/bootstrap-button.js')
assets['bootstrap-carousel.js'][Version('2.0.1')] = ('jquery.js', 'baseframe/js/bootstrap/bootstrap-carousel.js')
assets['bootstrap-collapse.js'][Version('2.0.1')] = ('jquery.js', 'baseframe/js/bootstrap/bootstrap-collapse.js')
assets['bootstrap-dropdown.js'][Version('2.0.1')] = ('jquery.js', 'baseframe/js/bootstrap/bootstrap-dropdown.js')
assets['bootstrap-modal.js'][Version('2.0.1')] = ('jquery.js', 'baseframe/js/bootstrap/bootstrap-modal.js')
assets['bootstrap-tooltip.js'][Version('2.0.1')] = ('jquery.js', 'baseframe/js/bootstrap/bootstrap-tooltip.js')
assets['bootstrap-popover.js'][Version('2.0.1')] = ('jquery.js', 'baseframe/js/bootstrap/bootstrap-popover.js')
assets['bootstrap-scrollspy.js'][Version('2.0.1')] = ('jquery.js', 'baseframe/js/bootstrap/bootstrap-scrollspy.js')
assets['bootstrap-tab.js'][Version('2.0.1')] = ('jquery.js', 'baseframe/js/bootstrap/bootstrap-tab.js')
assets['bootstrap-transition.js'][Version('2.0.1')] = ('jquery.js', 'baseframe/js/bootstrap/bootstrap-transition.js')
assets['bootstrap-typeahead.js'][Version('2.0.1')] = ('jquery.js', 'baseframe/js/bootstrap/bootstrap-typeahead.js')

assets['jquery.form.js'][Version('2.96.0')] = ('jquery.js', 'baseframe/js/jquery.form.js')
assets['jquery.tinymce.js'][Version('3.5.7')] = ('jquery.js', 'baseframe/js/tiny_mce/jquery.tinymce.js')
assets['bootstrap-datepicker.js'][Version('1.3.0')] = ('jquery.js', 'baseframe/js/bootstrap-datepicker.js')

assets['jquery.timepicker.js'][Version('1.0.7')] = ('jquery.js>=1.7.0', 'baseframe/js/jquery.timepicker.js')
assets['jquery.timepicker.css'][Version('1.0.7')] = 'baseframe/css/jquery.timepicker.css'

assets['select2.js'][Version('3.3.1')] = ('jquery.js>=1.4.6', 'baseframe/js/select2.js')
assets['select2.css'][Version('3.3.1')] = 'baseframe/css/select2.css'

assets['mousetrap.js'][Version('1.1.2')] = 'baseframe/js/mousetrap.js'
assets['toastr.js'][Version('1.2.2')] = 'baseframe/js/toastr.js'
assets['toastr.css'][Version('1.2.2')] = 'baseframe/css/toastr.css'

assets['jquery.expander.js'][Version('1.4.5')] = ('jquery.js', 'baseframe/js/jquery.expander.js')
assets['jquery.cookie.js'][Version('1.3.0')] = ('jquery.js', 'baseframe/js/jquery.cookie.js')
assets['timezone.js'][Version('0.0.0')] = 'baseframe/js/detect_timezone.js'
assets['socialite.js'][Version('2.0.0')] = 'baseframe/js/socialite.js'
assets['swfobject.js'][Version('2.2.0')] = 'baseframe/js/swfobject.js'
assets['parsley.js'][Version('1.1.13')] = ('jquery.js', 'baseframe/js/parsley.js')
assets['parsley.extend.js'][Version('1.1.13')] = ('parsley.js', 'baseframe/js/parsley.extend.js')

assets['animate.css'][Version('0.0.0')] = 'baseframe/css/animate.css'

# Asset packages
assets['bootstrap.js'][Version('2.0.1')] = {'requires': [
    'bootstrap-alert.js==2.0.1',
    'bootstrap-button.js==2.0.1',
    #'bootstrap-carousel.js==2.0.1',
    #'bootstrap-collapse.js==2.0.1',
    'bootstrap-dropdown.js==2.0.1',
    'bootstrap-modal.js==2.0.1',
    'bootstrap-tooltip.js==2.0.1',
    #'bootstrap-popover.js==2.0.1',
    #'bootstrap-scrollspy.js==2.0.1',
    'bootstrap-tab.js==2.0.1',
    'bootstrap-transition.js==2.0.1',
    #'bootstrap-typeahead.js==2.0.1',
    ]}

assets['extra.js'][Version('0.0.0')] = {'requires': [
    'jquery.form.js',
    'jquery.tinymce.js',
    'bootstrap-datepicker.js',
    'jquery.timepicker.js',
    'select2.js',
    ]}

assets['baseframe.js'][Version(__version)] = {'requires': [
    'jquery.js',
    'boostrap.js==2.0.1',
    'extra.js',
    'baseframe-base.js==' + __version,
    'baseframe-networkbar.js' + __version,
    ]}

assets['baseframe.css'][Version(__version)] = {'requires': [
    'bootstrap.css==2.0.1',
    'bootstrap-responsive.css==2.0.1',
    'select2.css',
    'jquery.timepicker.css',
    'baseframe-base.css==' + __version,
    'baseframe-networkbar.css==' + __version,
    ]}
