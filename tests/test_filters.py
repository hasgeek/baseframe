from datetime import datetime, timedelta

from baseframe import filters
from .fixtures import BaseframeTestCase, TestUser


class FilterTestCase(BaseframeTestCase):
    def setUp(self):
        super(FilterTestCase, self).setUp()
        self.now = datetime.utcnow()
        self.test_user = TestUser()
        self.test_avatar_size = ('100', '100')
        self.test_avatar_url = u'//www.gravatar.com/avatar/test'

    def tearDown(self):
        super(FilterTestCase, self).tearDown()

    def test_age(self):
        age = filters.age(self.now)
        self.assertEqual(age, u'now')

        nine_seconds = self.now - timedelta(seconds=9)
        age = filters.age(nine_seconds)
        self.assertEqual(age, u'seconds ago')

        one_half_hour = self.now - timedelta(hours=1.5)
        age = filters.age(one_half_hour)
        self.assertEqual(age, u'an hour ago')

        ten_months = self.now - timedelta(days=10*30)
        age = filters.age(ten_months)
        self.assertEqual(age, u'10 months ago')

        three_years = self.now - timedelta(days=3*12*30)
        age = filters.age(three_years)
        self.assertEqual(age, u'2 years ago')

    def test_usessl(self):
        with self.app.test_request_context('/'):
            self.app.config['USE_SSL'] = False
            ssled = filters.usessl('http://hasgeek.com')
            self.assertEqual(ssled, 'http://hasgeek.com')

            self.app.config['USE_SSL'] = True
            ssled = filters.usessl('http://hasgeek.com')
            self.assertEqual(ssled, 'https://hasgeek.com')

    def test_nossl(self):
        nossled = filters.nossl('https://hasgeek.com')
        self.assertEqual(nossled, 'http://hasgeek.com')

    def test_avatar_url(self):
        avatar_url = filters.avatar_url(self.test_user)
        self.assertEqual(avatar_url, u'//www.gravatar.com/avatar/00000000000000000000000000000000?d=mm')

        self.test_user.set_avatar(self.test_avatar_url)
        avatar_url = filters.avatar_url(self.test_user, self.test_avatar_size)
        self.assertEqual(avatar_url, self.test_avatar_url + '?size=' + u'x'.join(self.test_avatar_size))
