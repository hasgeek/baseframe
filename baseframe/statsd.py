# -*- coding: utf-8 -*-

from __future__ import absolute_import

from functools import partial
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

    Offers conveniences on top of using py-statsd directly:
    1. In a multi-app setup, each app can have its own statsd config
    2. The app's name is automatically prefixed to all stats
    3. Sampling rate can be specified in app config
    4. Requests are automatically timed and counted unless STATSD_REQUEST_TIMER is False

    App configuration defaults::

        SITE_ID = app.name  # Used as a prefix in stats
        STATSD_HOST = '127.0.0.1'
        STATSD_PORT = 8125
        STATSD_MAXUDPSIZE = 512
        STATSD_IPV6 = False
        STATSD_RATE = 1
        STATSD_TAGS = None
        STATSD_REQUEST_TIMER = True

    If the statsd server supports tags, the ``STATSD_TAGS`` parameter may be set to a
    separator character as per the server's syntax.

    Influxdb uses a comma: ``'metric_name,tag1=value1,tag2=value2'``

    Carbon/Graphite uses a semicolon: ``'metric_name;tag1=value;tag2=value2'``

    Tags will be discarded when ``STATSD_TAGS`` is unset. Servers have varying
    limitations on the allowed content in tags and values. Alphanumeric values are
    generally safe. This extension does not validate content. From Carbon/Graphite's
    documentation:

    > Tag names must have a length >= 1 and may contain any ascii characters except
    > ``;!^=``. Tag values must also have a length >= 1, they may contain any ascii
    > characters except ``;`` and the first character must not be ``~``. UTF-8
    > characters may work for names and values, but they are not well tested and it is
    > not recommended to use non-ascii characters in metric names or tags.

    The Datadog and SignalFx tag formats are not supported at this time.
    """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

        # Py 3.4+ has `functools.partialmethod`, allowing these to be set directly
        # on the class, but as per `timeit` it is about 50% slower. Since this class
        # will be instantiated only once per runtime, we get an overall performance
        # improvement at the cost of making it slightly harder to find documentation.
        for method in ('timer', 'timing', 'incr', 'decr', 'gauge', 'set'):
            func = partial(self._wrapper, method)
            func.__name__ = method
            setattr(self, method, func)

    def init_app(self, app):
        app.config.setdefault('STATSD_RATE', 1)
        app.config.setdefault('SITE_ID', app.name)
        app.config.setdefault('STATSD_TAGS', None)

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

    def _metric_name(self, name, tags):
        # In Py 3.8, the following two lines can be combined with a walrus operator:
        # if tags and (tag_sep := current_app.config['STATSD_TAGS']):
        if tags and current_app.config['STATSD_TAGS']:
            tag_sep = current_app.config['STATSD_TAGS']
            name += tag_sep + tag_sep.join(
                '='.join((str(t), str(v))) if v is not None else str(t)
                for t, v in tags.items()
            )
        return 'app.%s.%s' % (current_app.config['SITE_ID'], name)

    def _wrapper(self, metric, stat, *args, **kwargs):
        tags = kwargs.pop('tags', None)
        if kwargs.setdefault('rate', None) is None:
            kwargs['rate'] = current_app.config['STATSD_RATE']
        stat = self._metric_name(stat, tags)

        getattr(current_app.extensions['statsd_core'], metric)(stat, *args, **kwargs)

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
                # The timer metric also registers a count, making the counter metric
                # seemingly redundant, but the counter metric also includes a rate, so
                # we use both: timer (via `timing`) and counter (via `incr`).
                self.incr(metric_name)
