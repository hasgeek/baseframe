# -*- coding: utf-8 -*-

import dns.resolver
from urlparse import urljoin
from flask import request
import wtforms
import requests
from lxml import html
from coaster import make_name, get_email_domain
from .. import b__ as __
from .. import b_ as _
from ..signals import exception_catchall


__all__ = ['ValidEmailDomain', 'ValidUrl', 'AllUrlsValid', 'StripWhitespace', 'ValidName']


class ValidEmailDomain(object):
    """
    Validator to confirm an email address is likely to be valid because its
    domain exists and has an MX record.

    :param str message: Optional validation error message. If supplied, this message overrides the following three
    :param str message_invalid: Message if the email address is invalid
    :param str message_domain: Message if domain is not found
    :param str message_email: Message if domain does not have an MX record
    """
    message_invalid = __(u"That is not a valid email address")
    message_domain = __(u"That domain does not exist")
    message_email = __(u"That email address does not exist")

    def __init__(self, message=None, message_invalid=None, message_domain=None, message_email=None):
        self.message = message
        if message_invalid:
            self.message_invalid = message_invalid
        if message_domain:
            self.message_domain = message_domain
        if message_email:
            self.message_email = message_email

    def __call__(self, form, field):
        email_domain = get_email_domain(field.data)
        if not email_domain:
            raise wtforms.validators.StopValidation(self.message or self.message_invalid)
        try:
            dns.resolver.query(email_domain, 'MX')
        except dns.resolver.NXDOMAIN:
            raise wtforms.validators.StopValidation(self.message or self.message_domain)
        except dns.resolver.NoAnswer:
            raise wtforms.validators.StopValidation(self.message or self.message_email)
        except (dns.resolver.Timeout, dns.resolver.NoNameservers):
            pass


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
                r = requests.head(url, timeout=30, allow_redirects=True, headers={'User-Agent': ua})
                code = r.status_code
                if code == 405:  # Some servers don't like HTTP HEAD requests, strange but true
                    r = requests.get(url, timeout=30, allow_redirects=True, headers={'User-Agent': ua})
                    code  =r.status_code
            except (requests.exceptions.MissingSchema,    # Still a relative URL? Must be broken
                    requests.exceptions.ConnectionError,  # Name resolution or connection failed
                    requests.exceptions.Timeout):         # Didn't respond in time
                code = None
            except Exception as e:
                exception_catchall.send(e)
                code = None

            if code not in (200, 201, 202, 203, 204, 205, 206, 207, 208, 226):
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
                    r = requests.head(url, timeout=30, allow_redirects=True, headers={'User-Agent': ua})
                    code = r.status_code
                    if code == 405:  # Some servers don't like HTTP HEAD requests, strange but true
                        r = requests.get(url, timeout=30, allow_redirects=True, headers={'User-Agent': ua})
                        code  =r.status_code
                except (requests.exceptions.MissingSchema,    # Still a relative URL? Must be broken
                        requests.exceptions.ConnectionError,  # Name resolution or connection failed
                        requests.exceptions.Timeout):         # Didn't respond in time
                    code = None
                except Exception as e:
                    exception_catchall.send(e)
                    code = None

                if code not in (200, 201, 202, 203, 204, 205, 206, 207, 208, 226):
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
            message = __("Name contains unsupported characters")
        self.message = message

    def __call__(self, form, field):
        if make_name(field.data) != field.data:
            raise wtforms.validators.StopValidation(self.message)
