Baseframe
=========

Reusable styles and templates for HasGeek projects. Setup instructions::

  python setup.py install

You'll need this boilerplate in your code to use it::

  from flask import Flask
  from flaskext.assets import Environment, Bundle
  from baseframe import baseframe, baseframe_js, baseframe_css

  app = Flask(__name__, instance_relative_config=True)
  app.register_blueprint(baseframe)

  assets = Environment(app)
  js = Bundle(baseframe_js)
  css = Bundle(baseframe_css)
  assets.register('js_all', js)
  assets.register('css_all', css)

  # Import models and views, and register routes here

Baseframe is BSD-licensed, but is built on top of Twitter Bootstrap 2.0,
which uses the Apache license.
