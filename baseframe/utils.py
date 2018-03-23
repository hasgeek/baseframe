import six
from six.moves.urllib.parse import quote as urlquote
from . import asset_cache
from mxsniff import mxsniff, MXLookupException

__all__ = ['is_public_email_domain']


def get_mx(email_or_domain, default=None, timeout=30):
    """
    Returns None if the domain lookup fails and mxsniff raises ``MXLookupException``
    """
    if six.PY2:
        cache_key = 'mxrecord/' + urlquote(
            email_or_domain.encode('utf-8')
            if isinstance(email_or_domain, six.text_type) else email_or_domain,
            safe='')
    else:
        cache_key = 'mxrecord/' + urlquote(email_or_domain, safe='')

    mx_cache = asset_cache.get(cache_key)

    if mx_cache and isinstance(mx_cache, dict):
        domain = mx_cache.get('domain')
    else:
        domain = None

    if domain is None:
        # Cache entry missing or corrupted; fetch a new result and update cache
        try:
            sniffedmx = mxsniff(email_or_domain, timeout=timeout)
        except MXLookupException as e:
            # Domain lookup failed
            if default is None:
                raise e
            else:
                return
        asset_cache.set(cache_key, sniffedmx, timeout=86400)
        return sniffedmx
    else:
        # cache is fine, return it
        return mx_cache


def is_public_email_domain(email_or_domain, default=None, timeout=30):
    """
    Checks if the given domain (or domain of given email) is known to offer public email accounts

    :param email_or_domain: email address or domain name to check
    :param default: default value to return in case domain lookup fails
    :param timeout: Lookup timeout (will raise an exception if timeout happens before the check is completed and no default is provided)
    """
    sniffedmx = get_mx(email_or_domain, default=default, timeout=timeout)
    if sniffedmx is not None and any([p['public'] for p in sniffedmx['providers']]):
        return True
    else:
        # sniffedmx is only None if the domain lookup failed and a default is provided,
        # in that case return default
        return default
