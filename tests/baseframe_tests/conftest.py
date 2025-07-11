"""Test configuration."""
# pylint: disable=redefined-outer-name

from collections.abc import Generator

import pytest
from flask import Flask
from flask.ctx import AppContext
from flask.testing import FlaskClient

from baseframe import baseframe


@pytest.fixture
def app() -> Flask:
    """App fixture."""
    fixture_app = Flask(__name__)
    fixture_app.config['CACHE_TYPE'] = 'SimpleCache'
    fixture_app.config['SECRET_KEY'] = 'test secret'  # nosec: B105  # noqa: S105
    baseframe.init_app(fixture_app, requires=['baseframe'])
    return fixture_app


@pytest.fixture
def ctx(app: Flask) -> Generator[AppContext, None, None]:
    with app.app_context() as context:
        yield context


@pytest.fixture
def client(app: Flask) -> Generator[FlaskClient, None, None]:
    """App client fixture."""
    with app.test_client() as test_client:
        yield test_client
