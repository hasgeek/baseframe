# -*- coding: utf-8 -*-

from baseframe import _localized_country_list_inner
from .fixtures import TestCaseBaseframe


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
