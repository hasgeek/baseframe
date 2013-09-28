# -*- coding: utf-8 -*-

from __future__ import absolute_import
from coaster.assets import VersionedAssets, Version
from . import __version__


#: Semantic-versioned assets
assets = VersionedAssets()

assets['jquery.js'][Version('1.7.1')] = 'baseframe/js/jquery-1.7.1.js'
assets['jquery.js'][Version('1.8.3')] = 'baseframe/js/jquery-1.8.3.js'
assets['jquery.js'][Version('1.9.1')] = 'baseframe/js/jquery-1.9.1.js'

assets['baseframe-networkbar.js'][Version(__version__)] = 'baseframe/js/networkbar.js'
assets['baseframe-networkbar.css'][Version(__version__)] = 'baseframe/css/networkbar.css'
assets['baseframe-base.js'][Version(__version__)] = 'baseframe/js/baseframe.js'
assets['baseframe-base.css'][Version(__version__)] = 'baseframe/css/baseframe.css'
assets['baseframe-bs3-custom.css'][Version(__version__)] = 'baseframe/css/baseframe-bs3-custom.css'

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

# Bootstrap 3.0.0-WIP
assets['bootstrap.css'][Version('3.0.0')] = 'baseframe/css/bootstrap3/bootstrap.css'
assets['bootstrap-affix.js'][Version('3.0.0')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/affix.js')
assets['bootstrap-alert.js'][Version('3.0.0')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/alert.js')
assets['bootstrap-button.js'][Version('3.0.0')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/button.js')
assets['bootstrap-carousel.js'][Version('3.0.0')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/carousel.js')
assets['bootstrap-collapse.js'][Version('3.0.0')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/collapse.js')
assets['bootstrap-dropdown.js'][Version('3.0.0')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/dropdown.js')
assets['bootstrap-modal.js'][Version('3.0.0')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/modal.js')
assets['bootstrap-popover.js'][Version('3.0.0')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/popover.js')
assets['bootstrap-scrollspy.js'][Version('3.0.0')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/scrollspy.js')
assets['bootstrap-tab.js'][Version('3.0.0')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/tab.js')
assets['bootstrap-tooltip.js'][Version('3.0.0')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/tooltip.js')
assets['bootstrap-transition.js'][Version('3.0.0')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/transition.js')

assets['jquery.form.js'][Version('2.96.0')] = ('jquery.js', 'baseframe/js/jquery.form.js')
assets['jquery.tinymce.js'][Version('3.5.8')] = ('jquery.js', 'baseframe/js/tiny_mce/jquery.tinymce.js')
assets['tiny_mce.js'][Version('3.5.8')] = 'baseframe/js/tiny_mce/tiny_mce.js'
assets['bootstrap-datepicker.js'][Version('1.3.0')] = ('jquery.js', 'baseframe/js/bootstrap-datepicker.js')

assets['jquery.ui.js'][Version('1.10.3')] = ('jquery.js', 'baseframe/js/jquery-ui.js')
assets['jquery.ui.css'][Version('1.10.3')] = 'baseframe/css/jquery-ui.css'

assets['jquery.range-slider.js'][Version('5.3.0')] = ('jquery.js', 'baseframe/js/jQRangeSlider-min.js')
assets['jquery.range-slider.css'][Version('5.3.0')] = 'baseframe/css/jQRangeSlider.css'

assets['jquery.textarea-expander.js'][Version('1.0.0')] = ('jquery.js', 'baseframe/js/jquery.textarea-expander.js')

assets['jquery.oembed.js'][Version('1.0.0')] = ('jquery.js', 'baseframe/js/jquery.oembed.js')

assets['jquery.timepicker.js'][Version('1.0.7')] = ('jquery.js>=1.7.0', 'baseframe/js/jquery.timepicker.js')
assets['jquery.timepicker.css'][Version('1.0.7')] = 'baseframe/css/jquery.timepicker.css'

assets['select2.js'][Version('3.3.2')] = ('jquery.js>=1.4.6', 'baseframe/js/select2.js')
assets['select2.css'][Version('3.3.2')] = 'baseframe/css/select2.css'

assets['codemirror.js'][Version('3.16.0')] = 'baseframe/js/codemirror/lib/codemirror.js'
assets['codemirror.mode.markdown.js'][Version('3.16.0')] = 'baseframe/js/codemirror/mode/markdown/markdown.js'
assets['codemirror.mode.gfm.js'][Version('3.16.0')] = 'baseframe/js/codemirror/mode/gfm/gfm.js'
assets['codemirror.mode.htmlmixed.js'][Version('3.16.0')] = 'baseframe/js/codemirror/mode/htmlmixed/htmlmixed.js'
assets['codemirror.addon.mode.overlay.js'][Version('3.16.0')] = 'baseframe/js/codemirror/addon/mode/overlay.js'
assets['codemirror.addon.edit.continuelist.js'][Version('3.16.0')] = 'baseframe/js/codemirror/addon/edit/continuelist.js'
assets['codemirror.css'][Version('3.16.0')] = 'baseframe/js/codemirror/lib/codemirror.css'

assets['codemirror-markdown.js'][Version('3.16.0')] = {'requires': [
    'codemirror.js==3.16.0',
    'codemirror.mode.markdown.js==3.16.0',
    'codemirror.mode.gfm.js==3.16.0',
    'codemirror.mode.htmlmixed.js==3.16.0',
    'codemirror.addon.mode.overlay.js==3.16.0',
    'codemirror.addon.edit.continuelist.js==3.16.0',
]}
assets['codemirror-markdown.css'][Version('3.16.0')] = ('codemirror.css==3.16.0', 'baseframe/css/codemirror.css')

assets['mousetrap.js'][Version('1.1.2')] = 'baseframe/js/mousetrap.js'
assets['toastr.js'][Version('1.2.2')] = 'baseframe/js/toastr.js'
assets['toastr.css'][Version('1.2.2')] = 'baseframe/css/toastr.css'

assets['jquery.expander.js'][Version('1.4.5')] = ('jquery.js', 'baseframe/js/jquery.expander.js')
assets['jquery.cookie.js'][Version('1.3.0')] = ('jquery.js', 'baseframe/js/jquery.cookie.js')
assets['jquery.sparkline.js'][Version('2.1.2')] = ('jquery.js', 'baseframe/js/jquery.sparkline.js')
assets['timezone.js'][Version('0.0.0')] = 'baseframe/js/detect_timezone.js'
assets['socialite.js'][Version('2.0.0')] = 'baseframe/js/socialite.js'
assets['swfobject.js'][Version('2.2.0')] = 'baseframe/js/swfobject.js'
assets['parsley.js'][Version('1.1.13')] = ('jquery.js', 'baseframe/js/parsley.js')
assets['parsley.extend.js'][Version('1.1.13')] = ('parsley.js', 'baseframe/js/parsley.extend.js')

assets['animate.css'][Version('0.0.0')] = 'baseframe/css/animate.css'

assets['matchmedia.js'][Version('0.0.0')] = 'baseframe/js/matchmedia.js'
assets['picturefill.js'][Version('0.1.0')] = ('matchmedia.js', 'baseframe/js/picturefill.js')

assets['dropzone.js'][Version('3.2.0')] = 'baseframe/js/dropzone.js'
assets['dropzone.css'][Version('3.2.0')] = 'baseframe/css/dropzone.css'

assets['mustache-hogan.js'][Version('2.0.0')] = 'baseframe/js/mustache-hogan/hogan-2.0.0.min.mustache.js'
assets['mustache-loader.js'][Version('0.5.1')] = 'baseframe/js/mustache-hogan/mustache-loader.js'

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

assets['bootstrap.js'][Version('3.0.0')] = {'requires': [
    'bootstrap-transition.js==3.0.0',
    'bootstrap-alert.js==3.0.0',
    'bootstrap-button.js==3.0.0',
    'bootstrap-carousel.js==3.0.0',
    'bootstrap-collapse.js==3.0.0',
    'bootstrap-dropdown.js==3.0.0',
    'bootstrap-modal.js==3.0.0',
    'bootstrap-tooltip.js==3.0.0',
    'bootstrap-popover.js==3.0.0',
    'bootstrap-scrollspy.js==3.0.0',
    'bootstrap-tab.js==3.0.0',
    'bootstrap-affix.js==3.0.0',
]}

assets['mustache.js'][Version('2.0.0')] = {'requires': [
    'mustache-loader.js==0.5.1',
    'mustache-hogan.js==2.0.0',
]}

assets['extra.js'][Version('0.0.0')] = {'requires': [
    'jquery.form.js',
    'jquery.tinymce.js',
    'bootstrap-datepicker.js',
    'jquery.timepicker.js',
    'select2.js',
    'mustache.js',
]}

assets['baseframe.js'][Version(__version__)] = {'requires': [
    'jquery.js<1.9.0',
    'bootstrap.js==2.0.1',
    'extra.js',
    'baseframe-base.js==' + __version__,
    'baseframe-networkbar.js==' + __version__,
]}

assets['baseframe.css'][Version(__version__)] = {'requires': [
    'bootstrap.css==2.0.1',
    'bootstrap-responsive.css==2.0.1',
    'select2.css',
    'jquery.timepicker.css',
    'baseframe-base.css==' + __version__,
    'baseframe-networkbar.css==' + __version__,
]}

assets['baseframe-bs3.js'][Version(__version__)] = {'requires': [
    'jquery.js>=1.9.0',
    'bootstrap.js>=3.0.0',
    'extra.js',
    'baseframe-base.js==' + __version__,
    'baseframe-networkbar.js==' + __version__,
]}

assets['baseframe-bs3.css'][Version(__version__)] = {'requires': [
    'bootstrap.css>=3.0.0',
    'select2.css',
    'jquery.timepicker.css',
    'baseframe-base.css==' + __version__,
    'baseframe-networkbar.css==' + __version__,
    'baseframe-bs3-custom.css',
]}
