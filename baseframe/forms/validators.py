# -*- coding: utf-8 -*-

import re
from urllib import quote as urlquote
from urlparse import urljoin
import dns.resolver
from pyisemail import is_email
from flask import request
from wtforms.validators import (DataRequired, InputRequired, Optional, Length, EqualTo, URL, NumberRange,
    ValidationError, StopValidation)
import requests
from lxml import html
from coaster.utils import make_name, deobfuscate_email
from .. import b_ as _, b__ as __, asset_cache
from ..signals import exception_catchall


__all__ = ['OptionalIf', 'OptionalIfNot', 'ValidEmail', 'ValidEmailDomain', 'ValidUrl', 'AllUrlsValid',
    'ValidName', 'NoObfuscatedEmail', 'ValidCoordinates',
    # WTForms validators
    'DataRequired', 'InputRequired', 'Optional', 'Length', 'EqualTo', 'URL', 'NumberRange',
    'ValidationError', 'StopValidation']


EMAIL_RE = re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,63}\b', re.I)


class OptionalIf(object):
    """
    Validator that makes this field optional if the value of some other field is true.
    """
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message or __("This is required")

    def __call__(self, form, field):
        if not field.data:
            if form[self.fieldname].data:
                raise StopValidation()
            else:
                raise StopValidation(self.message)


class OptionalIfNot(OptionalIf):
    """
    Validator that makes this field optional if the value of some other field is false.
    """
    def __call__(self, form, field):
        if not field.data:
            if form[self.fieldname].data:
                raise StopValidation()
            else:
                raise StopValidation(self.message)


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
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
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
    Validator to confirm a URL is valid (returns 2xx status code)

    :param unicode message: Error message (None for default error message)
    :param unicode message_urltext: Unused parameter, only used in the :class:`AllUrlsValid` validator
    :param list invalid_urls: A list of (patterns, message) tuples for URLs that will be rejected,
        where ``patterns`` is a list of strings or regular expressions. If ``invalid_urls`` is
        a callable, it will be called to retrieve the list.
    """
    user_agent = 'HasGeek/linkchecker'

    def __init__(self, message=None, message_urltext=None, invalid_urls=[]):
        self.message = message or _(u'The URL “{url}” is not valid or is currently inaccessible')
        self.invalid_urls = invalid_urls
        self.message_urltext = message_urltext or _(u'The URL “{url}” linked from “{text}” is not valid or is currently inaccessible')

    def check_url(self, invalid_urls, url, text=None):
        cache_key = 'linkchecker/' + urlquote(url.encode('utf-8') if isinstance(url, unicode) else url, safe='')
        cache_check = asset_cache.get(cache_key)
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
                r = requests.get(url, timeout=30, allow_redirects=True, verify=False, headers={'User-Agent': self.user_agent})
                code = r.status_code
                rurl = r.url
            except (requests.exceptions.MissingSchema,    # Still a relative URL? Must be broken
                    requests.exceptions.ConnectionError,  # Name resolution or connection failed
                    requests.exceptions.Timeout):         # Didn't respond in time
                code = None
            except Exception as e:
                exception_catchall.send(e)
                code = None

        if rurl is not None and code in (200, 201, 202, 203, 204, 205, 206, 207, 208, 226, 999):
            # 999 is a non-standard too-many-requests error. We can't look past it to
            # check a URL, so we let it pass

            # The URL works, so now we check if it's in a reject list
            for patterns, message in invalid_urls:
                for pattern in patterns:
                    # For text patterns, do a substring search. For regex patterns (assumed so if not text),
                    # do a regex search. Test with the final URL from the response, after redirects,
                    # but report errors using the URL the user provided
                    if (isinstance(pattern, basestring) and pattern in rurl) or (pattern.search(rurl) is not None):
                        return message.format(url=url, text=text)
            # All good. The URL works and isn't invalid, so save to cache and return without an error message
            asset_cache.set(cache_key, {'url': rurl, 'code': code}, timeout=86400)
            return
        else:
            if text is not None and url != text:
                return self.message_urltext.format(url=url, text=text)
            else:
                return self.message.format(url=url)

    def call_inner(self, field, current_url, invalid_urls):
        error = self.check_url(invalid_urls, urljoin(current_url, field.data))
        if error:
            raise StopValidation(error)

    def __call__(self, form, field):
        if field.data:
            current_url = request.url if request else None
            invalid_urls = self.invalid_urls() if callable(self.invalid_urls) else self.invalid_urls

            return self.call_inner(field, current_url, invalid_urls)


class AllUrlsValid(ValidUrl):
    """
    Validator to confirm all URLs in a HTML snippet are valid because loading
    them returns 2xx status codes.

    :param unicode message: Error message (None for default error message)
    :param unicode message_urltext: Error message when the URL also has text (None to use default)
    :param list invalid_urls: A list of (patterns, message) tuples for URLs that will be rejected,
        where ``patterns`` is a list of strings or regular expressions. If ``invalid_urls`` is
        a callable, it will be called to retrieve the list.
    """
    def call_inner(self, field, current_url, invalid_urls):
        html_tree = html.fromstring(field.data)
        for text, href in [(atag.text_content(), atag.attrib.get('href')) for atag in html_tree.xpath("//a")]:
            error = self.check_url(invalid_urls, urljoin(current_url, href), text)
            if error:
                field.errors.append(error)
        if field.errors:
            raise StopValidation()


class NoObfuscatedEmail(object):
    """
    Scan for obfuscated email addresses in the provided text and reject them
    """
    def __init__(self, message=None):
        if not message:
            message = __(u"Email address identified")
        self.message = message

    def __call__(self, form, field):
        emails = EMAIL_RE.findall(deobfuscate_email(field.data or u''))
        for email in emails:
            try:
                diagnosis = is_email(email, check_dns=True, diagnose=True)
                if diagnosis.code == 0:
                    raise StopValidation(self.message)
            except (dns.resolver.Timeout, dns.resolver.NoNameservers):
                pass


class ValidName(object):
    def __init__(self, message=None):
        if not message:
            message = __(u"This name contains unsupported characters. "
                u"It should have letters, numbers and non-terminal hyphens only")
        self.message = message

    def __call__(self, form, field):
        if make_name(field.data) != field.data:
            raise StopValidation(self.message)


class ValidCoordinates(object):
    def __init__(self, message=None, message_latitude=None, message_longitude=None):
        self.message = message or __(u"Valid latitude and longitude expected")
        self.message_latitude = message_latitude or __(u"Latitude must be within ± 90 degrees")
        self.message_longitude = message_longitude or __(u"Longitude must be within ± 180 degrees")

    def __call__(self, form, field):
        if len(field.data) != 2:
            raise StopValidation(self.message)
        if not -90 <= field.data[0] <= 90:
            raise StopValidation(self.message_latitude)
        if not -180 <= field.data[1] <= 180:
            raise StopValidation(self.message_longitude)
