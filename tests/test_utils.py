# -*- coding: utf-8 -*-

from baseframe import _localized_country_list_inner, localized_country_list
from .fixtures import app1 as app, TestCaseBaseframe


@app.route('/')
def hello_world():
    country_list = localized_country_list()
    return dict(country_list)['DE']


class TestUtils(TestCaseBaseframe):
    def test_localized_country_list(self):
        countries = _localized_country_list_inner('en')
        assert dict(countries)['DE'] == u"Germany"
        countries = _localized_country_list_inner('de')
        assert dict(countries)['DE'] == u"Deutschland"
        countries = _localized_country_list_inner('es')
        assert dict(countries)['DE'] == u"Alemania"
        countries = _localized_country_list_inner('hi')
        assert dict(countries)['DE'] == u"जर्मनी"

    def test_localized_country_inrequest(self):
        with app.test_client() as c:
            rv = c.get('/', headers={'Accept-Language': 'en;q=0.8, *;q=0.5'})
            assert rv.data.decode('utf-8') == u"Germany"

        with app.test_client() as c:
            rv = c.get('/', headers={'Accept-Language': 'de;q=0.9, en;q=0.8, *;q=0.5'})
            assert rv.data.decode('utf-8') == u"Deutschland"

        with app.test_client() as c:
            rv = c.get('/', headers={'Accept-Language': 'es;q=0.9, en;q=0.8, *;q=0.5'})
            assert rv.data.decode('utf-8') == u"Alemania"

        with app.test_client() as c:
            rv = c.get('/', headers={'Accept-Language': 'hi;q=0.9, en;q=0.8, *;q=0.5'})
            assert rv.data.decode('utf-8') == u"जर्मनी"

    def test_localized_country_order(self):
        """
        Ordering is done by name. So even though index(DE) < index(DZ),
        the order will vary because of their localized names.
        """
        countries = _localized_country_list_inner('en')
        assert dict(countries)['DE'] == u"Germany"
        assert dict(countries)['DZ'] == u"Algeria"
        # index(DE) < index(DZ), but index(Germany) > index(Algeria)
        assert countries.index((u'DE', u'Germany')) > countries.index((u'DZ', u'Algeria'))

        countries = _localized_country_list_inner('de')
        assert dict(countries)['DE'] == u"Deutschland"
        assert dict(countries)['DZ'] == u"Algerien"
        # index(DE) < index(DZ), but index(Deutschland) > index(Algerien)
        assert countries.index((u'DE', u'Deutschland')) > countries.index((u'DZ', u'Algerien'))

        countries = _localized_country_list_inner('es')
        assert dict(countries)['DE'] == u"Alemania"
        assert dict(countries)['DZ'] == u"Algeria"
        # index(DE) < index(DZ), and index(Alemania) < index(Algeria)
        assert countries.index((u'DE', u'Alemania')) < countries.index((u'DZ', u'Algeria'))

        countries = _localized_country_list_inner('hi')
        assert dict(countries)['DE'] == u"जर्मनी"
        assert dict(countries)['DZ'] == u"अल्जीरिया"
        # index(DE) < index(DZ), but index(जर्मनी) > index(अल्जीरिया)
        assert countries.index((u'DE', u'जर्मनी')) > countries.index((u'DZ', u'अल्जीरिया'))
