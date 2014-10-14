# -*- coding: utf-8 -*-

import re
from urlparse import urljoin
import dns.resolver
from pyisemail import is_email
from flask import request
import wtforms
import requests
from lxml import html
from coaster.utils import make_name, deobfuscate_email
from .. import b__ as __
from .. import b_ as _
from ..signals import exception_catchall


__all__ = ['ValidEmail', 'ValidEmailDomain', 'ValidUrl', 'AllUrlsValid', 'StripWhitespace', 'ValidName', 'NoObfuscatedEmail']


EMAIL_RE = re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,63}\b', re.I)


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
            raise wtforms.validators.StopValidation(self.message or _(diagnosis.message))


# Legacy name
ValidEmailDomain = ValidEmail


class ValidUrl(object):
    """
    Validator to confirm a URL is valid (returns 2xx status code)
    """
    def __init__(self, message=None, invalid_urls=[]):
        self.message = message
        self.invalid_urls = invalid_urls

        if self.message is None:
            self.message = _(u'The URL “{url}” is not valid or is currently inaccessible')

    def __call__(self, form, field):
        if field.data:
            try:
                current_url = request.url
            except RuntimeError:
                current_url = None

            invalid_urls = self.invalid_urls
            if callable(invalid_urls):
                invalid_urls = invalid_urls()

            url = urljoin(current_url, field.data)  # Clean up relative URLs
            ua = 'HasGeek/linkchecker'

            r = None
            try:
                r = requests.head(url, timeout=30, allow_redirects=True, verify=False, headers={'User-Agent': ua})
                code = r.status_code
                if code in (405, 502):  # Some servers don't like HTTP HEAD requests, strange but true
                    r = requests.get(url, timeout=30, allow_redirects=True, verify=False, headers={'User-Agent': ua})
                    code = r.status_code
            except (requests.exceptions.MissingSchema,    # Still a relative URL? Must be broken
                    requests.exceptions.ConnectionError,  # Name resolution or connection failed
                    requests.exceptions.Timeout):         # Didn't respond in time
                code = None
            except Exception as e:
                exception_catchall.send(e)
                code = None

            if code not in (200, 201, 202, 203, 204, 205, 206, 207, 208, 226, 999):
                # 999 is a non-standard too-many-requests error. We can't do anything
                # about it, so let it pass.
                raise wtforms.validators.StopValidation(self.message.format(url=field.data))
            elif r is not None:
                # If load succeeded, confirm that the final URL (after expanding short URLs)
                # is not in the invalid_urls list
                for patterns, message in invalid_urls:
                    for pattern in patterns:
                        if isinstance(pattern, basestring) and pattern in r.url:
                            field.errors.append(message.format(url=url))
                        elif pattern.search(r.url) is not None:
                            field.errors.append(message.format(url=url))


class AllUrlsValid(object):
    """
    Validator to confirm all URLs in a HTML snippet are valid because loading
    them returns 2xx status codes.

    :param unicode message: Error message (None for default error message)
    :param unicode message_urltext: Error message when the URL also has text (None to use default)
    :param list invalid_urls: A list of (patterns, message) tuples for URLs that will be rejected,
        where ``patterns`` is a list of strings or regular expressions. If ``invalid_urls`` is
        a callable, it will be called to retrieve the list.
    """
    def __init__(self, message=None, message_urltext=None, invalid_urls=[]):
        self.message = message
        self.message_urltext = message_urltext
        self.invalid_urls = invalid_urls

        if self.message is None:
            self.message = _(u'The URL “{url}” is not valid or is currently inaccessible')

        if self.message_urltext is None:
            self.message_urltext = _(u'The URL “{url}” linked from “{text}” is not valid or is currently inaccessible')

    def __call__(self, form, field):
        if field.data:
            try:
                current_url = request.url
            except RuntimeError:
                current_url = None

            invalid_urls = self.invalid_urls
            if callable(invalid_urls):
                invalid_urls = invalid_urls()

            html_tree = html.fromstring(field.data)
            for text, href in [(atag.text_content(), atag.attrib.get('href')) for atag in html_tree.xpath("//a")]:
                url = urljoin(current_url, href)  # Clean up relative URLs
                ua = 'HasGeek/linkchecker'

                r = None
                try:
                    r = requests.head(url, timeout=30, allow_redirects=True, verify=False, headers={'User-Agent': ua})
                    code = r.status_code
                    if code in (405, 502):  # Some servers don't like HTTP HEAD requests, strange but true
                        r = requests.get(url, timeout=30, allow_redirects=True, verify=False, headers={'User-Agent': ua})
                        code = r.status_code
                except (requests.exceptions.MissingSchema,    # Still a relative URL? Must be broken
                        requests.exceptions.ConnectionError,  # Name resolution or connection failed
                        requests.exceptions.Timeout):         # Didn't respond in time
                    code = None
                except Exception as e:
                    exception_catchall.send(e)
                    code = None

                if code not in (200, 201, 202, 203, 204, 205, 206, 207, 208, 226, 999):
                    # 999 is a non-standard too-many-requests error. We can't do anything
                    # about it, so let it pass.
                    if url == text:
                        field.errors.append(self.message.format(url=href))
                    else:
                        field.errors.append(self.message_urltext.format(url=href, text=text))
                elif r is not None:
                    # If load succeeded, confirm that the final URL (after expanding short URLs)
                    # is not in the invalid_urls list
                    for patterns, message in invalid_urls:
                        for pattern in patterns:
                            if isinstance(pattern, basestring) and pattern in r.url:
                                field.errors.append(message.format(url=url, text=text))
                            elif pattern.search(r.url) is not None:
                                field.errors.append(message.format(url=url, text=text))


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
                    raise wtforms.validators.StopValidation(self.message)
            except (dns.resolver.Timeout, dns.resolver.NoNameservers):
                pass


class StripWhitespace(object):
    def __init__(self, left=True, right=True):
        self.left = left
        self.right = right

    def __call__(self, form, field):
        if self.left:
            field.data = field.data.lstrip()
        if self.right:
            field.data = field.data.rstrip()


class ValidName(object):
    def __init__(self, message=None):
        if not message:
            message = __(u"This name contains unsupported characters. "
                u"It should have letters, numbers and non-terminal hyphens only")
        self.message = message

    def __call__(self, form, field):
        if make_name(field.data) != field.data:
            raise wtforms.validators.StopValidation(self.message)
