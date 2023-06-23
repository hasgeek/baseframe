"""Statsd logger."""

import time
import typing as t
from datetime import timedelta

from flask import Flask, current_app, request, request_finished, request_started
from flask_wtf import FlaskForm
from statsd import StatsClient
from statsd.client.timer import Timer
from statsd.client.udp import Pipeline
from werkzeug.wrappers import Response

from .signals import form_validation_error, form_validation_success

__all__ = ['Statsd']

START_TIME_ATTR = 'statsd_start_time'

TagsType = t.Dict[str, t.Union[int, str, None]]


class Statsd:
    """
    Statsd extension for Flask.

    Offers conveniences on top of using py-statsd directly:

    1. In a multi-app setup, each app can have its own statsd config
    2. The app's name is automatically prefixed to all stats
    3. Sampling rate can be specified in app config
    4. Requests are automatically timed and counted unless ``STATSD_REQUEST_TIMER`` is
       False

    App configuration defaults::

        SITE_ID = app.name  # Used as a prefix in stats
        STATSD_HOST = '127.0.0.1'
        STATSD_PORT = 8125
        STATSD_MAXUDPSIZE = 512
        STATSD_IPV6 = False
        STATSD_RATE = 1
        STATSD_TAGS = False
        STATSD_REQUEST_LOG = True
        STATSD_FORM_LOG = True

    If the statsd server supports tags, the ``STATSD_TAGS`` parameter may be set to a
    separator character as per the server's syntax.

    Telegraf/Influxdb uses a comma: ``'metric_name,tag1=value1,tag2=value2'``

    Carbon/Graphite uses a semicolon: ``'metric_name;tag1=value;tag2=value2'``

    Tags will be converted into dot-separated buckets if ``STATSD_TAGS`` is falsy.
    Using an ordered dict is recommended (default in Py 3.6+) to ensure meaningful
    bucket order.

    Servers have varying limitations on the allowed content in tags and values.
    Alphanumeric values are generally safe. This extension does not validate content.
    From Carbon/Graphite's documentation:

       Tag names must have a length >= 1 and may contain any ascii characters except
       ``;!^=``. Tag values must also have a length >= 1, they may contain any ascii
       characters except ``;`` and the first character must not be ``~``. UTF-8
       characters may work for names and values, but they are not well tested and it is
       not recommended to use non-ascii characters in metric names or tags.

    The Datadog and SignalFx tag formats are not supported at this time.
    """

    def __init__(self, app: t.Optional[Flask] = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        app.config.setdefault('STATSD_RATE', 1)
        app.config.setdefault('SITE_ID', app.name)
        app.config.setdefault('STATSD_TAGS', False)
        app.config.setdefault('STATSD_FORM_LOG', True)

        app.extensions['statsd'] = self
        app.extensions['statsd_core'] = StatsClient(
            host=app.config.setdefault('STATSD_HOST', '127.0.0.1'),
            port=app.config.setdefault('STATSD_PORT', 8125),
            prefix=None,
            maxudpsize=app.config.setdefault('STATSD_MAXUDPSIZE', 512),
            ipv6=app.config.setdefault('STATSD_IPV6', False),
        )

        if app.config.setdefault('STATSD_REQUEST_LOG', True):
            # Use signals because they are called before and after all other request
            # processors, allowing us to capture (nearly) all time taken for processing
            request_started.connect(self._request_started, app)
            request_finished.connect(self._request_finished, app)

    def _metric_name(self, name: str, tags: t.Optional[TagsType] = None) -> str:
        if tags is None:
            tags = {}
        if current_app.config['STATSD_TAGS']:
            prefix = 'flask_app'
            tags['app'] = current_app.config['SITE_ID']
            tag_sep = current_app.config['STATSD_TAGS']
            tag_join = '='
        else:
            prefix = f'flask_app.{current_app.config["SITE_ID"]}'
            tag_sep = '.'
            tag_join = '_'
        if tags:
            name += tag_sep + tag_sep.join(
                tag_join.join((str(t), str(v))) if v is not None else str(t)
                for t, v in tags.items()
            )
        return f'{prefix}.{name}'

    def timer(
        self,
        stat: str,
        rate: t.Optional[t.Union[int, float]] = None,
        tags: t.Optional[TagsType] = None,
    ) -> Timer:
        """Return a Timer."""
        stat = self._metric_name(stat, tags)
        return current_app.extensions['statsd_core'].timer(
            stat, rate=rate if rate is not None else current_app.config['STATSD_RATE']
        )

    def timing(
        self,
        stat: str,
        delta: t.Union[int, timedelta],
        rate: t.Optional[t.Union[int, float]] = None,
        tags: t.Optional[TagsType] = None,
    ) -> None:
        """
        Send new timing information.

        :param delta: Either a number of milliseconds, or a timedelta
        """
        stat = self._metric_name(stat, tags)
        current_app.extensions['statsd_core'].timing(
            stat,
            delta,
            rate=rate if rate is not None else current_app.config['STATSD_RATE'],
        )

    def incr(
        self,
        stat: str,
        count: int = 1,
        rate: t.Optional[t.Union[int, float]] = None,
        tags: t.Optional[TagsType] = None,
    ) -> None:
        """Increment a stat by `count`."""
        stat = self._metric_name(stat, tags)
        current_app.extensions['statsd_core'].incr(
            stat,
            count,
            rate=rate if rate is not None else current_app.config['STATSD_RATE'],
        )

    def decr(
        self,
        stat: str,
        count: int = 1,
        rate: t.Optional[t.Union[int, float]] = None,
        tags: t.Optional[TagsType] = None,
    ) -> None:
        """Decrement a stat by `count`."""
        stat = self._metric_name(stat, tags)
        current_app.extensions['statsd_core'].decr(
            stat,
            count,
            rate=rate if rate is not None else current_app.config['STATSD_RATE'],
        )

    def gauge(
        self,
        stat: str,
        value: int,
        rate: t.Optional[t.Union[int, float]] = None,
        delta: bool = False,
        tags: t.Optional[TagsType] = None,
    ) -> None:
        """Set a gauge value."""
        stat = self._metric_name(stat, tags)
        current_app.extensions['statsd_core'].gauge(
            stat,
            value,
            rate=rate if rate is not None else current_app.config['STATSD_RATE'],
            delta=delta,
        )

    def set(  # noqa: A003
        self,
        stat: str,
        value: str,
        rate: t.Optional[t.Union[int, float]] = None,
        tags: t.Optional[TagsType] = None,
    ) -> None:
        """Set a set value."""
        stat = self._metric_name(stat, tags)
        current_app.extensions['statsd_core'].set(
            stat,
            value,
            rate=rate if rate is not None else current_app.config['STATSD_RATE'],
        )

    def pipeline(self) -> Pipeline:
        return current_app.extensions['statsd_core'].pipeline()

    def _request_started(self, app: Flask) -> None:
        if app.config['STATSD_RATE'] != 0:
            setattr(request, START_TIME_ATTR, time.time())

    def _request_finished(self, app: Flask, response: Response) -> None:
        if hasattr(request, START_TIME_ATTR):
            metrics = [
                (
                    'request_handlers',
                    {'endpoint': request.endpoint, 'status_code': response.status_code},
                )
            ]
            if not app.config['STATSD_TAGS']:
                metrics.append(
                    (
                        'request_handlers',
                        {'endpoint': '_overall', 'status_code': response.status_code},
                    )
                )

            for metric_name, tags in metrics:
                # Use `timing` instead of `timer` because we record it as two metrics.
                # Convert time from seconds:float to milliseconds:int
                self.timing(
                    metric_name,
                    int((time.time() - getattr(request, START_TIME_ATTR)) * 1000),
                    tags=tags,
                )
                # The timer metric also registers a count, making the counter metric
                # seemingly redundant, but the counter metric also includes a rate, so
                # we use both: timer (via `timing`) and counter (via `incr`).
                self.incr(metric_name, tags=tags)


@form_validation_success.connect
def _statsd_form_validation_success(form: FlaskForm) -> None:
    if (
        current_app
        and current_app.config.get('STATSD_FORM_LOG')
        and 'statsd' in current_app.extensions
    ):
        current_app.extensions['statsd'].incr(
            'form_validation_success', tags={'form': form.__class__.__name__}
        )


@form_validation_error.connect
def _statsd_form_validation_error(form: FlaskForm) -> None:
    if (
        current_app
        and current_app.config.get('STATSD_FORM_LOG')
        and 'statsd' in current_app.extensions
    ):
        # Submit errors one metric at a time as there's no obvious way to submit all
        for field in form.errors:
            current_app.extensions['statsd'].incr(
                'form_validation_error',
                tags={'form': form.__class__.__name__, 'field': str(field)},
            )
