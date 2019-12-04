# -*- coding: utf-8 -*-

import warnings

from werkzeug.datastructures import MultiDict

from mxsniff import MXLookupException
import urllib3

from baseframe import forms
from baseframe.utils import is_public_email_domain

from .fixtures import (
    AllUrlsFormTest,
    PublicEmailDomainFormTest,
    TestCaseBaseframe,
    UrlFormTest,
)


class TestValidators(TestCaseBaseframe):
    def setUp(self):
        super(TestValidators, self).setUp()
        with self.app.test_request_context('/'):
            self.form = UrlFormTest(meta={'csrf': False})
            self.all_urls_form = AllUrlsFormTest(meta={'csrf': False})
            self.webmail_form = PublicEmailDomainFormTest(meta={'csrf': False})
        urllib3.disable_warnings()

    def tearDown(self):
        super(TestValidators, self).tearDown()
        warnings.resetwarnings()

    def test_valid_url(self):
        with self.app.test_request_context('/'):
            url = 'https://hasgeek.com/'
            self.form.process(url=url)
            assert self.form.validate()

    def test_invalid_url(self):
        with self.app.test_request_context('/'):
            url = 'https://hasgeek'
            self.form.process(url=url)
            assert not self.form.validate()

    def test_public_email_domain(self):
        with self.app.test_request_context('/'):
            # both valid
            self.webmail_form.process(
                webmail_domain=u'gmail.com', not_webmail_domain=u'i❤.ws'
            )
            self.assertTrue(self.webmail_form.validate())

            # both invalid
            self.webmail_form.process(
                webmail_domain=u'i❤.ws', not_webmail_domain=u'gmail.com'
            )
            self.assertFalse(self.webmail_form.validate())
            self.assertIn('webmail_domain', self.webmail_form.errors)
            self.assertIn('not_webmail_domain', self.webmail_form.errors)

            # one valid, one invalid
            self.webmail_form.process(
                webmail_domain=u'gmail.com', not_webmail_domain=u'gmail.com'
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
                webmail_domain=u'www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijks.com',
                not_webmail_domain=u'www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijks.com',
            )
            self.assertFalse(self.webmail_form.validate())
            self.assertIn('webmail_domain', self.webmail_form.errors)
            self.assertNotIn('not_webmail_domain', self.webmail_form.errors)

    def test_public_email_domain_helper(self):
        with self.app.test_request_context('/'):
            assert is_public_email_domain(u'gmail.com', default=False)
            assert not is_public_email_domain(u'google.com', default=False)

            # Intentionally trigger a DNS lookup failure using an invalid domain name.
            # Since no default is provided, we will receive an exception.
            with self.assertRaises(MXLookupException):
                is_public_email_domain(
                    u'www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijks.com'
                )

            # If default value is provided, it'll return default is case of DNS lookup failure.
            assert not is_public_email_domain(
                u'www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijks.com',
                default=False,
            )
            assert is_public_email_domain(
                u'www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijks.com',
                default=True,
            )

    def test_url_without_protocol(self):
        with self.app.test_request_context('/'):
            url = 'hasgeek.com'
            self.form.process(url=url)
            assert not self.form.validate()

    def test_inaccessible_url(self):
        with self.app.test_request_context('/'):
            url = 'http://4dc1f6f0e7bc44f2b5b44f00abea4eae.com/'
            self.form.process(url=url)
            assert not self.form.validate()

    def test_disallowed_url(self):
        with self.app.test_request_context('/'):
            url = 'https://example.com/'
            self.form.process(url=url)
            assert not self.form.validate()
            url = 'https://example.in/'
            self.form.process(url=url)
            assert not self.form.validate()

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
        self.form.process(other='', field="Not empty")
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
        self.form.process(other="")
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

    other_not_empty = 0
