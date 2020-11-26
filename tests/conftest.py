import pytest

from .fixtures import app1 as app


@pytest.fixture(scope='module')
def test_client():
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client
    ctx.pop()
