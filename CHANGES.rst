0.3.1
-----

* AllUrlsValid now takes custom messages and an invalid_urls list
* New ValidUrl validator for a single URL (takes the same parameters)
* New StylesheetField for CSS
* New FormField for fieldsets
* New UserSelectField and UserSelectMultiField for Lastuser autocomplete
* Revamped forms.html and autoform generator
* ValidEmailDomain validator is now ValidEmail and does syntax checks
* New NoObfuscatedEmail validator looks for obfuscated emails
* New FormGenerator constructs forms from field definitions
* New CoordinatesField renders a map marker drag widget, falling back to lat/lon text fields
* Codemirror is now an external dependency installed via Makefile
* New RadioMatrixField for a table of fields and choices
* New InlineListWidget to list radio options inline
* Added ParsleyJS validation and reorganized forms to be more modular
* Added app-global CSRF protection (optional) and removed Mustache dependency
* Added ``firstline`` filter to extract first line of text from a HTML block
* ``OptionalIf`` and ``OptionalIfNot`` validators
* Added new networkbar for use in Hasjob and Funnel
* Replace ``csrf_form`` in template context with ``csrf_token``, regardless of whether
  global CSRF is enabled
* Optional support for Flask-DebugToolbar and LineProfiler extension
* SelectField now supports optgroup grouping
* Comparison validators to complement ``EqualTo`` with ``>``, ``>=``, ``<``, ``<=``, ``!=``

0.3.0
-----

* Added Bootstrap 3
* Added Mustache templating support
* Added a responsive networkbar for Bootstrap 3-based websites
* Reorganized forms into sub-modules
* Added Pygments syntax highlighting
* Removed baseframe.sqlalchemy. Use coaster.db now
* Switched default font from Open Sans to Source Sans Pro for the lower
  x-height, thereby improving the visible line height
* Fixed timezone handling in DateTimeField
* Support for external assets via the cookiefree server
* Removed local copies of Lato and Source Sans Pro fonts
* Upgraded to TinyMCE 4 and Font Awesome 4.2, with older versions stil in assets

0.2.16
------

* Mandatory cache provisioning for all apps using Flask-Cache
* i18n support via Flask-BabelEx for all apps
* Cached networkbar rendering to ensure all apps update networkbar together
* ValidEmailDomain validator for forms
* Assets: Dropzone, picturefill
* Template filters: usessl, nossl

0.2.15
------

* Template filters: age
* forms.render_delete_sqla takes a cancel_url and handles HTTP DELETE requests
* New NETWORKBAR_DATA config variable to load networkbar links
* Organizations dropdown in networkbar
* Meta Referrer header
* Font-Awesome 3.1.1
* assetenv, bundle_js and bundle_css parameters to baseframe.init_app
* select2 activation can now be disabled with "notselect" class
* New HiddenMultiSelect field in forms for customized form widgets with
  comma-separated data

0.2.14
------

* Added BSD license
* Moved static path to /_baseframe to avoid namespace clashes with /<profile>
* Many stylesheet changes; JS lib defaults
* DateTimeField is now timezone aware
* Switched from chosen.js to select2.js
* Added documentation
* Switched default font from Lato to Open Sans
* Added JS for timezone detection
* Added many optional JS assets
* Added root block to baseframe.html that can be overriden by templates
* Upgraded to FontAwesome 3.0 with many new icons
* Switched to Google Closure JS minifier for better compression than JSMin
* Semantically versioned assets, with unversioned assets moved into deprecated.py

0.2.13
------

* Incompatible API change for RichTextField to allow setting any TinyMCE option.

0.2.12
------

* Optional baseframe.sqlalchemy provides a Flask-SQLALchemy SQLAlchemy() object
  for use by blueprint-based apps

0.2.11
------

* Toastr messages can now be included via a JS include in the footer to
   prevent them from showing again on back/front navigation

0.2.10
------

* New logo and header blocks in the layout

0.2.9
-----

* Giving up on having a perfect typographic grid. It's not possible on the web
* New <span class="icon-*"> for use in menus with long lines that may wrap

0.2.8
-----

* Added optional mousetrap js for keyboard control
* Added optional toastr js for floating notifications

0.2.7
-----

* Minor style tweaks
* Modernizr build with more features
* Limit automatic tab selection to .nav-tabs-auto

0.2.6
-----

* linkify and rel=nofollow on links are now optional in RichTextField
* Many changes since 0.1. See git commit history for details
  
0.1
---

* First version
