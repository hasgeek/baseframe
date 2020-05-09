# -*- coding: utf-8 -*-
# Tests adapted from https://github.com/bbelyeu/flask-statsdclient

import unittest

from flask import Flask

from baseframe.statsd import Statsd

statsd = Statsd()


def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.update(config)
    statsd.init_app(app)
    return app


class TestStatsd(unittest.TestCase):
    """Test Statsd extension"""

    def setUp(self):
        self.app = create_app()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_default_config(self):
        assert self.app.extensions['statsd_core']._addr == ('127.0.0.1', 8125)

    def test_custom_config(self):
        self.app.config['STATSD_HOST'] = '1.2.3.4'
        self.app.config['STATSD_PORT'] = 12345

        Statsd(self.app)
        assert self.app.extensions['statsd_core']._addr == ('1.2.3.4', 12345)


# TODO: A full set of tests will require unittest.mock, available Py 3.3 onwards (not
# Py 2.7). Tests are pending for now, or will need a backward compatible method
