BaseFrame
=========

Reusable styles and templates for HasGeek projects. You'll need this
boilerplate to use it::

  from flask import Flask
  from flaskext.assets import Environment, Bundle
  from baseframe import baseframe, baseframe_js, baseframe_css

  app = Flask(__name__, instance_relative_config=True)
  app.register_blueprint(baseframe)
  app.config.from_pyfile('settings.py') # For your app's settings

  assets = Environment(app)
  js = Bundle(baseframe_js)
  css = Bundle(baseframe_css)
  assets.register('js_all', js)
  assets.register('css_all', css)

  # Import models and views, and register routes here
