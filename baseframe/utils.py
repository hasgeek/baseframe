# -*- coding: utf-8 -*-
from __future__ import absolute_import
from six.moves.urllib.parse import quote as urlquote
import six

from flask import g

from mxsniff import MXLookupException, mxsniff

from coaster.utils import utcnow

from . import asset_cache

__all__ = ['request_timestamp', 'is_public_email_domain']


def request_timestamp():
    """
    Return a UTC timestamp for the request
    """
    if not g:
        return utcnow()
    ts = getattr(g, 'request_timestamp', None)
    if ts is None:
        ts = utcnow()
        g.request_timestamp = ts
    return ts


def is_public_email_domain(email_or_domain, default=None, timeout=30):
    """
    Checks if the given domain (or domain of given email) is known to offer public email accounts.
    All MX lookup results are cached for one day. An exception is raised if timeout happens
    before the check is completed or domain lookup fails, and no default is provided.

    :param email_or_domain: Email address or domain name to check
    :param default: Default value to return in case domain lookup fails
    :param timeout: Lookup timeout
    :raises MXLookupException: If a DNS lookup error happens and no default is specified
    """
    if six.PY2:
        cache_key = 'mxrecord/' + urlquote(
            email_or_domain.encode('utf-8')
            if isinstance(email_or_domain, six.text_type)
            else email_or_domain,
            safe='',
        )
    else:
        cache_key = 'mxrecord/' + urlquote(email_or_domain, safe='')

    try:
        sniffedmx = asset_cache.get(cache_key)
    except ValueError:  # Possible error from Py2 vs Py3 pickle mismatch
        sniffedmx = None

    if sniffedmx is None or not isinstance(sniffedmx, dict):
        # Cache entry missing or corrupted; fetch a new result and update cache
        try:
            sniffedmx = mxsniff(email_or_domain, timeout=timeout)
            asset_cache.set(cache_key, sniffedmx, timeout=86400)  # cache for a day
        except MXLookupException as e:
            # Domain lookup failed
            if default is None:
                raise e
            else:
                return default

    if any(p['public'] for p in sniffedmx['providers']):
        return True
    else:
        return False
