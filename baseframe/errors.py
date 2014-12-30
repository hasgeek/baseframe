# -*- coding: utf-8 -*-

from . import baseframe, current_app, baseframe_translations
from flask import request, redirect
from coaster.views import render_with
from werkzeug.routing import NotFound, MethodNotAllowed, RequestRedirect


@baseframe.app_errorhandler(404)
@render_with('404.html', json=True)
def error404(e):
    if request.path.endswith('/') and request.method == 'GET':
        newpath = request.path[:-1]
        try:
            adapter = current_app.url_map.bind_to_environ(request)
            matchinfo = adapter.match(newpath)
            if matchinfo[0] != request.endpoint:
                # Redirect only if it's not back to the same endpoint
                return redirect(request.url[:-1])
        except (NotFound, RequestRedirect, MethodNotAllowed):
            pass
    baseframe_translations.as_default()
    return {'error': "404 Not Found"}, 404


@baseframe.app_errorhandler(403)
@render_with('403.html', json=True)
def error403(e):
    baseframe_translations.as_default()
    return {'error': "403 Forbidden"}, 403


@baseframe.app_errorhandler(500)
@render_with('500.html', json=True)
def error500(e):
    baseframe_translations.as_default()
    return {'error': "500 Internal Server Error"}, 500
