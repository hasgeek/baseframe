# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import warnings

from werkzeug.datastructures import MultiDict

from mxsniff import MXLookupException
import urllib3

from baseframe import forms
from baseframe.utils import is_public_email_domain

from .fixtures import (
    AllUrlsFormTest,
    EmojiFormTest,
    FormTest,
    PublicEmailDomainFormTest,
    TestCaseBaseframe,
    UrlFormTest,
)


class TestValidators(TestCaseBaseframe):
    def setUp(self):
        super(TestValidators, self).setUp()
        with self.app.test_request_context('/'):
            self.url_form = UrlFormTest(meta={'csrf': False})
            self.emoji_form = EmojiFormTest(meta={'csrf': False})
            self.all_urls_form = AllUrlsFormTest(meta={'csrf': False})
            self.webmail_form = PublicEmailDomainFormTest(meta={'csrf': False})
            self.nonce_form = FormTest(meta={'csrf': False})
        urllib3.disable_warnings()

    def tearDown(self):
        super(TestValidators, self).tearDown()
        warnings.resetwarnings()

    def test_valid_url(self):
        with self.app.test_request_context('/'):
            url = 'https://hasgeek.com/'
            self.url_form.process(url=url)
            assert self.url_form.validate()

    def test_invalid_url(self):
        with self.app.test_request_context('/'):
            url = 'https://hasgeek'
            self.url_form.process(url=url)
            assert not self.url_form.validate()

    def test_valid_emoji(self):
        with self.app.test_request_context('/'):
            dat = '👍'
            self.emoji_form.process(emoji=dat)
            assert self.emoji_form.validate() is True

    def test_invalid_emoji(self):
        with self.app.test_request_context('/'):
            dat = 'eviltext'
            self.emoji_form.process(emoji=dat)
            assert self.emoji_form.validate() is False

    def test_public_email_domain(self):
        with self.app.test_request_context('/'):
            # both valid
            self.webmail_form.process(
                webmail_domain='gmail.com', not_webmail_domain='i❤.ws'
            )
            self.assertTrue(self.webmail_form.validate())

            # both invalid
            self.webmail_form.process(
                webmail_domain='i❤.ws', not_webmail_domain='gmail.com'
            )
            self.assertFalse(self.webmail_form.validate())
            self.assertIn('webmail_domain', self.webmail_form.errors)
            self.assertIn('not_webmail_domain', self.webmail_form.errors)

            # one valid, one invalid
            self.webmail_form.process(
                webmail_domain='gmail.com', not_webmail_domain='gmail.com'
            )
            self.assertFalse(self.webmail_form.validate())
            self.assertNotIn('webmail_domain', self.webmail_form.errors)
            self.assertIn('not_webmail_domain', self.webmail_form.errors)

            # these domain lookups will fail because of the DNS label length limit.
            # (abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijks is 64 characters,
            # the maximum length of a DNS label is 63 characters)
            # ``mxsniff`` will raise ``MXLookupException`` for these domains.
            # So, webmail_domain should fail, and not_webmail_domain should pass.
            self.webmail_form.process(
                webmail_domain='www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijks.com',
                not_webmail_domain='www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijks.com',
            )
            self.assertFalse(self.webmail_form.validate())
            self.assertIn('webmail_domain', self.webmail_form.errors)
            self.assertNotIn('not_webmail_domain', self.webmail_form.errors)

    def test_public_email_domain_helper(self):
        with self.app.test_request_context('/'):
            assert is_public_email_domain('gmail.com', default=False)
            assert not is_public_email_domain('google.com', default=False)

            # Intentionally trigger a DNS lookup failure using an invalid domain name.
            # Since no default is provided, we will receive an exception.
            with self.assertRaises(MXLookupException):
                is_public_email_domain(
                    'www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijks.com'
                )

            # If default value is provided, it'll return default is case of DNS lookup failure.
            assert not is_public_email_domain(
                'www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijks.com',
                default=False,
            )
            assert is_public_email_domain(
                'www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijks.com',
                default=True,
            )

    def test_url_without_protocol(self):
        with self.app.test_request_context('/'):
            url = 'hasgeek.com'
            self.url_form.process(url=url)
            assert not self.url_form.validate()

    def test_inaccessible_url(self):
        with self.app.test_request_context('/'):
            url = 'http://4dc1f6f0e7bc44f2b5b44f00abea4eae.com/'
            self.url_form.process(url=url)
            assert not self.url_form.validate()

    def test_disallowed_url(self):
        with self.app.test_request_context('/'):
            url = 'https://example.com/'
            self.url_form.process(url=url)
            assert not self.url_form.validate()
            url = 'https://example.in/'
            self.url_form.process(url=url)
            assert not self.url_form.validate()

    def test_html_snippet_valid_urls(self):
        url1 = 'https://hasgeek.com/'
        url2 = 'https://hasjob.co/'
        with self.app.test_request_context('/'):
            snippet = '<ul><li><a href="{url1}">url1</a></li><li><a href="{url2}">url2</a></li></ul>'.format(
                url1=url1, url2=url2
            )
            self.all_urls_form.process(content_with_urls=snippet)
            assert self.all_urls_form.validate()

    def test_html_snippet_invalid_urls(self):
        url1 = 'https://hasgeek.com/'
        url2 = 'https://hasjob'
        with self.app.test_request_context('/'):
            snippet = '<ul><li><a href="{url1}">url1</a></li><li><a href="{url2}">url2</a></li></ul>'.format(
                url1=url1, url2=url2
            )
            self.all_urls_form.process(content_with_urls=snippet)
            assert not self.all_urls_form.validate()

    def test_nonce_form_on_success(self):
        """A form with a nonce cannot be submitted twice"""
        formdata = MultiDict({field.name: field.data for field in self.nonce_form})
        nonce = self.nonce_form.form_nonce.data
        assert nonce
        assert self.nonce_form.validate() is True
        # Nonce changes on each submit
        assert nonce != self.nonce_form.form_nonce.data
        assert not self.nonce_form.form_nonce.errors
        # Now restore old form contents
        self.nonce_form.process(formdata=formdata)
        # Second attempt on the same form contents will fail
        assert self.nonce_form.validate() is False
        assert self.nonce_form.form_nonce.errors

    def test_nonce_form_on_failure(self):
        """Form resubmission is not blocked (via the nonce) when validation fails"""
        self.emoji_form.process(
            formdata=MultiDict(
                {'emoji': 'not-emoji', 'form_nonce': self.emoji_form.form_nonce.data}
            )
        )
        assert self.emoji_form.validate() is False
        assert not self.emoji_form.form_nonce.errors
        formdata = MultiDict(
            {'emoji': '👍', 'form_nonce': self.emoji_form.form_nonce.data}
        )
        self.emoji_form.process(formdata=formdata)
        assert self.emoji_form.validate() is True
        assert not self.emoji_form.form_nonce.errors
        # Second attempt on the same form data will fail
        self.emoji_form.process(formdata)
        assert self.emoji_form.validate() is False
        assert self.emoji_form.errors


class TestValidUrl(TestCaseBaseframe):
    """Additional tests for the ValidUrl validator"""

    def setUp(self):
        super(TestValidUrl, self).setUp()
        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_no_schemes(self):
        class UrlForm(forms.Form):
            url = forms.StringField("URL", validators=[forms.validators.ValidUrl()])

        form = UrlForm(meta={'csrf': False})
        form.url.data = 'mailto:example@example.com'
        assert form.validate() is True

    def test_static_schemes(self):
        class UrlForm(forms.Form):
            url = forms.StringField(
                "URL",
                validators=[
                    forms.validators.ValidUrl(allowed_schemes=('http', 'https'))
                ],
            )

        form = UrlForm(meta={'csrf': False})
        form.url.data = 'mailto:example@example.com'
        assert form.validate() is False

    def test_static_schemes_allowed(self):
        class UrlForm(forms.Form):
            url = forms.StringField(
                "URL",
                validators=[
                    forms.validators.ValidUrl(
                        allowed_schemes=('http', 'https', 'mailto')
                    )
                ],
            )

        form = UrlForm(meta={'csrf': False})
        form.url.data = 'mailto:example@example.com'
        assert form.validate() is True

    def test_callable_schemes(self):
        class UrlForm(forms.Form):
            url = forms.StringField(
                "URL",
                validators=[
                    forms.validators.ValidUrl(allowed_schemes=lambda: ('http', 'https'))
                ],
            )

        form = UrlForm(meta={'csrf': False})
        form.url.data = 'mailto:example@example.com'
        assert form.validate() is False

    def test_callable_schemes_allowed(self):
        class UrlForm(forms.Form):
            url = forms.StringField(
                "URL",
                validators=[
                    forms.validators.ValidUrl(
                        allowed_schemes=lambda: ('http', 'https', 'mailto')
                    )
                ],
            )

        form = UrlForm(meta={'csrf': False})
        form.url.data = 'mailto:example@example.com'
        assert form.validate() is True

    def test_no_domains(self):
        class UrlForm(forms.Form):
            url = forms.StringField("URL", validators=[forms.validators.ValidUrl()])

        form = UrlForm(meta={'csrf': False})
        form.url.data = 'http://www.example.com'
        assert form.validate() is True

    def test_static_domains(self):
        class UrlForm(forms.Form):
            url = forms.StringField(
                "URL",
                validators=[
                    forms.validators.ValidUrl(allowed_domains=('example.net',))
                ],
            )

        form = UrlForm(meta={'csrf': False})
        form.url.data = 'http://www.example.com'
        assert form.validate() is False

    def test_static_domains_misconfigured(self):
        """Domains must be exact matches including subdomains"""

        class UrlForm(forms.Form):
            url = forms.StringField(
                "URL",
                validators=[
                    forms.validators.ValidUrl(
                        allowed_domains=('example.net', 'example.com')
                    )
                ],
            )

        form = UrlForm(meta={'csrf': False})
        form.url.data = 'http://www.example.com'
        assert form.validate() is False

    def test_static_domains_allowed(self):
        class UrlForm(forms.Form):
            url = forms.StringField(
                "URL",
                validators=[
                    forms.validators.ValidUrl(
                        allowed_domains=(
                            'example.net',
                            'example.com',
                            'www.example.com',
                        )
                    )
                ],
            )

        form = UrlForm(meta={'csrf': False})
        form.url.data = 'http://www.example.com'
        assert form.validate() is True

    def test_static_domains_case(self):
        class UrlForm(forms.Form):
            url = forms.StringField(
                "URL",
                validators=[
                    forms.validators.ValidUrl(
                        allowed_domains=(
                            'example.net',
                            'example.com',
                            'www.example.com',
                        )
                    )
                ],
            )

        form = UrlForm(meta={'csrf': False})
        form.url.data = 'http://WWW.EXAMPLE.COM'
        assert form.validate() is True

    def test_callable_domains(self):
        class UrlForm(forms.Form):
            url = forms.StringField(
                "URL",
                validators=[
                    forms.validators.ValidUrl(allowed_domains=lambda: ('example.net',))
                ],
            )

        form = UrlForm(meta={'csrf': False})
        form.url.data = 'http://www.example.com'
        assert form.validate() is False

    def test_callable_domains_allowed(self):
        class UrlForm(forms.Form):
            url = forms.StringField(
                "URL",
                validators=[
                    forms.validators.ValidUrl(
                        allowed_domains=lambda: (
                            'example.net',
                            'example.com',
                            'www.example.com',
                        )
                    )
                ],
            )

        form = UrlForm(meta={'csrf': False})
        form.url.data = 'http://www.example.com'
        assert form.validate() is True

    def test_visit_url_true(self):
        class UrlForm(forms.Form):
            url = forms.StringField(
                "URL", validators=[forms.validators.ValidUrl(visit_url=True)]
            )

        form = UrlForm(meta={'csrf': False})
        # Invalid URL will fail a load test
        form.url.data = 'http://localhosta'
        assert form.validate() is False

    def test_visit_url_false(self):
        class UrlForm(forms.Form):
            url = forms.StringField(
                "URL", validators=[forms.validators.ValidUrl(visit_url=False)]
            )

        form = UrlForm(meta={'csrf': False})
        # Invalid URL won't be tested
        form.url.data = 'http://localhosta'
        assert form.validate() is True

    def test_message_schemes(self):
        class UrlForm(forms.Form):
            url = forms.StringField(
                "URL",
                validators=[
                    forms.validators.ValidUrl(
                        allowed_schemes=('https', 'mailto'),
                        message_schemes="Scheme for '{url}' must be: {schemes}",
                    )
                ],
            )

        form = UrlForm(meta={'csrf': False})
        form.url.data = 'http://example.com'
        assert form.validate() is False
        assert form.url.errors == [
            "Scheme for 'http://example.com' must be: https, mailto"
        ]

    def test_message_domains(self):
        class UrlForm(forms.Form):
            url = forms.StringField(
                "URL",
                validators=[
                    forms.validators.ValidUrl(
                        allowed_domains=('example.net', 'example.org'),
                        message_domains="Allowed domains for '{url}': {domains}",
                    )
                ],
            )

        form = UrlForm(meta={'csrf': False})
        form.url.data = 'http://example.com'
        assert form.validate() is False
        assert form.url.errors == [
            "Allowed domains for 'http://example.com': example.net, example.org"
        ]


class TestFormBase(TestCaseBaseframe):
    # Subclasses must define a `Form`

    def setUp(self):
        super(TestFormBase, self).setUp()
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        self.form = self.Form(meta={'csrf': False})

    def tearDown(self):
        self.ctx.pop()


class TestForEach(TestFormBase):
    class Form(forms.Form):
        textlist = forms.TextListField(validators=[forms.ForEach([forms.URL()])])

    def test_passes_single(self):
        self.form.process(formdata=MultiDict({'textlist': "http://www.example.com/"}))
        assert self.form.validate() is True

    def test_passes_list(self):
        self.form.process(
            formdata=MultiDict(
                {'textlist': "http://www.example.com\r\nhttp://www.example.org/"}
            )
        )
        assert self.form.validate() is True

    def test_fails_single(self):
        self.form.process(formdata=MultiDict({'textlist': "example"}))
        assert self.form.validate() is False

    def test_fails_list(self):
        self.form.process(
            formdata=MultiDict({'textlist': "www.example.com\r\nwww.example.org"})
        )
        assert self.form.validate() is False

    def test_fails_mixed1(self):
        self.form.process(
            formdata=MultiDict(
                {'textlist': "http://www.example.com/\r\nwww.example.org"}
            )
        )
        assert self.form.validate() is False

    def test_fails_mixed2(self):
        self.form.process(
            formdata=MultiDict(
                {'textlist': "www.example.com\r\nhttp://www.example.org/"}
            )
        )
        assert self.form.validate() is False

    def test_fails_blanklines(self):
        self.form.process(
            formdata=MultiDict({'textlist': "http://www.example.com\r\n"})
        )
        assert self.form.validate() is False


class TestForEachChained(TestFormBase):
    class Form(forms.Form):
        textlist = forms.TextListField(
            validators=[forms.ForEach([forms.Optional(), forms.URL()])]
        )

    def test_skips_blanklines_and_fails(self):
        self.form.process(formdata=MultiDict({'textlist': "\r\nwww.example.com"}))
        assert self.form.validate() is False

    def test_skips_blanklines_and_passes(self):
        self.form.process(
            formdata=MultiDict({'textlist': "\r\nhttp://www.example.com/"})
        )
        assert self.form.validate() is True


class TestForEachFiltered(TestFormBase):
    class Form(forms.Form):
        textlist = forms.TextListField(
            validators=[forms.ForEach([forms.URL()])], filters=[forms.strip_each()]
        )

    def test_passes_blanklines(self):
        self.form.process(
            formdata=MultiDict({'textlist': "http://www.example.com\r\n"})
        )
        assert self.form.validate() is True


class TestAllowedIf(TestFormBase):
    class Form(forms.Form):
        other = forms.StringField("Other")
        field = forms.StringField(
            "Field", validators=[forms.validators.AllowedIf('other')]
        )

    other_not_empty = "Not empty"

    def test_is_allowed(self):
        self.form.process(other=self.other_not_empty, field="Also not empty")
        assert self.form.validate() is True

    def test_is_untested_when_empty(self):
        self.form.process(other=self.other_not_empty)
        assert self.form.validate() is True

    def test_is_untested_when_all_empty(self):
        self.form.process()
        assert self.form.validate() is True

    def test_not_allowed(self):
        self.form.process(field="Not empty")
        assert self.form.validate() is False

    def test_not_allowed2(self):
        self.form.process(other="", field="Not empty")
        assert self.form.validate() is False


class TestAllowedIfInteger(TestAllowedIf):
    class Form(forms.Form):
        other = forms.IntegerField("Other")
        field = forms.StringField(
            "Field", validators=[forms.validators.AllowedIf('other')]
        )

    other_not_empty = 0


class TestOptionalIf(TestFormBase):
    class Form(forms.Form):
        other = forms.StringField("Other")
        field = forms.StringField(
            "Field",
            validators=[
                forms.validators.OptionalIf('other'),
                forms.validators.DataRequired(),
            ],
        )

    other_empty = ''
    other_not_empty = "Not empty"

    def test_is_optional(self):
        self.form.process(other=self.other_not_empty)
        assert self.form.validate() is True

    def test_is_required_with_none(self):
        self.form.process(other=None)
        assert self.form.validate() is False

    def test_is_required_with_empty(self):
        self.form.process(other='')
        assert self.form.validate() is False

    def test_is_optional_but_value_accepted(self):
        self.form.process(other=self.other_not_empty, field="Not empty")
        assert self.form.validate() is True

    def test_is_required_with_none_and_accepted(self):
        self.form.process(other=None, field="Not empty")
        assert self.form.validate() is True

    def test_is_required_with_empty_and_accepted(self):
        self.form.process(other=self.other_empty, field="Not empty")
        assert self.form.validate() is True


class TestOptionalIfInteger(TestOptionalIf):
    class Form(forms.Form):
        other = forms.IntegerField("Other")
        field = forms.StringField(
            "Field",
            validators=[
                forms.validators.OptionalIf('other'),
                forms.validators.DataRequired(),
            ],
        )

    other_empty = None  # '' is not valid in IntegerField
    other_not_empty = 0


class TestRequiredIf(TestFormBase):
    class Form(forms.Form):
        other = forms.StringField("Other")
        field = forms.StringField(
            "Field",
            validators=[
                forms.validators.RequiredIf('other'),
                forms.validators.Optional(),
            ],
        )

    other_empty = ''
    other_not_empty = "Not empty"

    def test_is_required(self):
        self.form.process(other=self.other_not_empty)
        assert self.form.validate() is False

    def test_is_required2(self):
        self.form.process(other=self.other_not_empty, field="")
        assert self.form.validate() is False

    def test_is_required_and_valid(self):
        self.form.process(other=self.other_not_empty, field="Also not empty")
        assert self.form.validate() is True

    def test_is_not_required(self):
        self.form.process()
        assert self.form.validate() is True

    def test_is_not_required2(self):
        self.form.process(other=self.other_empty)
        assert self.form.validate() is True


class TestRequiredIfInteger(TestRequiredIf):
    class Form(forms.Form):
        other = forms.IntegerField("Other")
        field = forms.StringField(
            "Field",
            validators=[
                forms.validators.RequiredIf('other'),
                forms.validators.Optional(),
            ],
        )

    other_empty = None  # '' is not valid in IntegerField
    other_not_empty = 0
