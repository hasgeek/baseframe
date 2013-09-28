# -*- coding: utf-8 -*-

import dns.resolver
import wtforms
from coaster import make_name, get_email_domain
from .. import b__ as __

__all__ = ['ValidEmailDomain', 'StripWhitespace', 'ValidName']


class ValidEmailDomain(object):
    """
    Validator to confirm an email address is likely to be valid because its
    domain exists and has an MX record.
    """
    message_domain = __(u"That domain does not exist")
    message_email = __(u"That email address does not exist")

    def __init__(self, message=None, message_domain=None, message_email=None):
        self.message = message
        if message_domain:
            self.message_domain = message_domain
        if message_email:
            self.message_email = message_email

    def __call__(self, form, field):
        email_domain = get_email_domain(field.data)
        try:
            dns.resolver.query(email_domain, 'MX')
        except dns.resolver.NXDOMAIN:
            raise wtforms.ValidationError(self.message or self.message_domain)
        except dns.resolver.NoAnswer:
            raise wtforms.ValidationError(self.message or self.message_email)
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
            message = __("Name contains unsupported characters")
        self.message = message

    def __call__(self, form, field):
        if make_name(field.data) != field.data:
            raise wtforms.ValidationError(self.message)
