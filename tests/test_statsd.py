# -*- coding: utf-8 -*-
# Tests adapted from https://github.com/bbelyeu/flask-statsdclient

import six

import unittest

from flask import Flask

from baseframe.statsd import Statsd

try:
    from unittest.mock import patch
except ImportError:
    patch = None


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

    @property
    def statsd_core(self):
        return self.app.extensions['statsd_core']

    def test_default_config(self):
        assert self.statsd_core._addr == ('127.0.0.1', 8125)

    def test_custom_config(self):
        self.app.config['STATSD_HOST'] = '1.2.3.4'
        self.app.config['STATSD_PORT'] = 12345

        Statsd(self.app)
        assert self.statsd_core._addr == ('1.2.3.4', 12345)

    if six.PY3:

        # The wrapper in Statsd will:
        # 1. Prefix ``app.`` and `app.name` to the stat name
        # 2. Insert STATSD_RATE if no rate is specified
        # 3. Insert tags if tags are enabled and specified
        def test_wrapper(self):
            with patch('statsd.StatsClient.incr') as mock_incr:
                statsd.incr('test.counter')
                mock_incr.assert_called_once_with(
                    'flask_app.tests.test_statsd.test.counter', rate=1
                )
            with patch('statsd.StatsClient.incr') as mock_incr:
                statsd.incr('test.counter', rate=0.5)
                mock_incr.assert_called_once_with(
                    'flask_app.tests.test_statsd.test.counter', rate=0.5
                )
            with patch('statsd.StatsClient.incr') as mock_incr:
                statsd.incr('test.counter', 2, rate=0.5)
                mock_incr.assert_called_once_with(
                    'flask_app.tests.test_statsd.test.counter', 2, rate=0.5
                )

        def test_wrapper_custom_rate(self):
            self.app.config['STATSD_RATE'] = 0.3
            with patch('statsd.StatsClient.incr') as mock_incr:
                statsd.incr('test.counter')
                mock_incr.assert_called_once_with(
                    'flask_app.tests.test_statsd.test.counter', rate=0.3
                )
            with patch('statsd.StatsClient.incr') as mock_incr:
                statsd.incr('test.counter', rate=0.5)
                mock_incr.assert_called_once_with(
                    'flask_app.tests.test_statsd.test.counter', rate=0.5
                )

        def test_wrapper_tags(self):
            # Tags are converted into buckets if statsd doesn't support them
            with patch('statsd.StatsClient.incr') as mock_incr:
                statsd.incr('test.counter', tags={'tag': 'value'})
                mock_incr.assert_called_once_with(
                    'flask_app.tests.test_statsd.test.counter.tag_value', rate=1
                )

            # Tags are enabled if a separator character is specified in config,
            # and the app name is included as a tag instead of as a prefix.
            # `flask_app` is retained as a prefix.
            self.app.config['STATSD_TAGS'] = ';'
            with patch('statsd.StatsClient.incr') as mock_incr:
                statsd.incr('test.counter', tags={'tag': 'value'})
                mock_incr.assert_called_once_with(
                    'flask_app.test.counter;tag=value;app=tests.test_statsd', rate=1
                )
            with patch('statsd.StatsClient.incr') as mock_incr:
                statsd.incr('test.counter', tags={'tag': 'value', 't2': 'v2'})
                mock_incr.assert_called_once_with(
                    'flask_app.test.counter;tag=value;t2=v2;app=tests.test_statsd',
                    rate=1,
                )
            with patch('statsd.StatsClient.incr') as mock_incr:
                statsd.incr('test.counter', tags={'tag': 'val', 't2': 'v2', 't3': None})
                mock_incr.assert_called_once_with(
                    'flask_app.test.counter;tag=val;t2=v2;t3;app=tests.test_statsd',
                    rate=1,
                )
            with patch('statsd.StatsClient.incr') as mock_incr:
                statsd.incr('test.counter', tags={'tag': 'val', 't2': None, 't3': 'v3'})
                mock_incr.assert_called_once_with(
                    'flask_app.test.counter;tag=val;t2;t3=v3;app=tests.test_statsd',
                    rate=1,
                )

            # Other separator characters are supported too
            self.app.config['STATSD_TAGS'] = ','
            with patch('statsd.StatsClient.incr') as mock_incr:
                statsd.incr('test.counter', tags={'tag': 'value', 't2': 'v2'})
                mock_incr.assert_called_once_with(
                    'flask_app.test.counter,tag=value,t2=v2,app=tests.test_statsd',
                    rate=1,
                )


# TODO: Test all wrappers: ('timer', 'timing', 'incr', 'decr', 'gauge', 'set')
# TODO: Test pipeline()
# TODO: Test request handler stats
