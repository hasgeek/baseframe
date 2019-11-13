# -*- coding: utf-8 -*-

from flask import redirect, request
from werkzeug.routing import MethodNotAllowed, NotFound, RequestRedirect

from coaster.views import render_with

from . import baseframe, baseframe_translations, current_app


@baseframe.app_errorhandler(404)
@render_with('404.html.jinja2', json=True)
def error404(e):
    if request.path.endswith('/') and request.method == 'GET':
        newpath = request.path[:-1]
        try:
            adapter = current_app.url_map.bind_to_environ(request)
            matchinfo = adapter.match(newpath)
            if matchinfo[0] != request.endpoint:
                # Redirect only if it's not back to the same endpoint
                redirect_url = request.base_url[:-1]
                if request.query_string:
                    redirect_url = redirect_url + u'?' + request.query_string
                return redirect(redirect_url)
        except (NotFound, RequestRedirect, MethodNotAllowed):
            pass
    baseframe_translations.as_default()
    return {'error': "404 Not Found"}, 404


@baseframe.app_errorhandler(403)
@render_with('403.html.jinja2', json=True)
def error403(e):
    baseframe_translations.as_default()
    return {'error': "403 Forbidden"}, 403


@baseframe.app_errorhandler(500)
@render_with('500.html.jinja2', json=True)
def error500(e):
    if current_app.extensions and 'sqlalchemy' in current_app.extensions:
        current_app.extensions['sqlalchemy'].db.session.rollback()

    baseframe_translations.as_default()
    return {'error': "500 Internal Server Error"}, 500
