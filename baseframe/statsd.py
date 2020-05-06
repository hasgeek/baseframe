# -*- coding: utf-8 -*-

from __future__ import absolute_import

import time

from flask import current_app, request

from statsd import StatsClient

__all__ = ['Statsd']

START_TIME_ATTR = 'statsd_start_time'

# This extension was adapted from
# https://github.com/nylas/flask-statsd/blob/master/flask_statsd.py


class Statsd(object):
    """
    Statsd extension for Flask

    Offers conveniences on top of using statsd directly:
    1. In a multi-app setup, each app can have its own statsd config
    2. The app's name is automatically prefixed to all stats
    3. Sampling rate can be specified in app config instead of in each call
    4. Requests are automatically timed and counted unless STATSD_REQUEST_TIMER is False

    App configuration defaults:

    STATSD_HOST = '127.0.0.1'
    STATSD_PORT = 8125
    STATSD_PREFIX = None
    STATSD_MAXUDPSIZE = 512
    STATSD_IPV6 = False
    STATSD_RATE = 1
    STATSD_REQUEST_TIMER = True
    """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('STATSD_RATE', 1)

        app.statsd = StatsClient(
            host=app.config.setdefault('STATSD_HOST', '127.0.0.1'),
            port=app.config.setdefault('STATSD_PORT', 8125),
            prefix=app.config.setdefault('STATSD_PREFIX', None),
            maxudpsize=app.config.setdefault('STATSD_MAXUDPSIZE', 512),
            ipv6=app.config.setdefault('STATSD_IPV6', False),
        )

        if app.config.setdefault('STATSD_REQUEST_TIMER', True):
            app.before_request(self._before_request)
            app.after_request(self._after_request)

    def _metric_name(self, name):
        return '%s.%s' % (current_app.name, name)

    def timer(self, stat, rate=None):
        """
        Return a Timer object that can be used as a context manager to automatically
        record timing for a block or function call. Use as a decorator is not supported
        as an application context is required.
        """
        return current_app.statsd.timer(
            stat, rate=rate if rate is not None else current_app.config['STATSD_RATE']
        )

    def timing(self, stat, delta, rate=None):
        """
        Record timer information.
        """
        return current_app.statsd.timing(
            self._metric_name(stat),
            delta,
            rate=rate if rate is not None else current_app.config['STATSD_RATE'],
        )

    def incr(self, stat, count=1, rate=None):
        """
        Increment a counter.
        """
        return current_app.statsd.incr(
            self._metric_name(stat),
            count,
            rate=rate if rate is not None else current_app.config['STATSD_RATE'],
        )

    def decr(self, stat, count=1, rate=None):
        """
        Decrement a counter.
        """
        return current_app.statsd.decr(
            self._metric_name(stat),
            count,
            rate=rate if rate is not None else current_app.config['STATSD_RATE'],
        )

    def gauge(self, stat, value, rate=None, delta=False):
        """
        Set a gauge value.
        """
        return current_app.statsd.gauge(
            self._metric_name(stat),
            value,
            rate=rate if rate is not None else current_app.config['STATSD_RATE'],
            delta=delta,
        )

    def set(self, stat, value, rate=None):  # NOQA: A003
        """
        Increment a set value.

        The statsd server does _not_ take the sample rate into account for sets. Use
        with care.
        """
        return current_app.statsd.set(
            self._metric_name(stat),
            value,
            rate=rate if rate is not None else current_app.config['STATSD_RATE'],
        )

    def pipeline(self):
        return current_app.statsd.pipeline()

    def _before_request(self):
        if current_app.config['STATSD_RATE'] != 0:
            setattr(request, START_TIME_ATTR, time.time())

    def _after_request(self, response):
        if hasattr(request, START_TIME_ATTR):
            metrics = [
                '.'.join(
                    ['request_handlers', request.endpoint, str(response.status_code)]
                ),
                '.'.join(['request_handlers', '_overall', str(response.status_code)]),
            ]

            for metric_name in metrics:
                # Use `timing` instead of `timer` because we record it as two metrics.
                # Convert time from seconds:float to milliseconds:int
                self.timing(
                    metric_name,
                    int((time.time() - getattr(request, START_TIME_ATTR)) * 1000),
                )
                self.incr(metric_name)

        return response
