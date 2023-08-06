import traceback
from webob.exc import HTTPNotFound

from femtow.decorators import exception_route, view, http_exception_renderer


@exception_route(exception=HTTPNotFound)
@view(renderer=http_exception_renderer(status=404))
def http_not_found():
    return {"tb": [], "msg": "HTTP Not Found"}


@exception_route(exception=Exception)
@view(renderer=http_exception_renderer(status=500))
def http_internal_server_error(request):
    tb = traceback.format_tb(request.exception.__traceback__)
    return {"tb": tb, "msg": "Internal Server Error"}
