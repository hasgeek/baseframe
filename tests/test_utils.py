# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from baseframe import _localized_country_list_inner, localized_country_list

from .fixtures import TestCaseBaseframe
from .fixtures import app1 as app


@app.route('/localetest')
def locale_testview():
    country_list = localized_country_list()
    return dict(country_list)['DE']


class TestUtils(TestCaseBaseframe):
    def test_localized_country_list(self):
        countries = _localized_country_list_inner('en')
        assert dict(countries)['DE'] == "Germany"
        countries = _localized_country_list_inner('hi')
        assert dict(countries)['DE'] == "जर्मनी"

    def test_localized_country_inrequest(self):
        with app.test_client() as c:
            rv = c.get('/localetest', headers={'Accept-Language': 'en;q=0.8, *;q=0.5'})
            assert rv.data.decode('utf-8') == "Germany"

        with app.test_client() as c:
            rv = c.get(
                '/localetest',
                headers={'Accept-Language': 'hi;q=0.9, en;q=0.8, *;q=0.5'},
            )
            assert rv.data.decode('utf-8') == "जर्मनी"

    def test_localized_country_order(self):
        """
        Ordering is done by name. So even though index(DE) < index(DZ),
        the order will vary because of their localized names.
        """
        countries = _localized_country_list_inner('en')
        assert dict(countries)['DE'] == "Germany"
        assert dict(countries)['DZ'] == "Algeria"
        # index(DE) < index(DZ), but index(Germany) > index(Algeria)
        assert countries.index(('DE', 'Germany')) > countries.index(('DZ', 'Algeria'))

        countries = _localized_country_list_inner('de')
        assert dict(countries)['DE'] == "Deutschland"
        assert dict(countries)['DZ'] == "Algerien"
        # index(DE) < index(DZ), but index(Deutschland) > index(Algerien)
        assert countries.index(('DE', 'Deutschland')) > countries.index(
            ('DZ', 'Algerien')
        )

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
