"""Test form validators."""
# pylint: disable=redefined-outer-name

from types import SimpleNamespace
import re
import typing as t
import warnings

from werkzeug.datastructures import MultiDict
import pytest
import requests_mock
import urllib3

from baseframe import forms
from baseframe.utils import MxLookupError, is_public_email_domain

# --- Fixture classes ------------------------------------------------------------------


class FormTest(forms.Form):
    test_field = forms.IntegerField("Test label", default=1)


url_reject_list = [
    (['example.com', re.compile(r'example.in')], 'This URL is not allowed')
]


class UrlFormTest(forms.Form):
    url = forms.URLField(
        "URL",
        validators=[
            forms.validators.DataRequired(),
            forms.validators.Length(max=255),
            forms.validators.ValidUrl(invalid_urls=url_reject_list),
        ],
        filters=[forms.filters.strip()],
    )


class EmojiFormTest(forms.Form):
    emoji = forms.StringField("Emoji", validators=[forms.validators.IsEmoji()])


class AllUrlsFormTest(forms.Form):
    content_with_urls = forms.TextAreaField(
        "Content",
        validators=[
            forms.validators.DataRequired(),
            forms.validators.AllUrlsValid(),
        ],
    )


class PublicEmailDomainFormTest(forms.Form):
    webmail_domain = forms.StringField(
        "Webmail Domain", validators=[forms.validators.IsPublicEmailDomain()]
    )
    not_webmail_domain = forms.StringField(
        "Not Webmail Domain", validators=[forms.validators.IsNotPublicEmailDomain()]
    )


@pytest.fixture()
def tforms(ctx):
    urllib3.disable_warnings()
    yield SimpleNamespace(
        url_form=UrlFormTest(meta={'csrf': False}),
        emoji_form=EmojiFormTest(meta={'csrf': False}),
        all_urls_form=AllUrlsFormTest(meta={'csrf': False}),
        webmail_form=PublicEmailDomainFormTest(meta={'csrf': False}),
        nonce_form=FormTest(meta={'csrf': False}),
    )
    warnings.resetwarnings()


# --- Tests ----------------------------------------------------------------------------


def test_is_empty() -> None:
    assert forms.validators.is_empty(0) is False
    assert forms.validators.is_empty('0') is False
    assert forms.validators.is_empty('') is True
    assert forms.validators.is_empty(()) is True
    assert forms.validators.is_empty(None) is True


def test_valid_url(app, tforms) -> None:
    with app.test_request_context('/'):
        url = 'https://hasgeek.com/'
        tforms.url_form.process(url=url)
        assert tforms.url_form.validate()


def test_invalid_url(app, tforms) -> None:
    with app.test_request_context('/'):
        url = 'https://hasgeek'
        tforms.url_form.process(url=url)
        assert not tforms.url_form.validate()


def test_valid_emoji(app, tforms) -> None:
    with app.test_request_context('/'):
        dat = '👍'
        tforms.emoji_form.process(emoji=dat)
        assert tforms.emoji_form.validate() is True


def test_invalid_emoji(app, tforms) -> None:
    with app.test_request_context('/'):
        dat = 'eviltext'
        tforms.emoji_form.process(emoji=dat)
        assert tforms.emoji_form.validate() is False


def test_public_email_domain(app, tforms) -> None:
    with app.test_request_context('/'):
        # both valid
        tforms.webmail_form.process(
            webmail_domain='gmail.com', not_webmail_domain='i❤.ws'
        )
        assert tforms.webmail_form.validate()

        # both invalid
        tforms.webmail_form.process(
            webmail_domain='i❤.ws', not_webmail_domain='gmail.com'
        )
        assert not tforms.webmail_form.validate()
        assert 'webmail_domain' in tforms.webmail_form.errors
        assert 'not_webmail_domain' in tforms.webmail_form.errors

        # one valid, one invalid
        tforms.webmail_form.process(
            webmail_domain='gmail.com', not_webmail_domain='gmail.com'
        )
        assert not tforms.webmail_form.validate()
        assert 'webmail_domain' not in tforms.webmail_form.errors
        assert 'not_webmail_domain' in tforms.webmail_form.errors

        # these domain lookups will fail because of the DNS label length limit.
        # (abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijks is 64
        # characters, the maximum length of a DNS label is 63 characters) ``mxsniff``
        # will raise ``MxLookupError`` for these domains. So, webmail_domain should
        # fail, and not_webmail_domain should pass.
        tforms.webmail_form.process(
            webmail_domain='www'
            '.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijks.com',
            not_webmail_domain='www'
            '.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijks.com',
        )
        assert not tforms.webmail_form.validate()
        assert 'webmail_domain' in tforms.webmail_form.errors
        assert 'not_webmail_domain' not in tforms.webmail_form.errors


def test_public_email_domain_helper(app) -> None:
    with app.test_request_context('/'):
        assert is_public_email_domain('gmail.com', default=False)
        assert not is_public_email_domain('google.com', default=False)

        # Intentionally trigger a DNS lookup failure using an invalid domain name.
        # Since no default is provided, we will receive an exception.
        with pytest.raises(MxLookupError):
            is_public_email_domain(
                'www'
                '.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijks.com'
            )

        # If default value is provided, it'll return default is case of DNS lookup
        # failure.
        assert not is_public_email_domain(
            'www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijks.com',
            default=False,
        )
        assert is_public_email_domain(
            'www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijks.com',
            default=True,
        )


def test_url_without_protocol(app, tforms) -> None:
    with app.test_request_context('/'):
        url = 'hasgeek.com'
        tforms.url_form.process(url=url)
        assert not tforms.url_form.validate()


def test_inaccessible_url(app, tforms) -> None:
    with app.test_request_context('/'):
        url = 'http://4dc1f6f0e7bc44f2b5b44f00abea4eae.com/'
        tforms.url_form.process(url=url)
        assert not tforms.url_form.validate()


def test_disallowed_url(app, tforms) -> None:
    with app.test_request_context('/'):
        url = 'https://example.com/'
        tforms.url_form.process(url=url)
        assert not tforms.url_form.validate()
        url = 'https://example.in/'
        tforms.url_form.process(url=url)
        assert not tforms.url_form.validate()


def test_html_snippet_valid_urls(app, tforms) -> None:
    url1 = 'https://hasgeek.com/'
    url2 = 'https://hasjob.co/'
    with app.test_request_context('/'):
        snippet = f'''
            <ul>
              <li><a href="{url1}">url1</a></li>
              <li><a href="{url2}">url2</a></li>
            </ul>
            '''
        tforms.all_urls_form.process(content_with_urls=snippet)
        assert tforms.all_urls_form.validate()


def test_html_snippet_invalid_urls(app, tforms) -> None:
    url1 = 'https://hasgeek.com/'
    url2 = 'https://hasjob'
    with app.test_request_context('/'):
        snippet = f'''
            <ul>
              <li><a href="{url1}">url1</a></li>
              <li><a href="{url2}">url2</a></li>
            </ul>
        '''
        tforms.all_urls_form.process(content_with_urls=snippet)
        assert not tforms.all_urls_form.validate()


@pytest.mark.usefixtures('ctx')
def test_nonce_form_on_success(tforms) -> None:
    """A form with a nonce cannot be submitted twice."""
    formdata = MultiDict({field.name: field.data for field in tforms.nonce_form})
    nonce = tforms.nonce_form.form_nonce.data
    assert nonce
    assert tforms.nonce_form.validate() is True
    # Nonce changes on each submit
    assert nonce != tforms.nonce_form.form_nonce.data
    assert not tforms.nonce_form.form_nonce.errors
    # Now restore old form contents
    tforms.nonce_form.process(formdata=formdata)
    # Second attempt on the same form contents will fail
    assert tforms.nonce_form.validate() is False
    assert tforms.nonce_form.form_nonce.errors


@pytest.mark.usefixtures('ctx')
def test_nonce_form_on_failure(tforms) -> None:
    """Form resubmission is not blocked (via the nonce) when validation fails."""
    tforms.emoji_form.process(
        formdata=MultiDict(
            {'emoji': 'not-emoji', 'form_nonce': tforms.emoji_form.form_nonce.data}
        )
    )
    assert tforms.emoji_form.validate() is False
    assert not tforms.emoji_form.form_nonce.errors
    formdata = MultiDict(
        {'emoji': '👍', 'form_nonce': tforms.emoji_form.form_nonce.data}
    )
    tforms.emoji_form.process(formdata=formdata)
    assert tforms.emoji_form.validate() is True
    assert not tforms.emoji_form.form_nonce.errors
    # Second attempt on the same form data will fail
    tforms.emoji_form.process(formdata)
    assert tforms.emoji_form.validate() is False
    assert tforms.emoji_form.errors


@pytest.mark.usefixtures('ctx')
def test_no_schemes() -> None:
    class UrlForm(forms.Form):
        url = forms.StringField("URL", validators=[forms.validators.ValidUrl()])

    form = UrlForm(meta={'csrf': False})
    form.url.data = 'mailto:example@example.com'
    assert form.validate() is True


@pytest.mark.usefixtures('ctx')
def test_static_schemes() -> None:
    class UrlForm(forms.Form):
        url = forms.StringField(
            "URL",
            validators=[forms.validators.ValidUrl(allowed_schemes=('http', 'https'))],
        )

    form = UrlForm(meta={'csrf': False})
    form.url.data = 'mailto:example@example.com'
    assert form.validate() is False


@pytest.mark.usefixtures('ctx')
def test_static_schemes_allowed() -> None:
    class UrlForm(forms.Form):
        url = forms.StringField(
            "URL",
            validators=[
                forms.validators.ValidUrl(allowed_schemes=('http', 'https', 'mailto'))
            ],
        )

    form = UrlForm(meta={'csrf': False})
    form.url.data = 'mailto:example@example.com'
    assert form.validate() is True


@pytest.mark.usefixtures('ctx')
def test_callable_schemes() -> None:
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


@pytest.mark.usefixtures('ctx')
def test_callable_schemes_allowed() -> None:
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


@pytest.mark.usefixtures('ctx')
def test_no_domains() -> None:
    class UrlForm(forms.Form):
        url = forms.StringField("URL", validators=[forms.validators.ValidUrl()])

    form = UrlForm(meta={'csrf': False})
    form.url.data = 'http://www.example.com'
    assert form.validate() is True


@pytest.mark.usefixtures('ctx')
def test_static_domains() -> None:
    class UrlForm(forms.Form):
        url = forms.StringField(
            "URL",
            validators=[forms.validators.ValidUrl(allowed_domains=('example.net',))],
        )

    form = UrlForm(meta={'csrf': False})
    form.url.data = 'http://www.example.com'
    assert form.validate() is False


@pytest.mark.usefixtures('ctx')
def test_static_domains_misconfigured() -> None:
    """Domains must be exact matches including subdomains."""

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


@pytest.mark.usefixtures('ctx')
def test_static_domains_allowed() -> None:
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


@pytest.mark.usefixtures('ctx')
def test_static_domains_case() -> None:
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


@pytest.mark.usefixtures('ctx')
def test_callable_domains() -> None:
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


@pytest.mark.usefixtures('ctx')
def test_callable_domains_allowed() -> None:
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


@pytest.mark.usefixtures('ctx')
def test_visit_url_true() -> None:
    class UrlForm(forms.Form):
        url = forms.StringField(
            "URL", validators=[forms.validators.ValidUrl(visit_url=True)]
        )

    form = UrlForm(meta={'csrf': False})
    # Invalid URL will fail a load test
    form.url.data = 'http://localhosta'
    assert form.validate() is False


@pytest.mark.usefixtures('ctx')
def test_visit_url_false() -> None:
    class UrlForm(forms.Form):
        url = forms.StringField(
            "URL", validators=[forms.validators.ValidUrl(visit_url=False)]
        )

    form = UrlForm(meta={'csrf': False})
    # Invalid URL won't be tested
    form.url.data = 'http://localhosta'
    assert form.validate() is True


@pytest.mark.usefixtures('ctx')
def test_message_schemes() -> None:
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
    assert form.url.errors == ["Scheme for 'http://example.com' must be: https, mailto"]


@pytest.mark.usefixtures('ctx')
def test_message_domains() -> None:
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


@pytest.mark.usefixtures('ctx')
def test_redirect_url() -> None:
    class UrlForm(forms.Form):
        url = forms.StringField(
            "URL",
            validators=[
                forms.validators.ValidUrl(
                    allowed_domains=('youtu.be'),
                )
            ],
        )

    url = 'https://youtu.be/shorturl'
    longurl = 'https://www.youtube.com/watch?v=longurl'

    with requests_mock.Mocker() as m:
        m.get(url, status_code=303, headers={'Location': longurl})
        m.get(longurl, status_code=200)

        form = UrlForm(meta={'csrf': False})
        form.url.data = url
        assert form.validate() is True


@pytest.mark.usefixtures('ctx')
def test_cloudflare_protected_url() -> None:
    class UrlForm(forms.Form):
        url = forms.StringField(
            "URL",
            validators=[forms.validators.ValidUrl()],
        )

    url = 'https://important-domain.com'

    with requests_mock.Mocker() as m:
        m.get(url, status_code=403)

        form = UrlForm(meta={'csrf': False})
        form.url.data = url
        assert form.validate() is True


class TestFormBase:
    Form: t.Type[forms.Form]
    form: forms.Form

    @pytest.fixture(autouse=True)
    def _setup(self, app):
        with app.app_context():
            self.form = self.Form(meta={'csrf': False})
            yield


class TestForEach(TestFormBase):
    class Form(forms.Form):
        """Test form."""

        textlist = forms.TextListField(
            validators=[forms.validators.ForEach([forms.validators.URL()])]
        )

    def test_passes_single(self) -> None:
        self.form.process(formdata=MultiDict({'textlist': "http://www.example.com/"}))
        assert self.form.validate() is True

    def test_passes_list(self) -> None:
        self.form.process(
            formdata=MultiDict(
                {'textlist': "http://www.example.com\r\nhttp://www.example.org/"}
            )
        )
        assert self.form.validate() is True

    def test_fails_single(self) -> None:
        self.form.process(formdata=MultiDict({'textlist': "example"}))
        assert self.form.validate() is False

    def test_fails_list(self) -> None:
        self.form.process(
            formdata=MultiDict({'textlist': "www.example.com\r\nwww.example.org"})
        )
        assert self.form.validate() is False

    def test_fails_mixed1(self) -> None:
        self.form.process(
            formdata=MultiDict(
                {'textlist': "http://www.example.com/\r\nwww.example.org"}
            )
        )
        assert self.form.validate() is False

    def test_fails_mixed2(self) -> None:
        self.form.process(
            formdata=MultiDict(
                {'textlist': "www.example.com\r\nhttp://www.example.org/"}
            )
        )
        assert self.form.validate() is False

    def test_fails_blanklines(self) -> None:
        self.form.process(
            formdata=MultiDict({'textlist': "http://www.example.com\r\n"})
        )
        assert self.form.validate() is False


class TestForEachChained(TestFormBase):
    class Form(forms.Form):
        """Test form."""

        textlist = forms.TextListField(
            validators=[
                forms.validators.ForEach(
                    [forms.validators.Optional(), forms.validators.URL()]
                )
            ]
        )

    def test_skips_blanklines_and_fails(self) -> None:
        self.form.process(formdata=MultiDict({'textlist': "\r\nwww.example.com"}))
        assert self.form.validate() is False

    def test_skips_blanklines_and_passes(self) -> None:
        self.form.process(
            formdata=MultiDict({'textlist': "\r\nhttp://www.example.com/"})
        )
        assert self.form.validate() is True


class TestForEachFiltered(TestFormBase):
    class Form(forms.Form):
        """Test form."""

        textlist = forms.TextListField(
            validators=[forms.validators.ForEach([forms.validators.URL()])],
            filters=[forms.filters.strip_each()],
        )

    def test_passes_blanklines(self) -> None:
        self.form.process(
            formdata=MultiDict({'textlist': "http://www.example.com\r\n"})
        )
        assert self.form.validate() is True


class TestAllowedIf(TestFormBase):
    class Form(forms.Form):
        """Test form."""

        other = forms.StringField("Other")
        field = forms.StringField(
            "Field", validators=[forms.validators.AllowedIf('other')]
        )

    other_not_empty: t.Any = "Not empty"

    def test_is_allowed(self) -> None:
        self.form.process(other=self.other_not_empty, field="Also not empty")
        assert self.form.validate() is True

    def test_is_untested_when_empty(self) -> None:
        self.form.process(other=self.other_not_empty)
        assert self.form.validate() is True

    def test_is_untested_when_all_empty(self) -> None:
        self.form.process()
        assert self.form.validate() is True

    def test_not_allowed(self) -> None:
        self.form.process(field="Not empty")
        assert self.form.validate() is False

    def test_not_allowed2(self) -> None:
        self.form.process(other="", field="Not empty")
        assert self.form.validate() is False


class TestAllowedIfInteger(TestAllowedIf):
    class Form(forms.Form):
        """Test form."""

        other = forms.IntegerField("Other")
        field = forms.StringField(
            "Field", validators=[forms.validators.AllowedIf('other')]
        )

    other_not_empty = 0


class TestOptionalIf(TestFormBase):
    class Form(forms.Form):
        """Test form."""

        other = forms.StringField("Other")
        field = forms.StringField(
            "Field",
            validators=[
                forms.validators.OptionalIf('other'),
                forms.validators.DataRequired(),
            ],
        )

    other_empty: t.Any = ''
    other_not_empty: t.Any = "Not empty"

    def test_is_optional(self) -> None:
        self.form.process(other=self.other_not_empty)
        assert self.form.validate() is True

    def test_is_required_with_none(self) -> None:
        self.form.process(other=None)
        assert self.form.validate() is False

    def test_is_required_with_empty(self) -> None:
        self.form.process(other='')
        assert self.form.validate() is False

    def test_is_optional_but_value_accepted(self) -> None:
        self.form.process(other=self.other_not_empty, field="Not empty")
        assert self.form.validate() is True

    def test_is_required_with_none_and_accepted(self) -> None:
        self.form.process(other=None, field="Not empty")
        assert self.form.validate() is True

    def test_is_required_with_empty_and_accepted(self) -> None:
        self.form.process(other=self.other_empty, field="Not empty")
        assert self.form.validate() is True


class TestOptionalIfInteger(TestOptionalIf):
    class Form(forms.Form):
        """Test form."""

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
        """Test form."""

        other = forms.StringField("Other")
        field = forms.StringField(
            "Field",
            validators=[
                forms.validators.RequiredIf('other'),
                forms.validators.Optional(),
            ],
        )

    other_empty: t.Any = ''
    other_not_empty: t.Any = "Not empty"

    def test_is_required(self) -> None:
        self.form.process(other=self.other_not_empty)
        assert self.form.validate() is False

    def test_is_required2(self) -> None:
        self.form.process(other=self.other_not_empty, field="")
        assert self.form.validate() is False

    def test_is_required_and_valid(self) -> None:
        self.form.process(other=self.other_not_empty, field="Also not empty")
        assert self.form.validate() is True

    def test_is_not_required(self) -> None:
        self.form.process()
        assert self.form.validate() is True

    def test_is_not_required2(self) -> None:
        self.form.process(other=self.other_empty)
        assert self.form.validate() is True


class TestRequiredIfInteger(TestRequiredIf):
    class Form(forms.Form):
        """Test form."""

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
