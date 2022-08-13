"""Test configuration."""
from flask import Flask

import pytest

from baseframe import baseframe


@pytest.fixture()
def app():
    """App fixture."""
    fixture_app = Flask(__name__)
    fixture_app.config['CACHE_TYPE'] = 'SimpleCache'
    fixture_app.config['SECRET_KEY'] = 'test secret'  # nosec
    baseframe.init_app(fixture_app, requires=['baseframe'])
    return fixture_app


@pytest.fixture()
def ctx(app):
    with app.app_context() as context:
        yield context


@pytest.fixture()
def client(app):
    """App client fixture."""
    with app.test_client() as test_client:
        yield test_client
