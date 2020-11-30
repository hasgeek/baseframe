# Tests adapted from https://github.com/bbelyeu/flask-statsdclient

from datetime import timedelta
from unittest.mock import patch

from flask import Flask

from statsd.client.timer import Timer
from statsd.client.udp import Pipeline
import pytest

from baseframe.statsd import Statsd


@pytest.fixture()
def app():
    app = Flask(__name__)
    return app


@pytest.fixture()
def statsd(app):
    statsd = Statsd()
    statsd.init_app(app)
    return statsd


@pytest.fixture()
def ctx(app):
    ctx = app.app_context()
    ctx.push()
    yield ctx
    ctx.pop()


def test_default_config(app, statsd):
    assert app.extensions['statsd_core']._addr == ('127.0.0.1', 8125)


def test_custom_config(app):
    app.config['STATSD_HOST'] = '1.2.3.4'
    app.config['STATSD_PORT'] = 12345

    Statsd(app)
    assert app.extensions['statsd_core']._addr == ('1.2.3.4', 12345)


# The wrapper methods in Statsd will:
# 1. Prefix ``app.`` and `app.name` to the stat name
# 2. Insert STATSD_RATE if no rate is specified
# 3. Insert tags if tags are enabled and specified


def test_incr(ctx, statsd):
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter')
        mock_incr.assert_called_once_with(
            'flask_app.tests.test_statsd.test.counter', 1, rate=1
        )
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', rate=0.5)
        mock_incr.assert_called_once_with(
            'flask_app.tests.test_statsd.test.counter', 1, rate=0.5
        )
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', 2, rate=0.5)
        mock_incr.assert_called_once_with(
            'flask_app.tests.test_statsd.test.counter', 2, rate=0.5
        )


def test_decr(ctx, statsd):
    with patch('statsd.StatsClient.decr') as mock_decr:
        statsd.decr('test.counter')
        mock_decr.assert_called_once_with(
            'flask_app.tests.test_statsd.test.counter', 1, rate=1
        )
    with patch('statsd.StatsClient.decr') as mock_decr:
        statsd.decr('test.counter', rate=0.5)
        mock_decr.assert_called_once_with(
            'flask_app.tests.test_statsd.test.counter', 1, rate=0.5
        )
    with patch('statsd.StatsClient.decr') as mock_decr:
        statsd.decr('test.counter', 2, rate=0.5)
        mock_decr.assert_called_once_with(
            'flask_app.tests.test_statsd.test.counter', 2, rate=0.5
        )


def test_gauge(ctx, statsd):
    with patch('statsd.StatsClient.gauge') as mock_gauge:
        statsd.gauge('test.gauge', 5)
        mock_gauge.assert_called_once_with(
            'flask_app.tests.test_statsd.test.gauge', 5, rate=1, delta=False
        )
    with patch('statsd.StatsClient.gauge') as mock_gauge:
        statsd.gauge('test.gauge', 5, rate=0.5)
        mock_gauge.assert_called_once_with(
            'flask_app.tests.test_statsd.test.gauge', 5, rate=0.5, delta=False
        )
    with patch('statsd.StatsClient.gauge') as mock_gauge:
        statsd.gauge('test.gauge', 10, rate=0.5, delta=True)
        mock_gauge.assert_called_once_with(
            'flask_app.tests.test_statsd.test.gauge', 10, rate=0.5, delta=True
        )


def test_set(ctx, statsd):
    with patch('statsd.StatsClient.set') as mock_set:
        statsd.set('test.set', 'item')
        mock_set.assert_called_once_with(
            'flask_app.tests.test_statsd.test.set', 'item', rate=1
        )
    with patch('statsd.StatsClient.set') as mock_set:
        statsd.set('test.set', 'item', rate=0.5)
        mock_set.assert_called_once_with(
            'flask_app.tests.test_statsd.test.set', 'item', rate=0.5
        )


def test_timing(ctx, statsd):
    with patch('statsd.StatsClient.timing') as mock_timing:
        statsd.timing('test.timing', 10)
        mock_timing.assert_called_once_with(
            'flask_app.tests.test_statsd.test.timing', 10, rate=1
        )
    with patch('statsd.StatsClient.timing') as mock_timing:
        statsd.timing('test.timing', timedelta(seconds=5), rate=0.5)
        mock_timing.assert_called_once_with(
            'flask_app.tests.test_statsd.test.timing', timedelta(seconds=5), rate=0.5
        )


def test_timer(ctx, statsd):
    timer = statsd.timer('test.timer', rate=1)
    assert isinstance(timer, Timer)
    assert timer.stat == 'flask_app.tests.test_statsd.test.timer'
    assert timer.rate == 1

    timer = statsd.timer('test.timer', rate=0.5)
    assert isinstance(timer, Timer)
    assert timer.stat == 'flask_app.tests.test_statsd.test.timer'
    assert timer.rate == 0.5


def test_pipeline(ctx, statsd):
    pipeline = statsd.pipeline()
    assert isinstance(pipeline, Pipeline)


def test_custom_rate(app, ctx, statsd):
    app.config['STATSD_RATE'] = 0.3
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter')
        mock_incr.assert_called_once_with(
            'flask_app.tests.test_statsd.test.counter', 1, rate=0.3
        )
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', rate=0.5)
        mock_incr.assert_called_once_with(
            'flask_app.tests.test_statsd.test.counter', 1, rate=0.5
        )


def test_tags(app, ctx, statsd):
    # Tags are converted into buckets if statsd doesn't support them
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', tags={'tag': 'value'})
        mock_incr.assert_called_once_with(
            'flask_app.tests.test_statsd.test.counter.tag_value', 1, rate=1
        )

    # Tags are enabled if a separator character is specified in config.
    # The app name is then included as a tag instead of as a prefix.
    # `flask_app` is retained as a prefix.
    app.config['STATSD_TAGS'] = ';'
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', tags={'tag': 'value'})
        mock_incr.assert_called_once_with(
            'flask_app.test.counter;tag=value;app=tests.test_statsd', 1, rate=1
        )
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', tags={'tag': 'value', 't2': 'v2'})
        mock_incr.assert_called_once_with(
            'flask_app.test.counter;tag=value;t2=v2;app=tests.test_statsd',
            1,
            rate=1,
        )
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', tags={'tag': 'val', 't2': 'v2', 't3': None})
        mock_incr.assert_called_once_with(
            'flask_app.test.counter;tag=val;t2=v2;t3;app=tests.test_statsd',
            1,
            rate=1,
        )
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', tags={'tag': 'val', 't2': None, 't3': 'v3'})
        mock_incr.assert_called_once_with(
            'flask_app.test.counter;tag=val;t2;t3=v3;app=tests.test_statsd',
            1,
            rate=1,
        )

    # Other separator characters are supported too
    app.config['STATSD_TAGS'] = ','
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', tags={'tag': 'value', 't2': 'v2'})
        mock_incr.assert_called_once_with(
            'flask_app.test.counter,tag=value,t2=v2,app=tests.test_statsd',
            1,
            rate=1,
        )


# TODO: Test request handler and form error stats
