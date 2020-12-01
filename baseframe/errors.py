from typing import Tuple, Union

from flask import current_app, redirect, request
from werkzeug.exceptions import MethodNotAllowed, NotFound
from werkzeug.routing import RequestRedirect
from werkzeug.wrappers import Response

from coaster.views import render_with

from .blueprint import baseframe
from .extensions import baseframe_translations


@baseframe.app_errorhandler(400)
@render_with('400.html.jinja2', json=True)
def error400(e) -> Tuple[dict, int]:  # TODO: Use ReturnRenderWith
    """Render a 400 error."""
    baseframe_translations.as_default()
    return {'error': "400 Bad Request"}, 400


@baseframe.app_errorhandler(403)
@render_with('403.html.jinja2', json=True)
def error403(e) -> Tuple[dict, int]:  # TODO: Use ReturnRenderWith
    """Render a 403 error."""
    baseframe_translations.as_default()
    return {'error': "403 Forbidden"}, 403


@baseframe.app_errorhandler(404)
@render_with('404.html.jinja2', json=True)
def error404(e) -> Union[Response, Tuple[dict, int]]:  # TODO: Use ReturnRenderWith
    """Render a 404 error."""
    if request.path.endswith('/') and request.method == 'GET':
        # If the URL has a trailing slash, check if there's an endpoint handler that
        # works without the slash.
        newpath = request.path[:-1]
        try:
            adapter = current_app.url_map.bind_to_environ(request)
            matchinfo = adapter.match(newpath)
            if matchinfo[0] != request.endpoint:
                # Redirect only if it's not back to the same endpoint
                redirect_url = request.base_url[:-1]
                if request.query_string:
                    redirect_url = (
                        redirect_url + '?' + request.query_string.decode('utf-8')
                    )
                return redirect(redirect_url)
        except (NotFound, RequestRedirect, MethodNotAllowed):
            pass
    baseframe_translations.as_default()
    return {'error': "404 Not Found"}, 404


@baseframe.app_errorhandler(422)
@render_with('422.html.jinja2', json=True)
def error422(e) -> Tuple[dict, int]:  # TODO: Use ReturnRenderWith
    """Render a 422 error (substitute for 400 when syntax is ok, contents not)."""
    baseframe_translations.as_default()
    return {'error': "422 Unprocessable Entity"}, 422


@baseframe.app_errorhandler(429)
@render_with('429.html.jinja2', json=True)
def error429(e) -> Tuple[dict, int]:  # TODO: Use ReturnRenderWith
    """Render a 429 error."""
    baseframe_translations.as_default()
    return {'error': "429 Too Many Requests"}, 429


@baseframe.app_errorhandler(500)
@render_with('500.html.jinja2', json=True)
def error500(e) -> Tuple[dict, int]:  # TODO: Use ReturnRenderWith
    """Render a 500 error."""
    if current_app.extensions and 'sqlalchemy' in current_app.extensions:
        current_app.extensions['sqlalchemy'].db.session.rollback()

    baseframe_translations.as_default()
    return {'error': "500 Internal Server Error"}, 500
