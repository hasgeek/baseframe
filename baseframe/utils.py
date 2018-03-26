# -*- coding: utf-8 -*-
from __future__ import absolute_import
import six
from six.moves.urllib.parse import quote as urlquote

from mxsniff import mxsniff, MXLookupException

from . import asset_cache

__all__ = ['is_public_email_domain']


def is_public_email_domain(email_or_domain, default=None, timeout=30):
    """
    Checks if the given domain (or domain of given email) is known to offer public email accounts

    :param email_or_domain: email address or domain name to check
    :param default: default value to return in case domain lookup fails
    :param timeout: Lookup timeout (will raise an exception if timeout happens before the check is completed and no default is provided)
    """
    if six.PY2:
        cache_key = 'mxrecord/' + urlquote(
            email_or_domain.encode('utf-8')
            if isinstance(email_or_domain, six.text_type) else email_or_domain,
            safe='')
    else:
        cache_key = 'mxrecord/' + urlquote(email_or_domain, safe='')

    sniffedmx = asset_cache.get(cache_key)

    if sniffedmx is None or not isinstance(sniffedmx, dict):
        # Cache entry missing or corrupted; fetch a new result and update cache
        try:
            sniffedmx = mxsniff(email_or_domain, timeout=timeout)
        except MXLookupException as e:
            # Domain lookup failed
            if default is None:
                raise e
        asset_cache.set(cache_key, sniffedmx, timeout=86400)

    if any([p['public'] for p in sniffedmx['providers']]):
        return True
    else:
        # in that case return default
        return default
