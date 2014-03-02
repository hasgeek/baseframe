# -*- coding: utf-8 -*-

from . import b_ as _
from . import baseframe, current_app
from flask import Markup, request
from datetime import datetime
import os
from coaster.gfm import markdown

@baseframe.app_template_filter('age')
def age(dt):
    delta = datetime.utcnow() - dt
    if delta.days == 0:
        # < 1 day
        if delta.seconds < 10:
            return _(u"seconds ago")
        elif delta.seconds < 60:
            return _(u"%(num)s seconds ago", num=delta.seconds)
        elif delta.seconds < 120:
            return _(u"a minute ago")
        elif delta.seconds < 3600:  # < 1 hour
            return _(u"%(num)s minutes ago", num=int(delta.seconds / 60))
        elif delta.seconds < 7200:  # < 2 hours
            return _(u"an hour ago")
        else:
            return _("%(num)s hours ago", num=int(delta.seconds / 3600))
    elif delta.days == 1:
        return _(u"a day ago")
    elif delta.days < 30:
        return _(u"%(num)s days ago", num=delta.days)
    elif delta.days < 60:
        return _(u"a month ago")
    elif delta.days < 365:
        return _(u"%(num)s months ago", num=int(delta.days / 30))
    elif delta.days < 730:  # < 2 years
        return _(u"a year ago")
    else:
        return _(u"%(num)s years ago", num=int(delta.days / 365))


@baseframe.app_template_filter('usessl')
def usessl(url):
    """
    Convert a URL to https:// if SSL is enabled in site config
    """
    if not current_app.config.get('USE_SSL'):
        return url
    if url.startswith('//'):  # //www.example.com/path
        return 'https:' + url
    if url.startswith('/'):  # /path
        url = os.path.join(request.url_root, url[1:])
    if url.startswith('http:'):  # http://www.example.com
        url = 'https:' + url[5:]
    return url


@baseframe.app_template_filter('nossl')
def nossl(url):
    """
    Convert a URL to http:// if using SSL
    """
    if url.startswith('//'):
        return 'http:' + url
    if url.startswith('/') and request.url.startswith('https:'):  # /path and SSL is on
        url = os.path.join(request.url_root, url[1:])
    if url.startswith('https://'):
        return 'http:' + url[6:]
    return url


@baseframe.app_template_filter('render_field_options')
def render_field_options(field, **kwargs):
    """
    Remove HTML attributes with a value of None or False before rendering a field.
    """
    d = dict((k, v) for k, v in kwargs.items() if v is not None and v is not False)
    return field(**d)


@baseframe.app_template_filter('to_json')
def form_field_to_json(field, **kwargs):
    d = {}
    d['id'] = field.id
    d['label'] = field.label.text
    d['has_errors'] = bool(field.errors)
    d['errors'] = list(dict(error=e) for e in field.errors)
    d['is_listwidget'] = bool(hasattr(field.widget, 'html_tag') and field.widget.html_tag in ['ul', 'ol'])
    try:
    	d['is_checkbox'] = (field.widget.input_type == 'checkbox')
    except AttributeError:
    	d['is_checkbox'] = False
    d['is_required'] = bool(field.flags.required)
    d['render_html'] = Markup(render_field_options(field, **kwargs))
    return d

@baseframe.app_template_filter('markdown')
def field_markdown(field, **kwargs):
    html = markdown(field)
    return Markup(html)