from collections import namedtuple
from decimal import Decimal
from fractions import Fraction
from typing import Callable, Iterable, Set, Tuple, Union
from urllib.parse import urljoin, urlparse
import datetime
import re

from flask import current_app, request
from wtforms.validators import (  # NOQA
    URL,
    DataRequired,
    EqualTo,
    InputRequired,
    Length,
    NumberRange,
    Optional,
    StopValidation,
    ValidationError,
)

from pyisemail import is_email
import dns.resolver
import emoji
import html5lib
import requests

from coaster.utils import deobfuscate_email, make_name, md5sum

from ..extensions import _, __, asset_cache
from ..signals import exception_catchall
from ..utils import is_public_email_domain

__local = [
    'AllUrlsValid',
    'IsEmoji',
    'IsNotPublicEmailDomain',
    'IsPublicEmailDomain',
    'NoObfuscatedEmail',
    'AllowedIf',
    'OptionalIf',
    'RequiredIf',
    'ValidCoordinates',
    'ValidEmail',
    'ValidEmailDomain',
    'ValidName',
    'ValidUrl',
    'ForEach',
    'Recaptcha',
]
__imported = [  # WTForms validators
    'DataRequired',
    'EqualTo',
    'InputRequired',
    'Length',
    'NumberRange',
    'Optional',
    'StopValidation',
    'URL',
    'ValidationError',
]
__all__ = __local + __imported


EMAIL_RE = re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,63}\b', re.I)

_zero_values = (0, 0.0, Decimal('0'), 0j, Fraction(0, 1), datetime.time(0, 0, 0))

RECAPTCHA_VERIFY_SERVER = 'https://www.google.com/recaptcha/api/siteverify'
# Reproduced from flask_wtf.validators, with gettext applied
RECAPTCHA_ERROR_CODES = {
    'missing-input-secret': __("The secret parameter is missing"),
    'invalid-input-secret': __("The secret parameter is invalid or malformed"),
    'missing-input-response': __("The response parameter is missing"),
    'invalid-input-response': __("The response parameter is invalid or malformed"),
}

# XXX: This should use `Iterable[Union[str, Pattern]]` instead of `Iterable[object]`,
# but mypy doesn't recognise the output of re.compile as being an instance of Pattern
InvalidUrlPatterns = Iterable[Tuple[Iterable[object], str]]
AllowedListInit = Union[Iterable[str], Callable[[], Iterable[str]], None]
AllowedList = Union[Iterable[str], None]


def is_empty(value) -> bool:
    """Return True if the value is falsy but not a numeric zero."""
    return value not in _zero_values and not value


FakeField = namedtuple(
    'FakeField', ['data', 'raw_data', 'errors', 'gettext', 'ngettext']
)


class ForEach:
    """
    Runs specified validators on each element of an iterable value.

    If a validator raises :exc:`StopValidation`, it stops other validators within the
    chain given to :class:`ForEach`, but not validators specified alongside.
    """

    def __init__(self, validators) -> None:
        self.validators = validators

    def __call__(self, form, field) -> None:
        for element in field.data:
            fake_field = FakeField(element, element, [], field.gettext, field.ngettext)
            for validator in self.validators:
                try:
                    validator(form, fake_field)
                except StopValidation as e:
                    if str(e):
                        raise
                    break


class AllowedIf:
    """
    Validator that allows a value only if another field also has a value.

    :param str fieldname: Name of the other field
    :param str message: Validation error message. Will be formatted with an optional
        ``{field}`` label
    """

    default_message = __("This requires ‘{field}’ to be specified")

    def __init__(self, fieldname: str, message: str = None) -> None:
        self.fieldname = fieldname
        self.message = message or self.default_message

    def __call__(self, form, field) -> None:
        if field.data:
            if is_empty(form[self.fieldname].data):
                raise StopValidation(
                    self.message.format(field=form[self.fieldname].label.text)
                )


class OptionalIf(Optional):
    """
    Validator that makes this field optional if another field has data.

    If this field is required when the other field is empty, chain it with
    :class:`DataRequired`::

        field = forms.StringField("Field",
            validators=[
                forms.validators.OptionalIf('other'), forms.validators.DataRequired()
            ]
        )

    :param str fieldname: Name of the other field
    :param str message: Validation error message
    """

    default_message = __("This is required")

    def __init__(self, fieldname: str, message: str = None) -> None:
        super().__init__()
        self.fieldname = fieldname
        self.message = message or self.default_message

    def __call__(self, form, field) -> None:
        if not is_empty(form[self.fieldname].data):
            return super().__call__(form, field)


class RequiredIf(DataRequired):
    """
    Validator that makes this field required if another field has data.

    If this field is also optional when the other field is empty, chain it with
    :class:`Optional`::

        field = forms.StringField("Field",
            validators=[
                forms.validators.RequiredIf('other'), forms.validators.Optional()
            ]
        )

    :param str fieldname: Name of the other field
    :param str message: Validation error message
    """

    default_message = __("This is required")

    field_flags: Set[str] = set()

    def __init__(self, fieldname: str, message: str = None) -> None:
        message = message or self.default_message
        super().__init__(message=message)
        self.fieldname = fieldname

    def __call__(self, form, field) -> None:
        if not is_empty(form[self.fieldname].data):
            super().__call__(form, field)


class _Comparison:
    """Base class for validators that compare this field's value with another field."""

    default_message = __("Comparison failed")

    def __init__(self, fieldname: str, message: str = None) -> None:
        self.fieldname = fieldname
        self.message = message or self.default_message

    def __call__(self, form, field) -> None:
        other = form[self.fieldname]
        if not self.compare(field.data, other.data):
            d = {
                'other_label': hasattr(other, 'label')
                and other.label.text
                or self.fieldname,
                'other_name': self.fieldname,
            }
            raise ValidationError(self.message.format(**d))

    def compare(self, value, other) -> bool:
        raise NotImplementedError(_("Subclasses must define ``compare``"))


class GreaterThan(_Comparison):
    """
    Validate field.data > otherfield.data.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `{other_label}` and `{other_name}` to provide a
        more helpful error.
    """

    default_message = __("This must be greater than {other_label}")

    def compare(self, value, other) -> bool:
        return value > other


class GreaterThanEqualTo(_Comparison):
    """
    Validate field.data >= otherfield.data.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `{other_label}` and `{other_name}` to provide a
        more helpful error.
    """

    default_message = __("This must be greater than or equal to {other_label}")

    def compare(self, value, other) -> bool:
        return value >= other


class LesserThan(_Comparison):
    """
    Validate field.data < otherfield.data.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `{other_label}` and `{other_name}` to provide a
        more helpful error.
    """

    default_message = __("This must be lesser than {other_label}")

    def compare(self, value, other) -> bool:
        return value < other


class LesserThanEqualTo(_Comparison):
    """
    Validate field.data <= otherfield.data.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `{other_label}` and `{other_name}` to provide a
        more helpful error.
    """

    default_message = __("This must be lesser than or equal to {other_label}")

    def compare(self, value, other) -> bool:
        return value <= other


class NotEqualTo(_Comparison):
    """
    Validate field.data != otherfield.data.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `{other_label}` and `{other_name}` to provide a
        more helpful error.
    """

    default_message = __("This must not be the same as {other_label}")

    def compare(self, value, other) -> bool:
        return value != other


class IsEmoji:
    """
    Validate field to contain a single emoji.

    :param message:
        Error message to raise in case of a validation error.
    """

    default_message = __("This is not a valid emoji")

    def __init__(self, message: str = None) -> None:
        self.message = message or self.default_message

    def __call__(self, form, field) -> None:
        if field.data not in emoji.UNICODE_EMOJI_ENGLISH:  # type: ignore[attr-defined]
            raise ValidationError(self.message)


class IsPublicEmailDomain:
    """
    Validate that field.data belongs to a public email domain.

    If the domain lookup fails and mxsniff raises ``MXLookupException``, this validator
    will fail.

    :param message:
        Error message to raise in case of a validation error.
    """

    default_message = __("This domain is not a public email domain")

    def __init__(self, message: str = None, timeout: int = 30) -> None:
        self.message = message or self.default_message
        self.timeout = timeout

    def __call__(self, form, field) -> None:
        if is_public_email_domain(field.data, default=False, timeout=self.timeout):
            return
        raise ValidationError(self.message)


class IsNotPublicEmailDomain:
    """
    Validate that field.data does not belong to a public email domain.

    If the domain lookup fails and mxsniff raises ``MXLookupException``, this validator
    will still pass, as we expect that most domains are not public email domains.

    :param message:
        Error message to raise in case of a validation error.
    """

    default_message = __("This domain is a public email domain")

    def __init__(self, message: str = None, timeout: int = 30) -> None:
        self.message = message or self.default_message
        self.timeout = timeout

    def __call__(self, form, field) -> None:
        if not is_public_email_domain(field.data, default=False, timeout=self.timeout):
            return
        raise ValidationError(self.message)


class ValidEmail:
    """
    Validator to confirm an email address is likely to be valid.

    Criteria: email address is properly formatted and the domain exists.

    :param str message: Optional validation error message.
    """

    default_message = __("This email address does not appear to be valid")

    def __init__(self, message: str = None) -> None:
        self.message = message

    def __call__(self, form, field) -> None:
        try:
            diagnosis = is_email(field.data, check_dns=True, diagnose=True)
        except (dns.resolver.Timeout, dns.resolver.NoNameservers):
            return
        if diagnosis.code in (0, 3, 4):  # 0 is valid, 3 is DNS No NS, 4 is DNS timeout
            return
        raise StopValidation(self.message or diagnosis.message or self.default_message)


# Legacy name
ValidEmailDomain = ValidEmail


class ValidUrl:
    """
    Validator to confirm a HTTP URL is valid (returns 2xx status code).

    URIs using other protocol schemes are not validated, but can be explicitly
    disallowed by specifying ``allowed_schemes``.

    :param str message: Error message (None for default error message)
    :param str message_urltext: Unused parameter, only used in the :class:`AllUrlsValid`
        validator
    :param str message_schemes: Error message when the URL scheme is invalid
    :param str message_domains: Error message when the URL domain is not whitelisted
    :param list invalid_urls: A list of (patterns, message) tuples for URLs that will be
        rejected, where ``patterns`` is a list of strings or regular expressions
    :param set allowed_schemes: Allowed schemes in URLs (`None` implies no constraints)
    :param set allowed_domains: Whitelisted domains (`None` implies no constraints)
    :param bool visit_url: Visit the URL to confirm availability (default `True`)

    ``invalid_urls``, ``allowed_schemes`` and ``allowed_domains`` may also be callables
    that take no parameters and return the required data. They will be called once per
    validation.
    """

    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Hasgeek/linkchecker"
    )

    default_message = __("The URL “{url}” is not valid or is currently inaccessible")

    default_message_urltext = __(
        "The URL “{url}” linked from “{text}” is not valid or is currently inaccessible"
    )

    default_message_schemes = __("This URL’s protocol is not allowed")

    default_message_domains = __("This URL’s domain is not allowed")

    def __init__(
        self,
        message: str = None,
        message_urltext: str = None,
        message_schemes: str = None,
        message_domains: str = None,
        invalid_urls: InvalidUrlPatterns = (),
        allowed_schemes: AllowedListInit = None,
        allowed_domains: AllowedListInit = None,
        visit_url: bool = True,
    ):
        self.message = message or self.default_message
        self.message_urltext = message_urltext or self.default_message_urltext
        self.message_schemes = message_schemes or self.default_message_schemes
        self.message_domains = message_domains or self.default_message_domains
        self.invalid_urls = invalid_urls
        self.allowed_schemes = allowed_schemes
        self.allowed_domains = allowed_domains
        self.visit_url = visit_url

    def check_url(
        self,
        url: str,
        allowed_schemes: AllowedList,
        allowed_domains: AllowedList,
        invalid_urls: InvalidUrlPatterns,
        text: Union[str, None] = None,
    ):
        """
        Inner method to actually check the URL.

        This method accepts ``allowed_schemes``, ``allowed_domains`` and
        ``invalid_urls`` as direct parameters despite their availability via `self`
        because they may be callables, and in :class:`AllUrlsValid` we call
        :meth:`check_url` repeatedly. The callables should be called only once. This
        optimization has no value in the base class :class:`ValidUrl`.

        As the validator is instantiated once per form field, it cannot mutate itself
        at runtime to cache the callables' results, and must instead pass them from one
        method to the next.
        """
        urlparts = urlparse(url)
        if allowed_schemes:
            if urlparts.scheme not in allowed_schemes:
                return self.message_schemes.format(
                    url=url, schemes=_(', ').join(allowed_schemes)
                )
        if allowed_domains:
            if urlparts.netloc.lower() not in allowed_domains:
                return self.message_domains.format(
                    url=url, domains=_(', ').join(allowed_domains)
                )

        if urlparts.scheme not in ('http', 'https') or not self.visit_url:
            # The rest of this function only validates HTTP urls.
            return

        cache_key = 'linkchecker/' + md5sum(url)
        try:
            cache_check = asset_cache.get(cache_key)
        except ValueError:  # Possible error from a broken pickle
            cache_check = None
        # Read from cache, but assume cache may be broken
        # since Flask-Cache stores data as a pickle,
        # which is version-specific
        if cache_check and isinstance(cache_check, dict):
            rurl = cache_check.get('url')
            code = cache_check.get('code')
        else:
            rurl = None  # rurl is the response URL after following redirects

        if not rurl or not code:
            try:
                r = requests.get(
                    url,
                    timeout=30,
                    allow_redirects=True,
                    verify=False,
                    headers={'User-Agent': self.user_agent},
                )
                code = r.status_code
                rurl = r.url
            except (
                # Still a relative URL? Must be broken
                requests.exceptions.MissingSchema,
                # Name resolution or connection failed
                requests.exceptions.ConnectionError,
                # Didn't respond in time
                requests.exceptions.Timeout,
            ):
                code = None
            except Exception as e:
                exception_catchall.send(e)
                code = None

        if rurl is not None and code in (
            200,
            201,
            202,
            203,
            204,
            205,
            206,
            207,
            208,
            226,
            403,
            999,
        ):
            # Cloudflare now returns HTTP 403 for urls behind its bot protection.
            # Hence we're accepting 403 as an acceptable code.
            #
            # 999 is a non-standard too-many-requests error. We can't look past it to
            # check a URL, so we let it pass

            # The URL works, so now we check if it's in a reject list. This part
            # runs _after_ attempting to load the URL as we want to catch redirects.
            for patterns, message in invalid_urls:
                for pattern in patterns:
                    # For text patterns, do a substring search. For regex patterns
                    # (assumed so if not text), do a regex search. Test with the final
                    # URL from the response, after redirects, but report errors using
                    # the URL the user provided
                    if (
                        pattern in rurl
                        if isinstance(pattern, str)
                        else pattern.search(rurl) is not None  # type: ignore[attr-defined]
                    ):
                        return message.format(url=url, text=text)
            # All good. The URL works and isn't invalid, so save to cache and return
            # without an error message
            asset_cache.set(cache_key, {'url': rurl, 'code': code}, timeout=86400)
            return
        else:
            if text is not None and url != text:
                return self.message_urltext.format(url=url, text=text)
            else:
                return self.message.format(url=url)

    def call_inner(
        self,
        field,
        current_url: str,
        allowed_schemes: AllowedList,
        allowed_domains: AllowedList,
        invalid_urls: InvalidUrlPatterns,
    ):
        error = self.check_url(
            urljoin(current_url, field.data),
            allowed_schemes,
            allowed_domains,
            invalid_urls,
        )
        if error:
            raise StopValidation(error)

    def __call__(self, form, field) -> None:
        if field.data:
            current_url = request.url if request else ''
            invalid_urls = (
                self.invalid_urls()
                if callable(self.invalid_urls)
                else self.invalid_urls
            )
            allowed_schemes = (
                self.allowed_schemes()
                if callable(self.allowed_schemes)
                else self.allowed_schemes
            )
            allowed_domains = (
                self.allowed_domains()
                if callable(self.allowed_domains)
                else self.allowed_domains
            )

            return self.call_inner(
                field, current_url, allowed_schemes, allowed_domains, invalid_urls
            )


class AllUrlsValid(ValidUrl):
    """
    Validator to confirm all URLs in a HTML snippet.

    Subclasses :class:`ValidUrl` and accepts the same parameters.
    """

    def call_inner(
        self,
        field,
        current_url: str,
        allowed_schemes: AllowedList,
        allowed_domains: AllowedList,
        invalid_urls: InvalidUrlPatterns,
    ) -> None:
        html_tree = html5lib.parse(field.data, namespaceHTMLElements=False)
        for text, href in (
            (tag.text, tag.attrib.get('href')) for tag in html_tree.iter('a')
        ):
            error = self.check_url(
                urljoin(current_url, href),
                allowed_schemes,
                allowed_domains,
                invalid_urls,
                text,
            )
            if error:
                field.errors.append(error)
        if field.errors:
            raise StopValidation()


class NoObfuscatedEmail:
    """Scan for obfuscated email addresses in the provided text and reject them."""

    default_message = __("Email address identified")

    def __init__(self, message: str = None) -> None:
        self.message = message or self.default_message

    def __call__(self, form, field) -> None:
        emails = EMAIL_RE.findall(deobfuscate_email(field.data or ''))
        for email in emails:
            try:
                diagnosis = is_email(email, check_dns=True, diagnose=True)
                if diagnosis.code == 0:
                    raise StopValidation(self.message)
            except (dns.resolver.Timeout, dns.resolver.NoNameservers):
                pass


class ValidName:

    default_message = __(
        "This name contains unsupported characters. "
        "It should have letters, numbers and non-terminal hyphens only"
    )

    def __init__(self, message: str = None) -> None:
        self.message = message or self.default_message

    def __call__(self, form, field) -> None:
        if make_name(field.data) != field.data:
            raise StopValidation(self.message)


class ValidCoordinates:

    default_message = __("Valid latitude and longitude expected")
    default_message_latitude = __("Latitude must be within ± 90 degrees")
    default_message_longitude = __("Longitude must be within ± 180 degrees")

    def __init__(
        self,
        message: str = None,
        message_latitude: str = None,
        message_longitude: str = None,
    ) -> None:
        self.message = message or self.default_message
        self.message_latitude = message_latitude or self.default_message_latitude
        self.message_longitude = message_longitude or self.default_message_longitude

    def __call__(self, form, field) -> None:
        if len(field.data) != 2:
            raise StopValidation(self.message)
        if not -90 <= field.data[0] <= 90:
            raise StopValidation(self.message_latitude)
        if not -180 <= field.data[1] <= 180:
            raise StopValidation(self.message_longitude)


class Recaptcha:
    """Validates a ReCaptcha."""

    default_message_network = __("The server was temporarily unreachable. Try again")

    def __init__(self, message: str = None, message_network: str = None) -> None:
        if message is None:
            message = RECAPTCHA_ERROR_CODES['missing-input-response']

        self.message = message
        self.message_network = message_network or self.default_message_network

    def __call__(self, form, field) -> None:
        if current_app.testing:
            return

        if request.json:
            response = request.json.get('g-recaptcha-response', '')
        else:
            response = request.form.get('g-recaptcha-response', '')
        remote_ip = request.remote_addr

        if not response:
            raise ValidationError(self.message)

        if not self._validate_recaptcha(response, remote_ip):
            field.recaptcha_error = 'incorrect-captcha-sol'
            raise ValidationError(self.message)

    def _validate_recaptcha(self, response: str, remote_addr: str) -> bool:
        """Perform the actual validation."""
        try:
            private_key = current_app.config['RECAPTCHA_PRIVATE_KEY']
        except KeyError:
            raise RuntimeError("No RECAPTCHA_PRIVATE_KEY config set")

        data = {
            'secret': private_key,
            'remoteip': remote_addr,
            'response': response,
        }

        try:
            http_response = requests.post(RECAPTCHA_VERIFY_SERVER, data=data)
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ):
            raise ValidationError(self.message_network)

        if http_response.status_code != 200:
            return False

        json_resp = http_response.json()

        if json_resp["success"]:
            return True

        for error in json_resp.get("error-codes", []):
            if error in RECAPTCHA_ERROR_CODES:
                raise ValidationError(RECAPTCHA_ERROR_CODES[error])

        return False
