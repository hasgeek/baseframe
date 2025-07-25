"""Static assets (deprecated)."""

from coaster.assets import Version, VersionedAssets

from ._version import __version__

__all__ = ['Version', 'assets']

#: Semantic-versioned assets
assets = VersionedAssets()

assets['baseframe-networkbar.js'][Version(__version__)] = 'baseframe/js/networkbar.js'
assets['baseframe-networkbar.css'][Version(__version__)] = (
    'baseframe/css/networkbar.css'
)
assets['baseframe-base.js'][Version(__version__)] = (
    'baseframe/js/baseframe-bootstrap.js'
)
assets['baseframe-base.css'][Version(__version__)] = 'baseframe/css/baseframe.css'
assets['baseframe-base-bs3.css'][Version(__version__)] = (
    'baseframe/css/baseframe-bs3.css'
)

# Bootstrap 3.3.1
assets['bootstrap.css'][Version('3.3.1')] = 'baseframe/css/bootstrap3/bootstrap.css'
assets['bootstrap-affix.js'][Version('3.3.1')] = 'baseframe/js/bootstrap3/affix.js'
assets['bootstrap-alert.js'][Version('3.3.1')] = 'baseframe/js/bootstrap3/alert.js'
assets['bootstrap-button.js'][Version('3.3.1')] = 'baseframe/js/bootstrap3/button.js'
assets['bootstrap-carousel.js'][Version('3.3.1')] = (
    'baseframe/js/bootstrap3/carousel.js',
)
assets['bootstrap-collapse.js'][Version('3.3.1')] = (
    'baseframe/js/bootstrap3/collapse.js',
)
assets['bootstrap-dropdown.js'][Version('3.3.1')] = (
    'baseframe/js/bootstrap3/dropdown.js',
)
assets['bootstrap-modal.js'][Version('3.3.1')] = 'baseframe/js/bootstrap3/modal.js'
assets['bootstrap-popover.js'][Version('3.3.1')] = (
    'baseframe/js/bootstrap3/popover.js',
)
assets['bootstrap-scrollspy.js'][Version('3.3.1')] = (
    'baseframe/js/bootstrap3/scrollspy.js',
)
assets['bootstrap-tab.js'][Version('3.3.1')] = 'baseframe/js/bootstrap3/tab.js'
assets['bootstrap-tooltip.js'][Version('3.3.1')] = (
    'baseframe/js/bootstrap3/tooltip.js',
)
assets['bootstrap-transition.js'][Version('3.3.1')] = (
    'baseframe/js/bootstrap3/transition.js',
)

# Bootstrap Social - commit #918fc55c3c938377a7618ec0f115846e50d4b883
assets['bootstrap-social.css'][Version('1.0.0')] = (
    'bootstrap.css>=3.0.0',
    'baseframe/css/bootstrap-social.css',
)

assets['jquery.form.js'][Version('2.96.0')] = 'baseframe/js/jquery.form.js'
assets['jquery.tinymce.js'][Version('4.1.7')] = (
    'baseframe/js/tinymce4/jquery.tinymce.min.js',
)
assets['tinymce.js'][Version('4.1.7')] = 'baseframe/js/tinymce4/tinymce.min.js'
assets['bootstrap-datepicker.js'][Version('1.3.0')] = (
    'baseframe/js/bootstrap-datepicker.js',
)

assets['jquery.ui.js'][Version('1.10.3')] = 'baseframe/js/jquery-ui.js'
assets['jquery.ui.css'][Version('1.10.3')] = 'baseframe/css/jquery-ui.css'
assets['jquery.ui.js'][Version('1.12.1')] = 'baseframe/js/jquery-ui-1.12.1.js'
assets['jquery.ui.css'][Version('1.12.1')] = 'baseframe/css/jquery-ui-1.12.1.css'
assets['jquery.ui.sortable.js'][Version('1.12.1')] = (
    'baseframe/js/jquery-ui-sortable-1.12.1.js',
)
assets['jquery.ui.sortable.css'][Version('1.12.1')] = (
    'baseframe/css/jquery-ui-sortable-1.12.1.css'
)
assets['jquery.ui.touch-punch.js'][Version('0.2.3')] = (
    'baseframe/js/jquery.ui.touch-punch.js',
)
assets['jquery.ui.sortable.touch.js'][Version('1.12.1')] = {
    'requires': ['jquery.ui.sortable.js==1.12.1', 'jquery.ui.touch-punch.js==0.2.3']
}
assets['jquery.ui.sortable.touch.css'][Version('1.12.1')] = {
    'requires': ['jquery.ui.sortable.css==1.12.1']
}

assets['jquery.liblink.js'][Version('0.0.0')] = 'baseframe/js/jquery.liblink.js'
assets['jquery.wnumb.js'][Version('0.0.0')] = 'baseframe/js/jquery.wnumb.js'
assets['jquery.range-slider.js'][Version('5.3.0')] = (
    'jquery.ui.js',
    'baseframe/js/jQRangeSlider-min.js',
)
assets['jquery.range-slider.css'][Version('5.3.0')] = (
    'jquery.ui.css',
    'baseframe/css/jQRangeSlider.css',
)
assets['jquery.nouislider.js'][Version('7.0.10')] = (
    'baseframe/js/jquery.nouislider.min.js',
)
assets['jquery.nouislider.css'][Version('7.0.10')] = (
    'baseframe/css/jquery.nouislider.min.css'
)

# textarea-expander is deprecated. Use autosize instead
assets['jquery.textarea-expander.js'][Version('1.0.0')] = (
    'baseframe/js/jquery.textarea-expander.js',
)
assets['jquery.autosize.js'][Version('1.18.17')] = 'baseframe/js/jquery.autosize.js'

assets['jquery.oembed.js'][Version('1.0.1')] = 'baseframe/js/jquery.oembed.js'
assets['jquery.oembed.css'][Version('1.0.1')] = 'baseframe/css/jquery.oembed.css'

assets['jquery.fullcalendar.js'][Version('1.6.4')] = (
    'jquery.ui.js',
    'baseframe/js/fullcalendar/fullcalendar.js',
)
assets['jquery.fullcalendar.css'][Version('1.6.4')] = (
    'jquery.ui.css',
    'baseframe/js/fullcalendar/fullcalendar.css',
)
assets['jquery.fullcalendar.gcal.js'][Version('1.6.4')] = (
    'jquery.fullcalendar.js',
    'baseframe/js/fullcalendar/gcal.js',
)

assets['jquery.locationpicker.js'][Version('0.1.12')] = (
    'baseframe/js/jquery.locationpicker.js',
)
assets['jquery.appear.js'][Version('0.3.3')] = 'baseframe/js/jquery.appear.js'

assets['jquery-modal.js'][Version('0.8.2')] = 'baseframe/js/jquery-modal.js'
assets['jquery-modal.css'][Version('0.8.2')] = 'baseframe/css/jquery-modal.css'

assets['jquery-easytabs.js'][Version('3.2.0')] = 'baseframe/js/jquery-easytabs.js'

# jQuery plugin for truncating multiple lines of text
assets['jquery.succinct.js'][Version('1.1.0')] = 'baseframe/js/jquery.succinct.js'
assets['jquery.truncate8.js'][Version('1.3.3')] = 'baseframe/js/jquery.truncate8.js'

assets['jquery_jeditable.js'][Version('2.0.14')] = 'baseframe/js/jquery_jeditable.js'

# jQuery emoji picker
assets['emojionearea.css'][Version('3.4.1')] = 'baseframe/css/emojionearea.css'
assets['emojionearea-material.css'][Version('3.4.1')] = (
    'emojionearea.css',
    'baseframe/css/emojionearea-material.css',
)
assets['emojionearea.js'][Version('3.4.1')] = 'baseframe/js/emojionearea.js'
assets['emojionearea-material.js'][Version('3.4.1')] = {
    'requires': ['emojionearea.js==3.4.1']
}

assets['select2.js'][Version('4.0.3')] = 'baseframe/js/select2.js'
assets['select2.css'][Version('4.0.3')] = 'baseframe/css/select2.css'
assets['select2-bootstrap.css'][Version('0.1.0')] = (
    'select2.css',
    'baseframe/css/bootstrap-select2.css',
)
assets['select2-baseframe.css'][Version('4.0.3')] = (
    'select2-bootstrap.css',
    'baseframe/css/select2-baseframe.css',
)
assets['select2-baseframe.js'][Version('4.0.3')] = {'requires': ['select2.js==4.0.3']}
assets['select2-material.css'][Version('4.0.3')] = (
    'select2.css',
    'baseframe/css/select2-baseframe-material.css',
)
assets['select2-material.js'][Version('4.0.3')] = {'requires': ['select2.js==4.0.3']}


assets['bootstrap-multiselect.css'][Version('0.9.13')] = (
    'baseframe/css/bootstrap-multiselect.css'
)
assets['bootstrap-multiselect.js'][Version('0.9.13')] = (
    'baseframe/js/bootstrap-multiselect.js'
)

assets['codemirror.js'][Version('4.11.0')] = 'baseframe/js/codemirror/lib/codemirror.js'
assets['codemirror.css'][Version('4.11.0')] = (
    'baseframe/js/codemirror/lib/codemirror.css'
)

assets['codemirror.mode.markdown.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/mode/markdown/markdown.js'
)
assets['codemirror.mode.gfm.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/mode/gfm/gfm.js'
)
assets['codemirror.mode.htmlmixed.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/mode/htmlmixed/htmlmixed.js'
)
assets['codemirror.mode.css.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/mode/css/css.js'
)
assets['codemirror.mode.javascript.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/mode/javascript/javascript.js'
)
assets['codemirror.addon.display.fullscreen.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/addon/display/fullscreen.js'
)
assets['codemirror.addon.display.fullscreen.css'][Version('4.11.0')] = (
    'baseframe/js/codemirror/addon/display/fullscreen.css'
)
assets['codemirror.addon.display.rulers.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/addon/display/rulers.js'
)
assets['codemirror.addon.mode.overlay.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/addon/mode/overlay.js'
)
assets['codemirror.addon.edit.continuelist.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/addon/edit/continuelist.js'
)
assets['codemirror.addon.edit.closebrackets.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/addon/edit/closebrackets.js'
)
assets['codemirror.addon.edit.matchbrackets.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/addon/edit/matchbrackets.js'
)
assets['codemirror.addon.hint.show-hint.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/addon/hint/show-hint.js'
)
assets['codemirror.addon.hint.show-hint.css'][Version('4.11.0')] = (
    'baseframe/js/codemirror/addon/hint/show-hint.css'
)
assets['codemirror.addon.hint.css-hint.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/addon/hint/css-hint.js'
)
assets['codemirror.addon.hint.javascript-hint.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/addon/hint/javascript-hint.js'
)
assets['codemirror.addon.lint.css-lint.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/addon/lint/css-lint.js'
)
assets['codemirror.addon.lint.json-lint.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/addon/lint/json-lint.js'
)
assets['codemirror.addon.fold.brace-fold.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/addon/fold/brace-fold.js'
)
assets['codemirror.addon.fold.foldcode.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/addon/fold/foldcode.js'
)
assets['codemirror.addon.fold.foldgutter.js'][Version('4.11.0')] = (
    'baseframe/js/codemirror/addon/fold/foldgutter.js'
)
assets['codemirror.addon.fold.foldgutter.css'][Version('4.11.0')] = (
    'baseframe/js/codemirror/addon/fold/foldgutter.css'
)

assets['codemirror-markdown.js'][Version('4.11.0')] = {
    'requires': [
        'codemirror.js==4.11.0',
        'codemirror.mode.markdown.js==4.11.0',
        'codemirror.mode.gfm.js==4.11.0',
        'codemirror.mode.htmlmixed.js==4.11.0',
        'codemirror.addon.mode.overlay.js==4.11.0',
        'codemirror.addon.edit.continuelist.js==4.11.0',
        'codemirror.addon.edit.closebrackets.js==4.11.0',
    ]
}
assets['codemirror-markdown.css'][Version('4.11.0')] = (
    'codemirror.css==4.11.0',
    'baseframe/css/codemirror.css',
)
assets['codemirror-css.js'][Version('4.11.0')] = {
    'requires': [
        'codemirror.js==4.11.0',
        'codemirror.mode.css.js==4.11.0',
        'codemirror.addon.hint.show-hint.js==4.11.0',
        'codemirror.addon.hint.css-hint.js==4.11.0',
        'codemirror.addon.lint.css-lint.js==4.11.0',
        'codemirror.addon.edit.matchbrackets.js==4.11.0',
        'codemirror.addon.edit.closebrackets.js==4.11.0',
    ]
}
assets['codemirror-css.css'][Version('4.11.0')] = {
    'requires': [
        'codemirror.css==4.11.0',
        'codemirror.addon.hint.show-hint.css==4.11.0',
    ]
}
assets['codemirror-json.js'][Version('4.11.0')] = {
    'requires': [
        'codemirror.js==4.11.0',
        'codemirror.mode.javascript.js==4.11.0',
        'codemirror.addon.display.rulers.js==4.11.0',
        'codemirror.addon.display.fullscreen.js==4.11.0',
        'codemirror.addon.hint.show-hint.js==4.11.0',
        'codemirror.addon.hint.javascript-hint.js==4.11.0',
        'codemirror.addon.lint.json-lint.js==4.11.0',
        'codemirror.addon.fold.foldcode.js==4.11.0',
        'codemirror.addon.fold.foldgutter.js==4.11.0',
        'codemirror.addon.fold.brace-fold.js==4.11.0',
        'codemirror.addon.edit.matchbrackets.js==4.11.0',
        'codemirror.addon.edit.closebrackets.js==4.11.0',
    ]
}
assets['codemirror-json.css'][Version('4.11.0')] = {
    'requires': [
        'codemirror.css==4.11.0',
        'codemirror.addon.fold.foldgutter.css==4.11.0',
        'codemirror.addon.display.fullscreen.css==4.11.0',
        'codemirror.addon.hint.show-hint.css==4.11.0',
    ]
}

assets['codemirror.js'][Version('5.53.2')] = (
    'baseframe/js/codemirror-5.53.2/codemirror.min.js'
)
assets['codemirror.css'][Version('5.53.2')] = (
    'baseframe/css/codemirror-5.53.2/codemirror-basic.css'
)

assets['codemirror.mode.markdown.js'][Version('5.53.2')] = (
    'baseframe/js/codemirror-5.53.2/mode/markdown/markdown.min.js'
)
assets['codemirror.mode.gfm.js'][Version('5.53.2')] = (
    'baseframe/js/codemirror-5.53.2/mode/gfm/gfm.min.js'
)
assets['codemirror.mode.htmlmixed.js'][Version('5.53.2')] = (
    'baseframe/js/codemirror-5.53.2/mode/htmlmixed/htmlmixed.min.js'
)
assets['codemirror.mode.css.js'][Version('5.53.2')] = (
    'baseframe/js/codemirror-5.53.2/mode/css/css.min.js'
)
assets['codemirror.addon.mode.overlay.js'][Version('5.53.2')] = (
    'baseframe/js/codemirror-5.53.2/addon/mode/overlay.min.js'
)
assets['codemirror.addon.edit.continuelist.js'][Version('5.53.2')] = (
    'baseframe/js/codemirror-5.53.2/addon/edit/continuelist.min.js'
)
assets['codemirror.addon.edit.closebrackets.js'][Version('5.53.2')] = (
    'baseframe/js/codemirror-5.53.2/addon/edit/closebrackets.min.js'
)
assets['codemirror.addon.edit.matchbrackets.js'][Version('5.53.2')] = (
    'baseframe/js/codemirror-5.53.2/addon/edit/matchbrackets.min.js'
)
assets['codemirror.addon.hint.css-hint.js'][Version('5.53.2')] = (
    'baseframe/js/codemirror-5.53.2/addon/hint/css-hint.min.js'
)
assets['codemirror.addon.lint.css-lint.js'][Version('5.53.2')] = (
    'baseframe/js/codemirror-5.53.2/addon/lint/css-lint.min.js'
)
assets['codemirror.addon.display.placeholder.js'][Version('5.53.2')] = (
    'baseframe/js/codemirror-5.53.2/addon/display/placeholder.js'
)

assets['codemirror-markdown.js'][Version('5.53.2')] = {
    'requires': [
        'codemirror.js==5.53.2',
        'codemirror.mode.markdown.js==5.53.2',
        'codemirror.mode.gfm.js==5.53.2',
        'codemirror.mode.htmlmixed.js==5.53.2',
        'codemirror.addon.mode.overlay.js==5.53.2',
        'codemirror.addon.edit.continuelist.js==5.53.2',
        'codemirror.addon.edit.closebrackets.js==5.53.2',
        'codemirror.addon.display.placeholder.js==5.53.2',
    ]
}
assets['codemirror-markdown.css'][Version('5.53.2')] = (
    'codemirror.css==5.53.2',
    'baseframe/css/codemirror.css',
)
assets['codemirror-markdown-material.css'][Version('5.53.2')] = (
    'codemirror.css==5.53.2',
    'baseframe/css/codemirror-material.css',
)
assets['codemirror-css.js'][Version('5.53.2')] = {
    'requires': [
        'codemirror.js==5.53.2',
        'codemirror.mode.css.js==5.53.2',
        'codemirror.addon.hint.css-hint.js==5.53.2',
        'codemirror.addon.lint.css-lint.js==5.53.2',
        'codemirror.addon.edit.closebrackets.js==5.53.2',
    ]
}
assets['codemirror-css.css'][Version('5.53.2')] = {
    'requires': [
        'codemirror.css==5.53.2',
    ]
}


assets['pygments-default.css'][Version('1.5.0')] = 'baseframe/css/pygments-default.css'
assets['pygments-zenburn.css'][Version('1.5.0')] = 'baseframe/css/pygments-zenburn.css'
assets['pygments.css'][Version('1.5.0')] = {'requires': 'pygments-default.css'}

assets['mousetrap.js'][Version('1.1.2')] = 'baseframe/js/mousetrap.js'
assets['toastr.js'][Version('1.2.2')] = 'baseframe/js/toastr.js'
assets['toastr.css'][Version('1.2.2')] = 'baseframe/css/toastr.css'

assets['jquery.expander.js'][Version('1.4.5')] = 'baseframe/js/jquery.expander.js'
assets['jquery.cookie.js'][Version('1.3.0')] = 'baseframe/js/jquery.cookie.js'
assets['jquery.sparkline.js'][Version('2.1.2')] = 'baseframe/js/jquery.sparkline.js'
assets['timezone.js'][Version('0.0.0')] = 'baseframe/js/detect_timezone.js'
assets['socialite.js'][Version('2.0.0')] = 'baseframe/js/socialite.js'
assets['swfobject.js'][Version('2.2.0')] = 'baseframe/js/swfobject.js'
assets['parsley.js'][Version('2.0.7')] = 'baseframe/js/parsley.js'
assets['parsley.remote.js'][Version('2.0.7')] = {
    'provides': 'parsley.js',
    'bundle': 'baseframe/js/parsley.remote.js',
}
assets['fingerprint2.js'][Version('1.1.4')] = 'baseframe/js/fingerprint2.js'

# FooTable
assets['footable.js'][Version('2.0.3')] = 'baseframe/js/footable.js'
assets['footable-paginate.js'][Version('2.0.3')] = (
    'footable.js',
    'baseframe/js/footable-paginate.js',
)
assets['footable-filter.js'][Version('2.0.3')] = (
    'footable.js',
    'baseframe/js/footable-filter.js',
)
assets['footable-sort.js'][Version('2.0.3')] = (
    'footable.js',
    'baseframe/js/footable-sort.js',
)
assets['baseframe-footable.js'][Version('2.0.3')] = {
    'requires': ['footable.js', 'footable-filter.js', 'footable-sort.js']
}
assets['baseframe-footable.css'][Version('2.0.3')] = {
    'provides': 'footable.css',
    'requires': 'fontawesome.css>=4.4.0',
    'bundle': 'baseframe/css/baseframe-footable.css',
}
assets['baseframe-footable-mui.css'][Version('2.0.3')] = {
    'provides': 'footable-mui.css',
    'requires': 'baseframe-footable.css=2.0.3',
    'bundle': 'baseframe/css/footable-mui.css',
}


# NProgress
assets['nprogress.js'][Version('0.2.0')] = 'baseframe/js/nprogress.js'
assets['nprogress.css'][Version('0.2.0')] = 'baseframe/css/nprogress.css'

# Ractive
assets['ractive.js'][Version('0.7.3')] = 'baseframe/js/ractive.js'

# Ractive fly transition
assets['ractive-transitions-fly.js'][Version('0.3.0')] = (
    'baseframe/js/ractive-transitions-fly.js'
)

# Validate
assets['validate.js'][Version('2.0.1')] = 'baseframe/js/validate.js'

# Hammer
assets['hammer.js'][Version('2.0.6')] = 'baseframe/js/hammer.min.js'

assets['matchmedia.js'][Version('0.0.0')] = 'baseframe/js/matchmedia.js'
assets['picturefill.js'][Version('0.1.0')] = (
    'matchmedia.js',
    'baseframe/js/picturefill.js',
)

assets['dropzone.js'][Version('3.2.0')] = 'baseframe/js/dropzone.js'
assets['dropzone.css'][Version('3.2.0')] = 'baseframe/css/dropzone.css'
assets['dropzone.js'][Version('5.5.0')] = 'baseframe/js/dropzone-5.5.0.js'
assets['dropzone.css'][Version('5.5.0')] = 'baseframe/css/dropzone-5.5.0.css'

assets['marked.js'][Version('0.3.0')] = 'baseframe/js/marked.js'

assets['moment.js'][Version('2.24.0')] = 'baseframe/js/moment.js'
# To use moment timezone in the browser, zone data needs to be loaded.
assets['moment-timezone-data.js'][Version('0.5.25')] = (
    'baseframe/js/moment-timezone-with-data-10-year-range.js'
)

assets['leaflet.js'][Version('1.3.4')] = 'baseframe/js/leaflet.js'
assets['leaflet.css'][Version('1.3.4')] = 'baseframe/css/leaflet.css'
assets['leaflet-search.css'][Version('2.9.7')] = 'baseframe/css/leaflet-search.css'
assets['leaflet-search.js'][Version('2.9.7')] = 'baseframe/js/leaflet-search.js'

# Font Awesome
assets['fontawesome.css'][Version('4.7.0')] = 'baseframe/css/fontawesome-4.7.css'

# Social icons
assets['rrssb.js'][Version('1.8.5')] = 'baseframe/js/rrssb.js'
assets['rrssb.css'][Version('1.8.5')] = 'baseframe/css/rrssb.css'

assets['baseframe-firasans.css'][Version('1.0.0')] = (
    'baseframe/css/baseframe-firasans.css'
)

assets['getdevicepixelratio.js'][Version('1.0.0')] = (
    'baseframe/js/getdevicepixelratio.js'
)

assets['pace.js'][Version('1.0.0')] = 'baseframe/js/pace.js'

# Asset packages
assets['bootstrap.js'][Version('3.3.1')] = {
    'requires': [
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
    ]
}

assets['bootstrap3-editable.js'][Version('1.5.1')] = (
    'bootstrap.js>=3.0.0',
    'baseframe/js/bootstrap3-editable/js/bootstrap-editable.js',
)
assets['bootstrap3-editable.css'][Version('1.5.1')] = (
    'bootstrap.css>=3.0.0',
    'baseframe/js/bootstrap3-editable/css/bootstrap-editable.css',
)

assets['extra.js'][Version('0.0.0')] = {
    'requires': [
        'jquery.form.js',
        'jquery.autosize.js',
        # 'bootstrap-datepicker.js',
        'select2-baseframe.js',
        'getdevicepixelratio.js',
    ]
}
assets['extra-material.js'][Version('0.0.0')] = {
    'requires': [
        'jquery-modal.js',
        'jquery.form.js',
        'select2-material.js',
        'getdevicepixelratio.js',
    ]
}

assets['baseframe-bs3.js'][Version(__version__)] = {
    'requires': [
        'bootstrap.js>=3.0.0',
        'extra.js',
        'baseframe-base.js==' + __version__,
        'baseframe-networkbar.js==' + __version__,
    ]
}

assets['baseframe-bs3.css'][Version(__version__)] = {
    'requires': [
        'bootstrap.css>=3.0.0',
        'select2-baseframe.css',
        'baseframe-base-bs3.css==' + __version__,
        'baseframe-networkbar.css==' + __version__,
    ]
}

assets['mui.js'][Version('0.9.21')] = 'baseframe/js/mui.js'
assets['baseframe-material.js'][Version('0.9.21')] = (
    'baseframe/js/baseframe-material.js'
)
assets['baseframe-mui.js'][Version(__version__)] = {
    'requires': [
        'extra-material.js',
        'mui.js',
        'baseframe-material.js',
    ]
}

assets['mui.css'][Version('0.9.21')] = 'baseframe/css/mui.css'
assets['baseframe-mui.css'][Version(__version__)] = {
    'requires': ['jquery-modal.css', 'select2-material.css', 'mui.css']
}

assets['font-awesome5-sprite.svg'][Version('5.10.2')] = (
    'baseframe/img/font-awesome5-sprite.svg'
)
