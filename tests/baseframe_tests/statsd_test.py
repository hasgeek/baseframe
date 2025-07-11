"""Test statsd logging."""

# pylint: disable=redefined-outer-name

# Tests adapted from https://github.com/bbelyeu/flask-statsdclient

from __future__ import annotations

from collections.abc import Callable
from datetime import timedelta
from unittest.mock import patch

import pytest
from flask import Flask, render_template_string
from flask.ctx import AppContext
from flask.typing import ResponseReturnValue
from flask_babel import Babel
from statsd.client.timer import Timer
from statsd.client.udp import Pipeline

from baseframe import forms
from baseframe.statsd import Statsd


@pytest.fixture
def app() -> Flask:
    """Redefine app without Baseframe for statsd tests."""
    return Flask(__name__)


@pytest.fixture
def statsd(app: Flask) -> Statsd:
    s = Statsd()
    s.init_app(app)
    return s


@pytest.fixture
def view(app: Flask) -> Callable[[], ResponseReturnValue]:
    @app.route('/')
    def index() -> ResponseReturnValue:
        return 'index'

    return index


@pytest.fixture
def form(app: Flask) -> forms.Form:
    Babel(app)  # Needed for form validator message translations

    class SimpleForm(forms.Form):
        field = forms.StringField(
            "Required", validators=[forms.validators.DataRequired()]
        )

    return SimpleForm(meta={'csrf': False})


def test_default_config(app: Flask, statsd: Statsd) -> None:
    # pylint: disable=protected-access
    assert app.extensions['statsd_core']._addr == ('127.0.0.1', 8125)


def test_custom_config(app: Flask) -> None:
    # pylint: disable=protected-access
    app.config['STATSD_HOST'] = '1.2.3.4'
    app.config['STATSD_PORT'] = 12345

    Statsd(app)
    assert app.extensions['statsd_core']._addr == ('1.2.3.4', 12345)


# The wrapper methods in Statsd will:
# 1. Prefix ``app.`` and `app.name` to the stat name
# 2. Insert STATSD_RATE if no rate is specified
# 3. Insert tags if tags are enabled and specified


def test_incr(ctx: AppContext, statsd) -> None:
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter')
        mock_incr.assert_called_once_with(
            'flask_app.baseframe_tests.statsd_test.test.counter', 1, rate=1
        )
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', rate=0.5)
        mock_incr.assert_called_once_with(
            'flask_app.baseframe_tests.statsd_test.test.counter', 1, rate=0.5
        )
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', 2, rate=0.5)
        mock_incr.assert_called_once_with(
            'flask_app.baseframe_tests.statsd_test.test.counter', 2, rate=0.5
        )


def test_decr(ctx: AppContext, statsd: Statsd) -> None:
    with patch('statsd.StatsClient.decr') as mock_decr:
        statsd.decr('test.counter')
        mock_decr.assert_called_once_with(
            'flask_app.baseframe_tests.statsd_test.test.counter', 1, rate=1
        )
    with patch('statsd.StatsClient.decr') as mock_decr:
        statsd.decr('test.counter', rate=0.5)
        mock_decr.assert_called_once_with(
            'flask_app.baseframe_tests.statsd_test.test.counter', 1, rate=0.5
        )
    with patch('statsd.StatsClient.decr') as mock_decr:
        statsd.decr('test.counter', 2, rate=0.5)
        mock_decr.assert_called_once_with(
            'flask_app.baseframe_tests.statsd_test.test.counter', 2, rate=0.5
        )


def test_gauge(ctx: AppContext, statsd: Statsd) -> None:
    with patch('statsd.StatsClient.gauge') as mock_gauge:
        statsd.gauge('test.gauge', 5)
        mock_gauge.assert_called_once_with(
            'flask_app.baseframe_tests.statsd_test.test.gauge', 5, rate=1, delta=False
        )
    with patch('statsd.StatsClient.gauge') as mock_gauge:
        statsd.gauge('test.gauge', 5, rate=0.5)
        mock_gauge.assert_called_once_with(
            'flask_app.baseframe_tests.statsd_test.test.gauge', 5, rate=0.5, delta=False
        )
    with patch('statsd.StatsClient.gauge') as mock_gauge:
        statsd.gauge('test.gauge', 10, rate=0.5, delta=True)
        mock_gauge.assert_called_once_with(
            'flask_app.baseframe_tests.statsd_test.test.gauge', 10, rate=0.5, delta=True
        )


def test_set(ctx: AppContext, statsd: Statsd) -> None:
    with patch('statsd.StatsClient.set') as mock_set:
        statsd.set('test.set', 'item')
        mock_set.assert_called_once_with(
            'flask_app.baseframe_tests.statsd_test.test.set', 'item', rate=1
        )
    with patch('statsd.StatsClient.set') as mock_set:
        statsd.set('test.set', 'item', rate=0.5)
        mock_set.assert_called_once_with(
            'flask_app.baseframe_tests.statsd_test.test.set', 'item', rate=0.5
        )


def test_timing(ctx: AppContext, statsd: Statsd) -> None:
    with patch('statsd.StatsClient.timing') as mock_timing:
        statsd.timing('test.timing', 10)
        mock_timing.assert_called_once_with(
            'flask_app.baseframe_tests.statsd_test.test.timing', 10, rate=1
        )
    with patch('statsd.StatsClient.timing') as mock_timing:
        statsd.timing('test.timing', timedelta(seconds=5), rate=0.5)
        mock_timing.assert_called_once_with(
            'flask_app.baseframe_tests.statsd_test.test.timing',
            timedelta(seconds=5),
            rate=0.5,
        )


def test_timer(ctx: AppContext, statsd: Statsd) -> None:
    timer = statsd.timer('test.timer', rate=1)
    assert isinstance(timer, Timer)
    assert timer.stat == 'flask_app.baseframe_tests.statsd_test.test.timer'
    assert timer.rate == 1

    timer = statsd.timer('test.timer', rate=0.5)
    assert isinstance(timer, Timer)
    assert timer.stat == 'flask_app.baseframe_tests.statsd_test.test.timer'
    assert timer.rate == 0.5


def test_pipeline(ctx: AppContext, statsd: Statsd) -> None:
    pipeline = statsd.pipeline()
    assert isinstance(pipeline, Pipeline)


def test_custom_rate(app: Flask, ctx: AppContext, statsd: Statsd) -> None:
    app.config['STATSD_RATE'] = 0.3
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter')
        mock_incr.assert_called_once_with(
            'flask_app.baseframe_tests.statsd_test.test.counter', 1, rate=0.3
        )
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', rate=0.5)
        mock_incr.assert_called_once_with(
            'flask_app.baseframe_tests.statsd_test.test.counter', 1, rate=0.5
        )


def test_tags(app: Flask, ctx: AppContext, statsd: Statsd) -> None:
    # Tags are converted into buckets if statsd doesn't support them
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', tags={'tag': 'value'})
        mock_incr.assert_called_once_with(
            'flask_app.baseframe_tests.statsd_test.test.counter.tag_value', 1, rate=1
        )

    # Tags are enabled if a separator character is specified in config.
    # The app name is then included as a tag instead of as a prefix.
    # `flask_app` is retained as a prefix.
    app.config['STATSD_TAGS'] = ';'
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', tags={'tag': 'value'})
        mock_incr.assert_called_once_with(
            'flask_app.test.counter;tag=value;app=baseframe_tests.statsd_test',
            1,
            rate=1,
        )
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', tags={'tag': 'value', 't2': 'v2'})
        mock_incr.assert_called_once_with(
            'flask_app.test.counter;tag=value;t2=v2;app=baseframe_tests.statsd_test',
            1,
            rate=1,
        )
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', tags={'tag': 'val', 't2': 'v2', 't3': None})
        mock_incr.assert_called_once_with(
            'flask_app.test.counter;tag=val;t2=v2;t3;app=baseframe_tests.statsd_test',
            1,
            rate=1,
        )
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', tags={'tag': 'val', 't2': None, 't3': 'v3'})
        mock_incr.assert_called_once_with(
            'flask_app.test.counter;tag=val;t2;t3=v3;app=baseframe_tests.statsd_test',
            1,
            rate=1,
        )

    # Other separator characters are supported too
    app.config['STATSD_TAGS'] = ','
    with patch('statsd.StatsClient.incr') as mock_incr:
        statsd.incr('test.counter', tags={'tag': 'value', 't2': 'v2'})
        mock_incr.assert_called_once_with(
            'flask_app.test.counter,tag=value,t2=v2,app=baseframe_tests.statsd_test',
            1,
            rate=1,
        )


def test_request_handler_notags(
    app: Flask, statsd: Statsd, view: Callable[[], ResponseReturnValue]
) -> None:
    """Test request_handlers logging with tags disabled."""
    with (
        patch('statsd.StatsClient.incr') as mock_incr,
        patch('statsd.StatsClient.timing') as mock_timing,
        app.test_client() as client,
    ):
        client.get('/')
        # First call
        mock_incr.assert_any_call(
            'flask_app.baseframe_tests.statsd_test.request_handlers'
            '.endpoint_index.status_code_200',
            1,
            rate=1,
        )
        # Second and last call
        mock_incr.assert_called_with(
            'flask_app.baseframe_tests.statsd_test.request_handlers'
            '.endpoint__overall.status_code_200',
            1,
            rate=1,
        )
        mock_timing.assert_called()


def test_request_handler_tags(
    app: Flask, statsd: Statsd, view: Callable[[], ResponseReturnValue]
) -> None:
    """Test request_handlers logging with tags enabled."""
    app.config['STATSD_TAGS'] = ','
    with (
        patch('statsd.StatsClient.incr') as mock_incr,
        patch('statsd.StatsClient.timing') as mock_timing,
        app.test_client() as client,
    ):
        client.get('/')
        mock_incr.assert_called_once_with(
            'flask_app.request_handlers,endpoint=index,status_code=200'
            ',app=baseframe_tests.statsd_test',
            1,
            rate=1,
        )
        mock_timing.assert_called_once()


def test_request_handler_disabled(
    app: Flask, view: Callable[[], ResponseReturnValue]
) -> None:
    """Test request_handlers logging disabled."""
    app.config['STATSD_REQUEST_LOG'] = False
    Statsd(app)
    with (
        patch('statsd.StatsClient.incr') as mock_incr,
        patch('statsd.StatsClient.timing') as mock_timing,
        app.test_client() as client,
    ):
        client.get('/')
        mock_incr.assert_not_called()
        mock_timing.assert_not_called()


def test_render_template_notags(app: Flask, statsd: Statsd) -> None:
    """Test render_template logging with tags disabled."""
    with (
        patch('statsd.StatsClient.incr') as mock_incr,
        patch('statsd.StatsClient.timing') as mock_timing,
        app.app_context(),
    ):
        render_template_string("Test template")
        assert mock_incr.call_count == 2
        assert mock_timing.call_count == 2
        assert [c[0][0] for c in mock_incr.call_args_list] == [
            'flask_app.baseframe_tests.statsd_test.render_template.template__str',
            'flask_app.baseframe_tests.statsd_test.render_template.template__overall',
        ]
        assert [c[0][0] for c in mock_incr.call_args_list] == [
            'flask_app.baseframe_tests.statsd_test.render_template.template__str',
            'flask_app.baseframe_tests.statsd_test.render_template.template__overall',
        ]


def test_render_template_tags(app: Flask, statsd: Statsd) -> None:
    """Test render_template logging with tags enabled."""
    app.config['STATSD_TAGS'] = ','
    with (
        patch('statsd.StatsClient.incr') as mock_incr,
        patch('statsd.StatsClient.timing') as mock_timing,
        app.app_context(),
    ):
        render_template_string("Test template")
        assert mock_incr.call_count == 1
        assert mock_timing.call_count == 1
        assert (
            mock_incr.call_args[0][0] == 'flask_app.render_template,template=_str,'
            'app=baseframe_tests.statsd_test'
        )
        assert (
            mock_incr.call_args[0][0] == 'flask_app.render_template,template=_str,'
            'app=baseframe_tests.statsd_test'
        )


def test_render_template_disabled(
    app: Flask, view: Callable[[], ResponseReturnValue]
) -> None:
    """Test render_template logging disabled."""
    app.config['STATSD_RENDERTEMPLATE_LOG'] = False
    Statsd(app)
    with (
        patch('statsd.StatsClient.incr') as mock_incr,
        patch('statsd.StatsClient.timing') as mock_timing,
        app.app_context(),
    ):
        render_template_string("Test template")
        mock_incr.assert_not_called()
        mock_timing.assert_not_called()


def test_form_success(
    ctx: AppContext, app: Flask, statsd: Statsd, form: forms.Form
) -> None:
    app.config['STATSD_TAGS'] = ','
    with patch('statsd.StatsClient.incr') as mock_incr:
        form.field.data = "test"
        assert form.validate() is True
        mock_incr.assert_called_once_with(
            'flask_app.form_validation_success,form=SimpleForm'
            ',app=baseframe_tests.statsd_test',
            1,
            rate=1,
        )


def test_form_error(ctx, app: Flask, statsd: Statsd, form: forms.Form) -> None:
    app.config['STATSD_TAGS'] = ','
    with patch('statsd.StatsClient.incr') as mock_incr:
        form.field.data = None
        assert form.validate() is False
        mock_incr.assert_called_once_with(
            'flask_app.form_validation_error,form=SimpleForm,field=field'
            ',app=baseframe_tests.statsd_test',
            1,
            rate=1,
        )


def test_form_nolog(
    ctx: AppContext, app: Flask, statsd: Statsd, form: forms.Form
) -> None:
    app.config['STATSD_TAGS'] = ','
    app.config['STATSD_FORM_LOG'] = False
    with patch('statsd.StatsClient.incr') as mock_incr:
        form.field.data = 'test'
        assert form.validate() is True
        mock_incr.assert_not_called()
        form.field.data = False
        assert form.validate() is False
        mock_incr.assert_not_called()


def test_form_signals_off(
    ctx: AppContext, app: Flask, statsd: Statsd, form: forms.Form
) -> None:
    app.config['STATSD_TAGS'] = ','
    app.config['STATSD_FORM_LOG'] = True
    with patch('statsd.StatsClient.incr') as mock_incr:
        form.field.data = 'test'
        assert form.validate(send_signals=False) is True
        mock_incr.assert_not_called()
        form.field.data = False
        assert form.validate(send_signals=False) is False
        mock_incr.assert_not_called()
