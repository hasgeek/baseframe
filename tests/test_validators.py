from .fixtures import BaseframeTestCase, TestUrlForm, TestAllUrlsForm, TestOptionalIfForm, TestOptionalIfNotForm


class ValidatorTestCase(BaseframeTestCase):
    def setUp(self):
        super(ValidatorTestCase, self).setUp()
        with self.app.test_request_context('/'):
            self.form = TestUrlForm(csrf_enabled=False)
            self.all_urls_form = TestAllUrlsForm(csrf_enabled=False)
            self.optional_if_form = TestOptionalIfForm(csrf_enabled=False)
            self.optional_if_not_form = TestOptionalIfNotForm(csrf_enabled=False)

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
