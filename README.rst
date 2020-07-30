Baseframe
=========

|docs| |travis| |coveralls|

Reusable styles and templates for Hasgeek projects. Setup instructions::

    python setup.py install

Or, to use in a development environment where Baseframe will change frequently::

    python setup.py develop
    make

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


.. |docs| image:: https://readthedocs.org/projects/baseframe/badge/?version=latest
    :target: http://baseframe.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation status

.. |travis| image:: https://secure.travis-ci.org/hasgeek/baseframe.svg?branch=master
    :target: https://travis-ci.org/hasgeek/baseframe
    :alt: Build status

.. |coveralls| image:: https://coveralls.io/repos/hasgeek/baseframe/badge.svg
    :target: https://coveralls.io/r/hasgeek/baseframe
    :alt: Coverage status
