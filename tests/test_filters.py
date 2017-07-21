from datetime import datetime, timedelta

from coaster.utils import md5sum
from baseframe import filters, forms
from .fixtures import BaseframeTestCase, TestUser, TestForm


class FilterTestCase(BaseframeTestCase):
    def setUp(self):
        super(FilterTestCase, self).setUp()
        self.now = datetime.utcnow()
        self.test_user = TestUser()
        self.test_avatar_size = ('100', '100')
        self.test_avatar_url = u'//images.hasgeek.com/embed/test'

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
        self.assertEqual(avatar_url, u'//www.gravatar.com/avatar/00000000000000000000000000000000?d=mm')

        # testing what if the user has an avatar already
        self.test_user.set_avatar(self.test_avatar_url)
        avatar_url = filters.avatar_url(self.test_user, self.test_avatar_size)
        self.assertEqual(avatar_url, self.test_avatar_url + '?size=' + u'x'.join(self.test_avatar_size))

        # what if the user doesn't have an avatar but has an email
        self.test_user.set_avatar(None)
        self.test_user.set_email('foobar@foo.com')
        avatar_url = filters.avatar_url(self.test_user, self.test_avatar_size)
        hash = md5sum(self.test_user.email)
        self.assertEqual(avatar_url, u'//www.gravatar.com/avatar/' + hash + u'?d=mm&s=' + u'x'.join(self.test_avatar_size))

    def test_render_field_options(self):
        test_attrs = dict(attrone='test', attrtwo=False, attrthree=None, attrfour='')
        modified_field = filters.render_field_options(forms.RichTextField, **test_attrs)
        assert 'attrone' in modified_field.kwargs and modified_field.kwargs['attrone'] == 'test'
        assert not hasattr(modified_field.kwargs, 'attrtwo')
        assert not hasattr(modified_field.kwargs, 'attrthree')
        assert 'attrfour' in modified_field.kwargs and modified_field.kwargs['attrfour'] == ''

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
