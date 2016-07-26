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
assets['baseframe-base-bs3.css'][Version(__version__)] = 'baseframe/css/baseframe-bs3.css'

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

# Bootstrap 3.3.1
assets['bootstrap.css'][Version('3.3.1')] = 'baseframe/css/bootstrap3/bootstrap.css'
assets['bootstrap-affix.js'][Version('3.3.1')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/affix.js')
assets['bootstrap-alert.js'][Version('3.3.1')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/alert.js')
assets['bootstrap-button.js'][Version('3.3.1')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/button.js')
assets['bootstrap-carousel.js'][Version('3.3.1')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/carousel.js')
assets['bootstrap-collapse.js'][Version('3.3.1')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/collapse.js')
assets['bootstrap-dropdown.js'][Version('3.3.1')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/dropdown.js')
assets['bootstrap-modal.js'][Version('3.3.1')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/modal.js')
assets['bootstrap-popover.js'][Version('3.3.1')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/popover.js')
assets['bootstrap-scrollspy.js'][Version('3.3.1')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/scrollspy.js')
assets['bootstrap-tab.js'][Version('3.3.1')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/tab.js')
assets['bootstrap-tooltip.js'][Version('3.3.1')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/tooltip.js')
assets['bootstrap-transition.js'][Version('3.3.1')] = ('jquery.js>=1.9.0', 'baseframe/js/bootstrap3/transition.js')

# Bootstrap Social - commit #918fc55c3c938377a7618ec0f115846e50d4b883
assets['bootstrap-social.css'][Version('1.0.0')] = ('bootstrap.css>=3.0.0', 'baseframe/css/bootstrap-social.css')

assets['jquery.form.js'][Version('2.96.0')] = ('jquery.js', 'baseframe/js/jquery.form.js')
assets['jquery.tinymce.js'][Version('3.5.10')] = ('jquery.js', 'baseframe/js/tinymce3/jquery.tinymce.js')
assets['tinymce.js'][Version('3.5.10')] = 'baseframe/js/tinymce3/tiny_mce.js'
assets['tiny_mce.js'][Version('3.5.10')] = {'requires': ['tinymce.js==3.5.10']}
assets['jquery.tinymce.js'][Version('4.1.7')] = ('jquery.js', 'baseframe/js/tinymce4/jquery.tinymce.min.js')
assets['tinymce.js'][Version('4.1.7')] = 'baseframe/js/tinymce4/tinymce.min.js'
assets['bootstrap-datepicker.js'][Version('1.3.0')] = ('jquery.js', 'baseframe/js/bootstrap-datepicker.js')

assets['jquery.ui.js'][Version('1.10.3')] = ('jquery.js', 'baseframe/js/jquery-ui.js')
assets['jquery.ui.css'][Version('1.10.3')] = 'baseframe/css/jquery-ui.css'

assets['jquery.liblink.js'][Version('0.0.0')] = ('jquery.js', 'baseframe/js/jquery.liblink.js')
assets['jquery.wnumb.js'][Version('0.0.0')] = ('jquery.js', 'baseframe/js/jquery.wnumb.js')
assets['jquery.range-slider.js'][Version('5.3.0')] = ('jquery.js', 'jquery.ui.js', 'baseframe/js/jQRangeSlider-min.js')
assets['jquery.range-slider.css'][Version('5.3.0')] = ('jquery.ui.css', 'baseframe/css/jQRangeSlider.css')
assets['jquery.nouislider.js'][Version('7.0.10')] = ('jquery.js', 'baseframe/js/jquery.nouislider.min.js')
assets['jquery.nouislider.css'][Version('7.0.10')] = ('baseframe/css/jquery.nouislider.min.css')

# textarea-expander is deprecated. Use autosize instead
assets['jquery.textarea-expander.js'][Version('1.0.0')] = ('jquery.js', 'baseframe/js/jquery.textarea-expander.js')
assets['jquery.autosize.js'][Version('1.18.17')] = ('jquery.js', 'baseframe/js/jquery.autosize.js')

assets['jquery.oembed.js'][Version('1.0.1')] = ('jquery.js', 'baseframe/js/jquery.oembed.js')
assets['jquery.oembed.css'][Version('1.0.1')] = ('baseframe/css/jquery.oembed.css')

assets['jquery.timepicker.js'][Version('1.6.0')] = ('jquery.js>=1.7.0', 'baseframe/js/jquery.timepicker.js')
assets['jquery.timepicker.css'][Version('1.6.0')] = 'baseframe/css/jquery.timepicker.css'

assets['jquery.fullcalendar.js'][Version('1.6.4')] = ('jquery.js', 'jquery.ui.js', 'baseframe/js/fullcalendar/fullcalendar.js')
assets['jquery.fullcalendar.css'][Version('1.6.4')] = ('jquery.ui.css', 'baseframe/js/fullcalendar/fullcalendar.css')
assets['jquery.fullcalendar.gcal.js'][Version('1.6.4')] = ('jquery.fullcalendar.js', 'baseframe/js/fullcalendar/gcal.js')

assets['jquery.locationpicker.js'][Version('0.1.12')] = ('jquery.js', 'baseframe/js/jquery.locationpicker.js')
assets['jquery.appear.js'][Version('0.3.3')] = ('jquery.js', 'baseframe/js/jquery.appear.js')

assets['select2.js'][Version('3.3.2')] = ('jquery.js>=1.4.6', 'baseframe/js/select2.js')
assets['select2.css'][Version('3.3.2')] = 'baseframe/css/select2.css'

assets['bootstrap-multiselect.css'][Version('0.9.13')] = 'baseframe/css/bootstrap-multiselect.css'
assets['bootstrap-multiselect.js'][Version('0.9.13')] = 'baseframe/js/bootstrap-multiselect.js'

assets['codemirror.js'][Version('4.11.0')] = 'baseframe/js/codemirror/lib/codemirror.js'
assets['codemirror.css'][Version('4.11.0')] = 'baseframe/js/codemirror/lib/codemirror.css'

assets['codemirror.mode.markdown.js'][Version('4.11.0')] = 'baseframe/js/codemirror/mode/markdown/markdown.js'
assets['codemirror.mode.gfm.js'][Version('4.11.0')] = 'baseframe/js/codemirror/mode/gfm/gfm.js'
assets['codemirror.mode.htmlmixed.js'][Version('4.11.0')] = 'baseframe/js/codemirror/mode/htmlmixed/htmlmixed.js'
assets['codemirror.mode.css.js'][Version('4.11.0')] = 'baseframe/js/codemirror/mode/css/css.js'
assets['codemirror.addon.mode.overlay.js'][Version('4.11.0')] = 'baseframe/js/codemirror/addon/mode/overlay.js'
assets['codemirror.addon.edit.continuelist.js'][Version('4.11.0')] = 'baseframe/js/codemirror/addon/edit/continuelist.js'
assets['codemirror.addon.edit.closebrackets.js'][Version('4.11.0')] = 'baseframe/js/codemirror/addon/edit/closebrackets.js'
assets['codemirror.addon.edit.matchbrackets.js'][Version('4.11.0')] = 'baseframe/js/codemirror/addon/edit/matchbrackets.js'
assets['codemirror.addon.hint.css-hint.js'][Version('4.11.0')] = 'baseframe/js/codemirror/addon/hint/css-hint.js'
assets['codemirror.addon.lint.css-lint.js'][Version('4.11.0')] = 'baseframe/js/codemirror/addon/lint/css-lint.js'

assets['codemirror-markdown.js'][Version('4.11.0')] = {'requires': [
    'codemirror.js==4.11.0',
    'codemirror.mode.markdown.js==4.11.0',
    'codemirror.mode.gfm.js==4.11.0',
    'codemirror.mode.htmlmixed.js==4.11.0',
    'codemirror.addon.mode.overlay.js==4.11.0',
    'codemirror.addon.edit.continuelist.js==4.11.0',
    'codemirror.addon.edit.closebrackets.js==4.11.0',
]}
assets['codemirror-markdown.css'][Version('4.11.0')] = ('codemirror.css==4.11.0', 'baseframe/css/codemirror.css')
assets['codemirror-css.js'][Version('4.11.0')] = {'requires': [
    'codemirror.js==4.11.0',
    'codemirror.mode.css.js==4.11.0',
    'codemirror.addon.hint.css-hint.js==4.11.0',
    'codemirror.addon.lint.css-lint.js==4.11.0',
    'codemirror.addon.edit.closebrackets.js==4.11.0',
]}

assets['pygments-default.css'][Version('1.5.0')] = 'baseframe/css/pygments-default.css'
assets['pygments-zenburn.css'][Version('1.5.0')] = 'baseframe/css/pygments-zenburn.css'
assets['pygments.css'][Version('1.5.0')] = {'requires': 'pygments-default.css'}

assets['mousetrap.js'][Version('1.1.2')] = 'baseframe/js/mousetrap.js'
assets['toastr.js'][Version('1.2.2')] = 'baseframe/js/toastr.js'
assets['toastr.css'][Version('1.2.2')] = 'baseframe/css/toastr.css'

assets['jquery.expander.js'][Version('1.4.5')] = ('jquery.js', 'baseframe/js/jquery.expander.js')
assets['jquery.cookie.js'][Version('1.3.0')] = ('jquery.js', 'baseframe/js/jquery.cookie.js')
assets['jquery.sparkline.js'][Version('2.1.2')] = ('jquery.js', 'baseframe/js/jquery.sparkline.js')
assets['timezone.js'][Version('0.0.0')] = 'baseframe/js/detect_timezone.js'
assets['socialite.js'][Version('2.0.0')] = 'baseframe/js/socialite.js'
assets['swfobject.js'][Version('2.2.0')] = 'baseframe/js/swfobject.js'
assets['parsley.js'][Version('2.0.7')] = ('jquery.js', 'baseframe/js/parsley.js')
assets['parsley.remote.js'][Version('2.0.7')] = {
    'provides': 'parsley.js',
    'bundle': 'baseframe/js/parsley.remote.js',
    }
assets['fingerprint2.js'][Version('1.1.4')] = 'baseframe/js/fingerprint2.js'

# FooTable
assets['footable.js'][Version('2.0.3')] = ('jquery.js', 'baseframe/js/footable.js')
assets['footable-paginate.js'][Version('2.0.3')] = ('jquery.js', 'footable.js', 'baseframe/js/footable-paginate.js')
assets['footable-filter.js'][Version('2.0.3')] = ('jquery.js', 'footable.js', 'baseframe/js/footable-filter.js')
assets['footable-sort.js'][Version('2.0.3')] = ('jquery.js', 'footable.js', 'baseframe/js/footable-sort.js')
assets['baseframe-footable.js'][Version('2.0.3')] = {
    'requires': ['footable.js', 'footable-filter.js', 'footable-sort.js']
    }
assets['baseframe-footable.css'][Version('2.0.3')] = {
    'provides': 'footable.css',
    'requires': 'fontawesome.css>=4.4.0',
    'bundle': 'baseframe/css/baseframe-footable.css',
    }

# NProgress
assets['nprogress.js'][Version('0.2.0')] = 'baseframe/js/nprogress.js'
assets['nprogress.css'][Version('0.2.0')] = 'baseframe/css/nprogress.css'

# Ractive
assets['ractive.js'][Version('0.7.3')] = 'baseframe/js/ractive.js'

# Ractive fly transition
assets['ractive-transitions-fly.js'][Version('0.3.0')] = 'baseframe/js/ractive-transitions-fly.js'

# Validate
assets['validate.js'][Version('2.0.1')] = 'baseframe/js/validate.js'

# Hammer
assets['hammer.js'][Version('2.0.6')] = 'baseframe/js/hammer.min.js'

assets['animate.css'][Version('0.0.0')] = 'baseframe/css/animate.css'

assets['matchmedia.js'][Version('0.0.0')] = 'baseframe/js/matchmedia.js'
assets['picturefill.js'][Version('0.1.0')] = ('matchmedia.js', 'baseframe/js/picturefill.js')

assets['dropzone.js'][Version('3.2.0')] = 'baseframe/js/dropzone.js'
assets['dropzone.css'][Version('3.2.0')] = 'baseframe/css/dropzone.css'

assets['mustache-hogan.js'][Version('2.0.0')] = 'baseframe/js/mustache-hogan/hogan-2.0.0.min.mustache.js'
assets['mustache-loader.js'][Version('0.5.1')] = 'baseframe/js/mustache-hogan/mustache-loader.js'

assets['marked.js'][Version('0.3.0')] = 'baseframe/js/marked.js'

# Font Awesome
assets['fontawesome.css'][Version('3.1.0')] = 'baseframe/css/fontawesome-3.1.css'
assets['fontawesome.css'][Version('4.4.0')] = 'baseframe/css/fontawesome-4.4.css'

# Social icons
assets['rrssb.js'][Version('1.8.5')] = 'baseframe/js/rrssb.js'
assets['rrssb.css'][Version('1.8.5')] = 'baseframe/css/rrssb.css'

# Fira Sans and Fira Mono
assets['firasans-regular.css'][Version('1.0.0')] = 'baseframe/css/fira/firasans-regular.css'
assets['firasans-regularitalic.css'][Version('1.0.0')] = 'baseframe/css/fira/firasans-regularitalic.css'
assets['firasans-light.css'][Version('1.0.0')] = 'baseframe/css/fira/firasans-light.css'
assets['firasans-lightitalic.css'][Version('1.0.0')] = 'baseframe/css/fira/firasans-lightitalic.css'
assets['firasans-medium.css'][Version('1.0.0')] = 'baseframe/css/fira/firasans-medium.css'
assets['firasans-mediumitalic.css'][Version('1.0.0')] = 'baseframe/css/fira/firasans-mediumitalic.css'
assets['firasans-bold.css'][Version('1.0.0')] = 'baseframe/css/fira/firasans-bold.css'
assets['firasans-bolditalic.css'][Version('1.0.0')] = 'baseframe/css/fira/firasans-bolditalic.css'
assets['firamono-regular.css'][Version('1.0.0')] = 'baseframe/css/fira/firamono-regular.css'
assets['firamono-bold.css'][Version('1.0.0')] = 'baseframe/css/fira/firamono-bold.css'

assets['firasans.css'][Version('1.0.0')] = {'requires': [
    'firasans-regular.css==1.0.0',
    'firasans-regularitalic.css==1.0.0',
    'firasans-bold.css==1.0.0',
    'firasans-bolditalic.css==1.0.0'
    ]}

assets['firamono.css'][Version('1.0.0')] = {'requires': [
    'firamono-regular.css==1.0.0',
    'firamono-bold.css==1.0.0'
    ]}


assets['firasans-regular.css'][Version('4.2.0')] = 'baseframe/fonts/fira-4/firasans-regular.css'
assets['firasans-regular-italic.css'][Version('4.2.0')] = 'baseframe/fonts/fira-4/firasans-regular-italic.css'
assets['firasans-bold.css'][Version('4.2.0')] = 'baseframe/fonts/fira-4/firasans-bold.css'
assets['firasans-bold-italic.css'][Version('4.2.0')] = 'baseframe/fonts/fira-4/firasans-bold-italic.css'

assets['firasans.css'][Version('4.2.0')] = {'requires': [
    'firasans-regular.css==4.2.0',
    'firasans-regular-italic.css==4.2.0',
    'firasans-bold.css==4.2.0',
    'firasans-bold-italic.css==4.2.0'
    ]}


assets['firamono-regular.css'][Version('4.2.0')] = 'baseframe/fonts/fira/firamono-regular.css'
assets['firamono-bold.css'][Version('4.2.0')] = 'baseframe/fonts/fira/firamono-bold.css'

assets['firamono.css'][Version('4.2.0')] = {'requires': [
    'firamono-regular.css==4.2.0',
    'firamono-bold.css==4.2.0'
    ]}


assets['baseframe-firasans.css'][Version('1.0.0')] = 'baseframe/css/baseframe-firasans.css'

# Asset packages
assets['bootstrap.js'][Version('2.0.1')] = {'requires': [
    'bootstrap-alert.js==2.0.1',
    'bootstrap-button.js==2.0.1',
    # 'bootstrap-carousel.js==2.0.1',
    # 'bootstrap-collapse.js==2.0.1',
    'bootstrap-dropdown.js==2.0.1',
    'bootstrap-modal.js==2.0.1',
    'bootstrap-tooltip.js==2.0.1',
    # 'bootstrap-popover.js==2.0.1',
    # 'bootstrap-scrollspy.js==2.0.1',
    'bootstrap-tab.js==2.0.1',
    'bootstrap-transition.js==2.0.1',
    # 'bootstrap-typeahead.js==2.0.1',
]}

assets['bootstrap.js'][Version('3.3.1')] = {'requires': [
    'bootstrap-transition.js==3.3.1',
    'bootstrap-alert.js==3.3.1',
    'bootstrap-button.js==3.3.1',
    'bootstrap-carousel.js==3.3.1',
    'bootstrap-collapse.js==3.3.1',
    'bootstrap-dropdown.js==3.3.1',
    'bootstrap-modal.js==3.3.1',
    'bootstrap-tooltip.js==3.3.1',
    'bootstrap-popover.js==3.3.1',
    'bootstrap-scrollspy.js==3.3.1',
    'bootstrap-tab.js==3.3.1',
    'bootstrap-affix.js==3.3.1',
]}

assets['bootstrap3-editable.js'][Version('1.5.1')] = ('bootstrap.js>=3.0.0',
    'baseframe/js/bootstrap3-editable/js/bootstrap-editable.js')
assets['bootstrap3-editable.css'][Version('1.5.1')] = ('bootstrap.css>=3.0.0',
    'baseframe/js/bootstrap3-editable/css/bootstrap-editable.css')

assets['mustache.js'][Version('2.0.0')] = {'requires': [
    'mustache-loader.js==0.5.1',
    'mustache-hogan.js==2.0.0',
]}

assets['extra.js'][Version('0.0.0')] = {'requires': [
    'jquery.form.js',
    # 'bootstrap-datepicker.js',
    'jquery.timepicker.js',
    'select2.js',
]}

assets['baseframe.js'][Version(__version__)] = {'requires': [
    'jquery.js<1.9.0',
    'bootstrap.js==2.0.1',
    'extra.js',
    'jquery.tinymce.js>=3.0.0,<4.0.0',
    'baseframe-base.js==' + __version__,
    'baseframe-networkbar.js==' + __version__,
]}

assets['baseframe.css'][Version(__version__)] = {'requires': [
    'bootstrap.css==2.0.1',
    'bootstrap-responsive.css==2.0.1',
    'select2.css',
    'jquery.timepicker.css',
    'fontawesome.css==3.1.0',
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
    'baseframe-base-bs3.css==' + __version__,
    'baseframe-networkbar.css==' + __version__,
]}
