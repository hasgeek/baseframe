# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import date, datetime, time, timedelta

from pytz import UTC, timezone

from baseframe import filters, forms
from coaster.utils import md5sum

from .fixtures import TestCaseBaseframe, UserTest


class TestDatetimeFilters(TestCaseBaseframe):
    def setUp(self):
        super(TestDatetimeFilters, self).setUp()
        self.now = datetime.now(UTC)
        self.date = date(2020, 1, 31)
        self.datetime = datetime(2020, 1, 31, 0, 0, tzinfo=timezone("UTC"))
        self.time = time(23, 59, 59)
        self.datetimeEST = datetime(
            2020, 1, 31, 0, 0, tzinfo=timezone("America/New_York")
        )

    def test_age(self):
        age = filters.age(self.now)
        self.assertEqual(age, 'now')

        nine_seconds = self.now - timedelta(seconds=9)
        age = filters.age(nine_seconds)
        self.assertEqual(age, 'seconds ago')

        thirty_minutes = self.now - timedelta(minutes=30)
        age = filters.age(thirty_minutes)
        self.assertEqual(age, '30 minutes ago')

        one_half_hour = self.now - timedelta(hours=1.5)
        age = filters.age(one_half_hour)
        self.assertEqual(age, 'an hour ago')

        ten_months = self.now - timedelta(days=10 * 30)
        age = filters.age(ten_months)
        self.assertEqual(age, '10 months ago')

        three_years = self.now - timedelta(days=3 * 12 * 30)
        age = filters.age(three_years)
        self.assertEqual(age, '2 years ago')

    def test_shortdate_date_with_threshold(self):
        self.app.config['SHORTDATE_THRESHOLD_DAYS'] = 10
        testdate = self.now.date() - timedelta(days=5)
        with self.app.test_request_context('/'):
            assert filters.shortdate(testdate) == testdate.strftime('%e %b')

    def test_shortdate_date_without_threshold(self):
        self.app.config['SHORTDATE_THRESHOLD_DAYS'] = 0
        testdate = self.now.date() - timedelta(days=5)
        with self.app.test_request_context('/'):
            assert filters.shortdate(testdate).replace("’", "'") == testdate.strftime(
                "%e %b '%y"
            )

    def test_shortdate_datetime_with_threshold(self):
        self.app.config['SHORTDATE_THRESHOLD_DAYS'] = 10
        testdate = self.now - timedelta(days=5)
        with self.app.test_request_context('/'):
            assert filters.shortdate(testdate) == testdate.strftime('%e %b')

    def test_shortdate_datetime_without_threshold(self):
        testdate = self.now - timedelta(days=5)
        with self.app.test_request_context('/'):
            assert filters.shortdate(testdate).replace("’", "'") == testdate.strftime(
                "%e %b '%y"
            )

    def test_shortdate_datetime_with_tz(self):
        testdate = self.now
        with self.app.test_request_context('/'):
            assert filters.shortdate(testdate).replace("’", "'") == testdate.strftime(
                "%e %b '%y"
            )

    def test_longdate_date(self):
        testdate = self.now.date()
        with self.app.test_request_context('/'):
            assert filters.longdate(testdate) == testdate.strftime('%e %B %Y')

    def test_longdate_datetime(self):
        testdate = self.now
        with self.app.test_request_context('/'):
            assert filters.longdate(testdate) == testdate.strftime('%e %B %Y')

    def test_longdate_datetime_with_tz(self):
        testdate = self.now
        with self.app.test_request_context('/'):
            assert filters.longdate(testdate) == testdate.strftime('%e %B %Y')

    def test_date_filter(self):
        with self.app.test_request_context('/'):
            assert (
                filters.date_filter(self.date, 'yyyy-MM-dd', usertz=False)
                == '2020-01-31'
            )

    def test_date_localized_short_hi(self):
        with self.app.test_request_context('/', headers={'Accept-Language': 'hi'}):
            assert filters.date_filter(self.date, format='short') == '31/1/20'

    def test_date_localized_medium_hi(self):
        with self.app.test_request_context('/', headers={'Accept-Language': 'hi'}):
            assert filters.date_filter(self.date, format='medium') == '31 जन॰ 2020'

    def test_date_localized_long_hi(self):
        with self.app.test_request_context('/', headers={'Accept-Language': 'hi'}):
            assert filters.date_filter(self.date, format='long') == '31 जनवरी 2020'

    def test_time_localized_hi_medium(self):
        with self.app.test_request_context('/', headers={'Accept-Language': 'hi'}):
            assert (
                filters.datetime_filter(self.datetime, format='medium')
                == '31 जन॰ 2020, 12:00:00 am'
            )

    def test_month_localized_hi(self):
        with self.app.test_request_context('/', headers={'Accept-Language': 'hi'}):
            assert filters.date_filter(self.date, "MMMM") == 'जनवरी'

    def test_month_localized_en(self):
        with self.app.test_request_context('/'):
            assert filters.date_filter(self.date, "MMMM") == 'January'

    def test_time_localized_short(self):
        with self.app.test_request_context('/', headers={'Accept-Language': 'hi'}):
            assert filters.time_filter(self.datetime, format='short') == '12:00 am'

    def test_time_localized_medium(self):
        with self.app.test_request_context('/', headers={'Accept-Language': 'hi'}):
            assert filters.time_filter(self.datetime, format='medium') == '12:00:00 am'

    def test_time_localized_long(self):
        with self.app.test_request_context('/', headers={'Accept-Language': 'hi'}):
            assert (
                filters.time_filter(self.datetime, format='long') == '12:00:00 am UTC'
            )

    def test_time_localized_hi_full(self):
        with self.app.test_request_context('/', headers={'Accept-Language': 'hi'}):
            assert (
                filters.time_filter(self.time, format='full')
                == '11:59:59 pm समन्वित वैश्विक समय'
            )

    def test_time_localized_en_full(self):
        with self.app.test_request_context('/', headers={'Accept-Language': 'en'}):
            assert (
                filters.time_filter(self.time, format='full')
                == '11:59:59 PM Coordinated Universal Time'
            )

    def test_datetime_with_usertz(self):
        with self.app.test_request_context('/'):
            assert (
                filters.datetime_filter(self.datetimeEST, format='full', usertz=False)
                == 'Friday, January 31, 2020 at 12:00:00 AM Eastern Standard Time'
            )

    def test_datetime_without_usertz(self):
        with self.app.test_request_context('/'):
            assert (
                filters.datetime_filter(self.datetimeEST, format='full', usertz=True)
                == 'Friday, January 31, 2020 at 4:56:00 AM Coordinated Universal Time'
            )

    def test_date_dmy(self):
        with self.app.test_request_context('/'):
            assert (
                filters.date_filter(self.datetime, format='short', locale='en_GB')
                == '31/01/2020'
            )

    def test_date_mdy(self):
        with self.app.test_request_context('/'):
            assert (
                filters.date_filter(self.datetime, format='short', locale='en_US')
                == '1/31/20'
            )


class TestNaiveDatetimeFilters(TestDatetimeFilters):
    def setUp(self):
        super(TestNaiveDatetimeFilters, self).setUp()
        self.now = datetime.utcnow()

    def test_now_is_naive(self):
        assert self.now.tzinfo is None


class TestFilters(TestCaseBaseframe):
    def setUp(self):
        super(TestFilters, self).setUp()
        self.user = UserTest()
        self.avatar_size = ('100', '100')
        self.avatar_url = '//images.hasgeek.com/embed/test'

    def test_initials(self):
        initial = filters.initials('A Named Example')
        self.assertEqual(initial, 'AE')

        initial = filters.initials('A Slightly Longer Named Example')
        self.assertEqual(initial, 'AE')

        initial = filters.initials(' Abnormally  Spaced Example ')
        self.assertEqual(initial, 'AE')

        initial = filters.initials('Example')
        self.assertEqual(initial, 'E')

        initial = filters.initials('एक एक्साम्पल')
        self.assertEqual(initial, 'एए')

        initial = filters.initials(' ')
        self.assertEqual(initial, '')

        initial = filters.initials('')
        self.assertEqual(initial, '')

        initial = filters.initials(None)
        self.assertEqual(initial, '')

    def test_usessl(self):
        with self.app.test_request_context('/'):
            self.app.config['USE_SSL'] = False
            ssled = filters.usessl('http://hasgeek.com')
            self.assertEqual(ssled, 'http://hasgeek.com')

            self.app.config['USE_SSL'] = True
            ssled = filters.usessl('http://hasgeek.com')
            self.assertEqual(ssled, 'https://hasgeek.com')

            ssled = filters.usessl('hasgeek.com')
            self.assertEqual(ssled, 'hasgeek.com')

            ssled = filters.usessl('/static/test')
            self.assertEqual(ssled, 'https://localhost/static/test')

    def test_nossl(self):
        with self.app.test_request_context('/'):
            nossled = filters.nossl('https://hasgeek.com')
            self.assertEqual(nossled, 'http://hasgeek.com')

            nossled = filters.nossl('hasgeek.com')
            self.assertEqual(nossled, 'hasgeek.com')

            nossled = filters.nossl('//hasgeek.com')
            self.assertEqual(nossled, 'http://hasgeek.com')

    def test_avatar_url(self):
        # user object doesn't have an email or an avatar by default
        avatar_url = filters.avatar_url(self.user)
        self.assertEqual(
            avatar_url,
            '//www.gravatar.com/avatar/00000000000000000000000000000000?d=mm',
        )

        # testing what if the user has an avatar already
        self.user.set_avatar(self.avatar_url)
        avatar_url = filters.avatar_url(self.user, self.avatar_size)
        self.assertEqual(
            avatar_url, self.avatar_url + '?size=' + 'x'.join(self.avatar_size)
        )

        # what if the user doesn't have an avatar but has an email
        self.user.set_avatar(None)
        self.user.set_email('foobar@foo.com')
        avatar_url = filters.avatar_url(self.user, self.avatar_size)
        ehash = md5sum(self.user.email)
        self.assertEqual(
            avatar_url,
            '//www.gravatar.com/avatar/'
            + ehash
            + '?d=mm&s='
            + 'x'.join(self.avatar_size),
        )

    def test_render_field_options(self):
        test_attrs = {
            'attrone': 'test',
            'attrtwo': False,
            'attrthree': None,
            'attrfour': '',
        }
        modified_field = filters.render_field_options(forms.RichTextField, **test_attrs)
        self.assertIn('attrone', modified_field.kwargs) and self.assertEqual(
            modified_field.kwargs['attrone'], 'test'
        )
        assert not hasattr(modified_field.kwargs, 'attrtwo')
        assert not hasattr(modified_field.kwargs, 'attrthree')
        self.assertIn('attrfour', modified_field.kwargs) and self.assertEqual(
            modified_field.kwargs['attrfour'], ''
        )

    def test_firstline(self):
        html = "<div>this is the first line</div><div>and second line</div>"
        firstline = filters.firstline(html)
        self.assertEqual(firstline, "this is the first line")

    def test_cdata(self):
        text = "foo bar"
        result = filters.cdata(text)
        self.assertEqual(result, "<![CDATA[foo bar]]>")

        text = "<![CDATA[foo bar]]>"
        result = filters.cdata(text)
        self.assertEqual(result, "<![CDATA[<![CDATA[foo bar]]]]><![CDATA[>]]>")

    def test_lower(self):
        lower_func = forms.lower()
        self.assertEqual(lower_func('TEST'), 'test')
        self.assertEqual(lower_func('Test'), 'test')
        self.assertEqual(lower_func(''), '')

    def test_upper(self):
        upper_func = forms.upper()
        self.assertEqual(upper_func('Test'), 'TEST')
        self.assertEqual(upper_func('test'), 'TEST')
        self.assertEqual(upper_func(''), '')

    def test_strip(self):
        strip_func = forms.strip()
        self.assertEqual(strip_func(' Test '), 'Test')
        self.assertEqual(strip_func('a       test   '), 'a       test')
        self.assertEqual(strip_func('      '), '')

    def test_lstrip(self):
        lstrip_func = forms.lstrip()
        self.assertEqual(lstrip_func(' Test '), 'Test ')
        self.assertEqual(lstrip_func('a       test   '), 'a       test   ')
        self.assertEqual(lstrip_func('      '), '')

    def test_rstrip(self):
        rstrip_func = forms.rstrip()
        self.assertEqual(rstrip_func(' Test '), ' Test')
        self.assertEqual(rstrip_func('a       test   '), 'a       test')
        self.assertEqual(rstrip_func('      '), '')

    def test_strip_each(self):
        strip_each_func = forms.strip_each()
        assert strip_each_func(None) is None
        assert strip_each_func([]) == []
        assert strip_each_func(
            [' Left strip', 'Right strip ', ' Full strip ', '', 'No strip', '']
        ) == ['Left strip', 'Right strip', 'Full strip', 'No strip']

    def test_none_if_empty(self):
        none_if_empty_func = forms.none_if_empty()
        assert none_if_empty_func('Test') == 'Test'
        assert none_if_empty_func('') is None
        assert none_if_empty_func([]) is None
        assert none_if_empty_func(False) is None
        assert none_if_empty_func(0) is None
