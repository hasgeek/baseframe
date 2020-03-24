# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta

from baseframe import filters, forms
from coaster.utils import md5sum, utcnow

from .fixtures import TestCaseBaseframe, UserTest


class TestDatetimeFilters(TestCaseBaseframe):
    def setUp(self):
        super(TestDatetimeFilters, self).setUp()
        self.now = utcnow()
        self.today = date.today()

    def test_age(self):
        age = filters.age(self.now)
        self.assertEqual(age, u'now')

        nine_seconds = self.now - timedelta(seconds=9)
        age = filters.age(nine_seconds)
        self.assertEqual(age, u'seconds ago')

        thirty_minutes = self.now - timedelta(minutes=30)
        age = filters.age(thirty_minutes)
        self.assertEqual(age, u'30 minutes ago')

        one_half_hour = self.now - timedelta(hours=1.5)
        age = filters.age(one_half_hour)
        self.assertEqual(age, u'an hour ago')

        ten_months = self.now - timedelta(days=10 * 30)
        age = filters.age(ten_months)
        self.assertEqual(age, u'10 months ago')

        three_years = self.now - timedelta(days=3 * 12 * 30)
        age = filters.age(three_years)
        self.assertEqual(age, u'2 years ago')

    def test_shortdate_date_with_threshold(self):
        self.app.config['SHORTDATE_THRESHOLD_DAYS'] = 10
        testdate = self.now.date() - timedelta(days=5)
        with self.app.test_request_context('/'):
            assert filters.shortdate(testdate) == testdate.strftime('%e %b')

    def test_shortdate_date_without_threshold(self):
        self.app.config['SHORTDATE_THRESHOLD_DAYS'] = 0
        testdate = self.now.date() - timedelta(days=5)
        with self.app.test_request_context('/'):
            assert filters.shortdate(testdate).replace(u"’", u"'") == testdate.strftime(
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
            assert filters.shortdate(testdate).replace(u"’", u"'") == testdate.strftime(
                "%e %b '%y"
            )

    def test_shortdate_datetime_with_tz(self):
        testdate = self.now
        with self.app.test_request_context('/'):
            assert filters.shortdate(testdate).replace(u"’", u"'") == testdate.strftime(
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
        testdate = self.today
        testdate_string = self.today.strftime('%Y-%m-%d')
        with self.app.test_request_context('/'):
            assert filters.date_filter(testdate, 'yyyy-MM-dd', usertz=False) == testdate_string


class TestNaiveDatetimeFilters(TestDatetimeFilters):
    def setUp(self):
        super(TestNaiveDatetimeFilters, self).setUp()
        self.now = datetime.utcnow()

    def test_now_is_naive(self):
        assert self.now.tzinfo is None


class TestFilters(TestCaseBaseframe):
    def setUp(self):
        super(TestFilters, self).setUp()
        self.test_user = UserTest()
        self.test_avatar_size = ('100', '100')
        self.test_avatar_url = u'//images.hasgeek.com/embed/test'

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
        # test_user object doesn't have an email or an avatar by default
        avatar_url = filters.avatar_url(self.test_user)
        self.assertEqual(
            avatar_url,
            u'//www.gravatar.com/avatar/00000000000000000000000000000000?d=mm',
        )

        # testing what if the user has an avatar already
        self.test_user.set_avatar(self.test_avatar_url)
        avatar_url = filters.avatar_url(self.test_user, self.test_avatar_size)
        self.assertEqual(
            avatar_url,
            self.test_avatar_url + '?size=' + u'x'.join(self.test_avatar_size),
        )

        # what if the user doesn't have an avatar but has an email
        self.test_user.set_avatar(None)
        self.test_user.set_email('foobar@foo.com')
        avatar_url = filters.avatar_url(self.test_user, self.test_avatar_size)
        ehash = md5sum(self.test_user.email)
        self.assertEqual(
            avatar_url,
            u'//www.gravatar.com/avatar/'
            + ehash
            + u'?d=mm&s='
            + u'x'.join(self.test_avatar_size),
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
