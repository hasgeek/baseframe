Baseframe
=========

.. image:: https://secure.travis-ci.org/hasgeek/baseframe.png
   :alt: Build status

.. image:: https://coveralls.io/repos/hasgeek/baseframe/badge.png
   :target: https://coveralls.io/r/hasgeek/baseframe
   :alt: Coverage status

Reusable styles and templates for HasGeek projects. Setup instructions::

  python setup.py install

You'll need this boilerplate in your code to use it::

  from flask import Flask
  from baseframe import baseframe, assets, Version

  version = Version('0.1.0')  # Insert your app's version number here
  app = Flask(__name__, instance_relative_config=True)

  # Declare your app's assets (with .js and .css suffixes)
  # Filenames are relative to your app's static folder
  assets['myapp.js'][version] = 'js/myapp.js'
  assets['myapp.css'][version] = 'css/myapp.css'

  # Initialize baseframe with required JS/CSS assets
  # The 'baseframe' requirement is optional: it gives you the default UI
  baseframe.init_app(app, requires=['baseframe', 'myapp'])

Baseframe is BSD-licensed, but is built on top of Twitter Bootstrap 3.0
and bundles various JavaScript libraries which use BSD, MIT and Apache.
