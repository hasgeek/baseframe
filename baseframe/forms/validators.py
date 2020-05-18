# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from six.moves.urllib.parse import urljoin, urlparse
import six

from collections import namedtuple
from decimal import Decimal
from fractions import Fraction
import datetime
import re

from flask import request
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

from .. import asset_cache
from .. import b_ as _
from .. import b__ as __
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


def is_empty(value):
    """
    Returns True if the value is falsy but not a numeric zero::

        >>> is_empty(0)
        False
        >>> is_empty('0')
        False
        >>> is_empty('')
        True
        >>> is_empty(())
        True
        >>> is_empty(None)
        True
    """
    return value not in _zero_values and not value


FakeField = namedtuple(
    'FakeField', ['data', 'raw_data', 'errors', 'gettext', 'ngettext']
)


class ForEach(object):
    """
    Runs specified validators on each element of an iterable value. If a validator
    raises :exc:`StopValidation`, it stops other validators within the chain given
    to :class:`ForEach`, but not validators specified alongside.
    """

    def __init__(self, validators):
        self.validators = validators

    def __call__(self, form, field):
        for element in field.data:
            fake_field = FakeField(element, element, [], field.gettext, field.ngettext)
            for validator in self.validators:
                try:
                    validator(form, fake_field)
                except StopValidation as e:
                    if six.text_type(e):
                        raise
                    else:
                        break


class AllowedIf(object):
    """
    Validator that allows a value only if another field also has a value.

    :param str fieldname: Name of the other field
    :param str message: Validation error message. Will be formatted with an optional
        ``{field}`` label
    """

    default_message = __("This requires ‘{field}’ to be specified")

    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message or self.default_message

    def __call__(self, form, field):
        if field.data:
            if is_empty(form[self.fieldname].data):
                raise StopValidation(
                    self.message.format(field=form[self.fieldname].label.text)
                )


class OptionalIf(Optional):
    """
    Validator that makes this field optional if another field has data. If this
    field is required when the other field is empty, chain it with
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

    def __init__(self, fieldname, message=None):
        super(OptionalIf, self).__init__()
        self.fieldname = fieldname
        self.message = message or self.default_message

    def __call__(self, form, field):
        if not is_empty(form[self.fieldname].data):
            return super(OptionalIf, self).__call__(form, field)


class RequiredIf(DataRequired):
    """
    Validator that makes this field required if another field has data. If this
    field is also optional when the other field is empty, chain it with
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

    field_flags = set()

    def __init__(self, fieldname, message=None):
        message = message or self.default_message
        super(RequiredIf, self).__init__(message=message)
        self.fieldname = fieldname

    def __call__(self, form, field):
        if not is_empty(form[self.fieldname].data):
            super(RequiredIf, self).__call__(form, field)


class _Comparison(object):
    """
    Base class for validators that compare this field's value with another field
    """

    default_message = __("Comparison failed")

    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message or self.default_message

    def __call__(self, form, field):
        other = form[self.fieldname]
        if not self.compare(field.data, other.data):
            d = {
                'other_label': hasattr(other, 'label')
                and other.label.text
                or self.fieldname,
                'other_name': self.fieldname,
            }
            raise ValidationError(self.message.format(**d))

    def compare(self, value, other):
        raise NotImplementedError(_("Subclasses must define ``compare``"))


class GreaterThan(_Comparison):
    """
    Validate field.data > otherfield.data

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `{other_label}` and `{other_name}` to provide a
        more helpful error.
    """

    default_message = __("This must be greater than {other_label}")

    def compare(self, value, other):
        return value > other


class GreaterThanEqualTo(_Comparison):
    """
    Validate field.data >= otherfield.data

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `{other_label}` and `{other_name}` to provide a
        more helpful error.
    """

    default_message = __("This must be greater than or equal to {other_label}")

    def compare(self, value, other):
        return value >= other


class LesserThan(_Comparison):
    """
    Validate field.data < otherfield.data

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `{other_label}` and `{other_name}` to provide a
        more helpful error.
    """

    default_message = __("This must be lesser than {other_label}")

    def compare(self, value, other):
        return value < other


class LesserThanEqualTo(_Comparison):
    """
    Validate field.data <= otherfield.data

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `{other_label}` and `{other_name}` to provide a
        more helpful error.
    """

    default_message = __("This must be lesser than or equal to {other_label}")

    def compare(self, value, other):
        return value <= other


class NotEqualTo(_Comparison):
    """
    Validate field.data != otherfield.data

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `{other_label}` and `{other_name}` to provide a
        more helpful error.
    """

    default_message = __("This must not be the same as {other_label}")

    def compare(self, value, other):
        return value != other


class IsEmoji(object):
    """
    Validate field to contain a single emoji.

    :param message:
        Error message to raise in case of a validation error.
    """

    default_message = __("This is not a valid emoji")

    def __init__(self, message=None):
        self.message = message or self.default_message

    def __call__(self, form, field):
        if field.data not in emoji.UNICODE_EMOJI:
            raise ValidationError(self.message)


class IsPublicEmailDomain(object):
    """
    Validate that field.data belongs to a public email domain.
    If the domain lookup fails and mxsniff raises ``MXLookupException``,
    this validator will fail.

    :param message:
        Error message to raise in case of a validation error.
    """

    default_message = __("This domain is not a public email domain")

    def __init__(self, message=None, timeout=30):
        self.message = message or self.default_message
        self.timeout = timeout

    def __call__(self, form, field):
        if is_public_email_domain(field.data, default=False, timeout=self.timeout):
            return
        else:
            raise ValidationError(self.message)


class IsNotPublicEmailDomain(object):
    """
    Validate that field.data does not belong to a public email domain.
    If the domain lookup fails and mxsniff raises ``MXLookupException``, this validator
    will still pass, as we expect that most domains are not public email domains.

    :param message:
        Error message to raise in case of a validation error.
    """

    default_message = __("This domain is a public email domain")

    def __init__(self, message=None, timeout=30):
        self.message = message or self.default_message
        self.timeout = timeout

    def __call__(self, form, field):
        if not is_public_email_domain(field.data, default=False, timeout=self.timeout):
            return
        else:
            raise ValidationError(self.message)


class ValidEmail(object):
    """
    Validator to confirm an email address is likely to be valid because it is properly
    formatted and the domain exists.

    :param str message: Optional validation error message.
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        try:
            diagnosis = is_email(field.data, check_dns=True, diagnose=True)
        except (dns.resolver.Timeout, dns.resolver.NoNameservers):
            return
        if diagnosis.code == 0:
            return
        else:
            raise StopValidation(self.message or _(diagnosis.message))


# Legacy name
ValidEmailDomain = ValidEmail


class ValidUrl(object):
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
        "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 HasGeek/linkchecker"
    )

    default_message = __("The URL “{url}” is not valid or is currently inaccessible")

    default_message_urltext = __(
        "The URL “{url}” linked from “{text}” is not valid or is currently inaccessible"
    )

    default_message_schemes = __("This URL’s protocol is not allowed")

    default_message_domains = __("This URL’s domain is not allowed")

    def __init__(
        self,
        message=None,
        message_urltext=None,
        message_schemes=None,
        message_domains=None,
        invalid_urls=(),
        allowed_schemes=None,
        allowed_domains=None,
        visit_url=True,
    ):
        self.message = message or self.default_message
        self.message_urltext = message_urltext or self.default_message_urltext
        self.message_schemes = message_schemes or self.default_message_schemes
        self.message_domains = message_domains or self.default_message_domains
        self.invalid_urls = invalid_urls
        self.allowed_schemes = allowed_schemes
        self.allowed_domains = allowed_domains
        self.visit_url = visit_url

    def check_url(self, url, allowed_schemes, allowed_domains, invalid_urls, text=None):
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

        if six.PY2:
            cache_key = b'linkchecker/' + md5sum(
                url.encode('utf-8') if isinstance(url, six.text_type) else url
            )
        else:
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
            999,
        ):
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
                        if isinstance(pattern, six.string_types)
                        else pattern.search(rurl) is not None
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
        self, field, current_url, allowed_schemes, allowed_domains, invalid_urls
    ):
        error = self.check_url(
            urljoin(current_url, field.data),
            allowed_schemes,
            allowed_domains,
            invalid_urls,
        )
        if error:
            raise StopValidation(error)

    def __call__(self, form, field):
        if field.data:
            current_url = request.url if request else None
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
        self, field, current_url, allowed_schemes, allowed_domains, invalid_urls
    ):
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


class NoObfuscatedEmail(object):
    """
    Scan for obfuscated email addresses in the provided text and reject them
    """

    default_message = __("Email address identified")

    def __init__(self, message=None):
        self.message = message or self.default_message

    def __call__(self, form, field):
        emails = EMAIL_RE.findall(deobfuscate_email(field.data or ''))
        for email in emails:
            try:
                diagnosis = is_email(email, check_dns=True, diagnose=True)
                if diagnosis.code == 0:
                    raise StopValidation(self.message)
            except (dns.resolver.Timeout, dns.resolver.NoNameservers):
                pass


class ValidName(object):

    default_message = __(
        "This name contains unsupported characters. "
        "It should have letters, numbers and non-terminal hyphens only"
    )

    def __init__(self, message=None):
        self.message = message or self.default_message

    def __call__(self, form, field):
        if make_name(field.data) != field.data:
            raise StopValidation(self.message)


class ValidCoordinates(object):

    default_message = __("Valid latitude and longitude expected")
    default_message_latitude = __("Latitude must be within ± 90 degrees")
    default_message_longitude = __("Longitude must be within ± 180 degrees")

    def __init__(self, message=None, message_latitude=None, message_longitude=None):
        self.message = message or self.default_message
        self.message_latitude = message_latitude or self.default_message_latitude
        self.message_longitude = message_longitude or self.default_message_longitude

    def __call__(self, form, field):
        if len(field.data) != 2:
            raise StopValidation(self.message)
        if not -90 <= field.data[0] <= 90:
            raise StopValidation(self.message_latitude)
        if not -180 <= field.data[1] <= 180:
            raise StopValidation(self.message_longitude)
