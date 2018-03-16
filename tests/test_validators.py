# -*- coding: utf-8 -*-

import warnings
import urllib3
from .fixtures import TestCaseBaseframe, UrlFormTest, AllUrlsFormTest, OptionalIfFormTest, OptionalIfNotFormTest, PublicEmailDomainTest


class TestValidators(TestCaseBaseframe):
    def setUp(self):
        super(TestValidators, self).setUp()
        with self.app.test_request_context('/'):
            self.form = UrlFormTest(meta={'csrf': False})
            self.all_urls_form = AllUrlsFormTest(meta={'csrf': False})
            self.optional_if_form = OptionalIfFormTest(meta={'csrf': False})
            self.optional_if_not_form = OptionalIfNotFormTest(meta={'csrf': False})
            self.webmail_form = PublicEmailDomainTest(meta={'csrf': False})
        urllib3.disable_warnings()

    def tearDown(self):
        super(TestValidators, self).tearDown()
        warnings.resetwarnings()

    def test_valid_url(self):
        with self.app.test_request_context('/'):
            url = 'https://hasgeek.com/'
            self.form.process(url=url)
            self.assertEqual(self.form.validate(), True)

    def test_invalid_url(self):
        with self.app.test_request_context('/'):
            url = 'https://hasgeek'
            self.form.process(url=url)
            self.assertEqual(self.form.validate(), False)

    def test_public_email_domain(self):
        with self.app.test_request_context('/'):
            # both valid
            self.webmail_form.process(
                webmail_domain='gmail.com',
                not_webmail_domain='foobar.com'
            )
            self.assertTrue(self.webmail_form.validate())

            # Emoji domain, should not raise any exception
            self.webmail_form.process(
                webmail_domain='gmail.com',
                not_webmail_domain='i❤.ws'
            )
            self.assertTrue(self.webmail_form.validate())

            # both invalid
            self.webmail_form.process(
                webmail_domain='foobar.com',
                not_webmail_domain='yahoo.com'
            )
            self.assertFalse(self.webmail_form.validate())
            self.assertIn('webmail_domain', self.webmail_form.errors)
            self.assertIn('not_webmail_domain', self.webmail_form.errors)

            # one valid, one invalid
            self.webmail_form.process(
                webmail_domain='gmail.com',
                not_webmail_domain='yahoo.com'
            )
            self.assertFalse(self.webmail_form.validate())
            self.assertNotIn('webmail_domain', self.webmail_form.errors)
            self.assertIn('not_webmail_domain', self.webmail_form.errors)

            # these domain names don't exist, MX lookup will fail
            # So, webmail_domain should fail, but not_webmail_domain should pass
            self.webmail_form.process(
                webmail_domain='9vGw1TMChQWH.com',
                not_webmail_domain='9vGw1TMChQWH.com'
            )
            self.assertFalse(self.webmail_form.validate())
            self.assertIn('webmail_domain', self.webmail_form.errors)
            self.assertNotIn('not_webmail_domain', self.webmail_form.errors)

    def test_url_without_protocol(self):
        with self.app.test_request_context('/'):
            url = 'hasgeek.com'
            self.form.process(url=url)
            self.assertEqual(self.form.validate(), False)

    def test_inaccessible_url(self):
        with self.app.test_request_context('/'):
            url = 'http://4dc1f6f0e7bc44f2b5b44f00abea4eae.com/'
            self.form.process(url=url)
            self.assertEqual(self.form.validate(), False)

    def test_disallowed_url(self):
        with self.app.test_request_context('/'):
            url = 'https://example.com/'
            self.form.process(url=url)
            self.assertEqual(self.form.validate(), False)
            url = 'https://example.in/'
            self.form.process(url=url)
            self.assertEqual(self.form.validate(), False)

    def test_html_snippet_valid_urls(self):
        url1 = 'https://hasgeek.com/'
        url2 = 'https://hasjob.co/'
        with self.app.test_request_context('/'):
            snippet = '<ul><li><a href="{url1}">url1</a></li><li><a href="{url2}">url2</a></li></ul>'.format(url1=url1, url2=url2)
            self.all_urls_form.process(content_with_urls=snippet)
            self.assertEqual(self.all_urls_form.validate(), True)

    def test_html_snippet_invalid_urls(self):
        url1 = 'https://hasgeek.com/'
        url2 = 'https://hasjob'
        with self.app.test_request_context('/'):
            snippet = '<ul><li><a href="{url1}">url1</a></li><li><a href="{url2}">url2</a></li></ul>'.format(url1=url1, url2=url2)
            self.all_urls_form.process(content_with_urls=snippet)
            self.assertEqual(self.all_urls_form.validate(), False)

    def test_optional_if(self):
        self.optional_if_form.process(headline=u'Headline')
        self.assertTrue(self.optional_if_form.validate())

        self.optional_if_form.process()
        self.assertFalse(self.optional_if_form.validate())

    def test_optional_if_not(self):
        self.optional_if_not_form.process()
        self.assertTrue(self.optional_if_not_form.validate())

        self.optional_if_not_form.process(content=u'Content')
        self.assertFalse(self.optional_if_not_form.validate())
