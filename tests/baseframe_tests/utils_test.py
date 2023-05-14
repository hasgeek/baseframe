"""Test utils."""
# pylint: disable=redefined-outer-name

import pytest

from baseframe.utils import (
    _localized_country_list_inner,
    localized_country_list,
    request_checked_xhr,
    request_is_xhr,
)

# --- Fixtures -------------------------------------------------------------------------


@pytest.fixture()
def testview(app):
    """Add a view to the app for testing."""

    @app.route('/localetest')
    def locale_testview():
        country_list = localized_country_list()
        return dict(country_list)['DE']

    return locale_testview


# --- Tests ----------------------------------------------------------------------------


@pytest.mark.usefixtures('app')  # localized country list needs cache
def test_localized_country_list():
    countries = _localized_country_list_inner('en')
    assert dict(countries)['DE'] == "Germany"
    countries = _localized_country_list_inner('hi')
    assert dict(countries)['DE'] == "जर्मनी"


@pytest.mark.usefixtures('testview')
def test_localized_country_inrequest(client):
    rv = client.get('/localetest', headers={'Accept-Language': 'en;q=0.8, *;q=0.5'})
    assert rv.data.decode('utf-8') == "Germany"

    rv = client.get(
        '/localetest',
        headers={'Accept-Language': 'hi;q=0.9, en;q=0.8, *;q=0.5'},
    )
    assert rv.data.decode('utf-8') == "जर्मनी"


def test_localized_country_order():
    # Ordering is done by name. So even though index(DE) < index(DZ),
    # the order will vary because of their localized names.
    countries = _localized_country_list_inner('en')
    assert dict(countries)['DE'] == "Germany"
    assert dict(countries)['DZ'] == "Algeria"
    # index(DE) < index(DZ), but index(Germany) > index(Algeria)
    assert countries.index(('DE', 'Germany')) > countries.index(('DZ', 'Algeria'))

    countries = _localized_country_list_inner('de')
    assert dict(countries)['DE'] == "Deutschland"
    assert dict(countries)['DZ'] == "Algerien"
    # index(DE) < index(DZ), but index(Deutschland) > index(Algerien)
    assert countries.index(('DE', 'Deutschland')) > countries.index(('DZ', 'Algerien'))

    countries = _localized_country_list_inner('es')
    assert dict(countries)['DE'] == "Alemania"
    assert dict(countries)['DZ'] == "Algeria"
    # index(DE) < index(DZ), and index(Alemania) < index(Algeria)
    assert countries.index(('DE', 'Alemania')) < countries.index(('DZ', 'Algeria'))

    countries = _localized_country_list_inner('hi')
    assert dict(countries)['DE'] == "जर्मनी"
    assert dict(countries)['DZ'] == "अल्जीरिया"
    # index(DE) < index(DZ), but index(जर्मनी) > index(अल्जीरिया)
    assert countries.index(('DE', 'जर्मनी')) > countries.index(('DZ', 'अल्जीरिया'))


def test_request_has_xhr(app):
    """Verify request_checked_xhr() returns True if request_is_xhr() was called."""
    with app.test_request_context():
        assert request_checked_xhr() is False
        request_is_xhr()
        assert request_checked_xhr() is True

    with app.test_request_context():
        assert request_checked_xhr() is False
