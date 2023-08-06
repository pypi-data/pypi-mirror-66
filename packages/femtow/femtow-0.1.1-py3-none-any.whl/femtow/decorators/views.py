import inspect

import venusian
from webob import Response

from femtow.decorators.renderers import json_renderer


def view(*, renderer=json_renderer):
    def decorator(view_func):
        def callback(scanner, name, ob):
            params = [
                scanner.app.view_params[p]
                for p in inspect.signature(view_func).parameters
            ]

            def wrapper():
                response = Response()
                evaluated_params = [p(scanner.app) for p in params]
                view_results = view_func(*evaluated_params)
                if isinstance(view_results, Response):
                    return view_results
                renderer(view_results, response)
                return response

            scanner.app.view_registry[view_func] = wrapper

        venusian.attach(view_func, callback, "femtow-views")
        return view_func

    return decorator


def view_param(view_func):
    def callback(scanner, name, ob):
        scanner.app.view_params[name] = view_func

    venusian.attach(view_func, callback, "femtow-view-params")
    return view_func
