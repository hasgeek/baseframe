# -*- coding: utf-8 -*-

from __future__ import absolute_import

import time

from flask import current_app, request, request_finished, request_started

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

    App configuration defaults::

        SITE_ID = app.name  # Used as a prefix in stats
        STATSD_HOST = '127.0.0.1'
        STATSD_PORT = 8125
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
        app.config.setdefault('SITE_ID', app.name)

        app.extensions['statsd'] = self
        app.extensions['statsd_core'] = StatsClient(
            host=app.config.setdefault('STATSD_HOST', '127.0.0.1'),
            port=app.config.setdefault('STATSD_PORT', 8125),
            prefix=None,
            maxudpsize=app.config.setdefault('STATSD_MAXUDPSIZE', 512),
            ipv6=app.config.setdefault('STATSD_IPV6', False),
        )

        if app.config.setdefault('STATSD_REQUEST_TIMER', True):
            # Use signals because they are called before and after all other request
            # processors, allowing us to capture (nearly) all time taken for processing
            request_started.connect(self._request_started, app)
            request_finished.connect(self._request_finished, app)

    def _metric_name(self, name):
        return 'app.%s.%s' % (current_app.config['SITE_ID'], name)

    def timer(self, stat, rate=None):
        """
        Return a Timer object that can be used as a context manager to automatically
        record timing for a block or function call. Use as a decorator is not supported
        as an application context is required.
        """
        return current_app.extensions['statsd_core'].timer(
            stat, rate=rate if rate is not None else current_app.config['STATSD_RATE']
        )

    def timing(self, stat, delta, rate=None):
        """
        Record timer information.
        """
        return current_app.extensions['statsd_core'].timing(
            self._metric_name(stat),
            delta,
            rate=rate if rate is not None else current_app.config['STATSD_RATE'],
        )

    def incr(self, stat, count=1, rate=None):
        """
        Increment a counter.
        """
        return current_app.extensions['statsd_core'].incr(
            self._metric_name(stat),
            count,
            rate=rate if rate is not None else current_app.config['STATSD_RATE'],
        )

    def decr(self, stat, count=1, rate=None):
        """
        Decrement a counter.
        """
        return current_app.extensions['statsd_core'].decr(
            self._metric_name(stat),
            count,
            rate=rate if rate is not None else current_app.config['STATSD_RATE'],
        )

    def gauge(self, stat, value, rate=None, delta=False):
        """
        Set a gauge value.
        """
        return current_app.extensions['statsd_core'].gauge(
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
        return current_app.extensions['statsd_core'].set(
            self._metric_name(stat),
            value,
            rate=rate if rate is not None else current_app.config['STATSD_RATE'],
        )

    def pipeline(self):
        return current_app.extensions['statsd_core'].pipeline()

    def _request_started(self, app):
        if app.config['STATSD_RATE'] != 0:
            setattr(request, START_TIME_ATTR, time.time())

    def _request_finished(self, app, response):
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
