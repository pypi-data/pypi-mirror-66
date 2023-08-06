from typing import Callable
import inspect

import venusian


def route(route_name: str, route_path: str, methods: tuple = ("GET",)) -> Callable:
    def decorator(view_func: Callable) -> Callable:
        def callback(scanner, name, ob):
            conditions = {"method": methods}
            try:
                decorated_view_func = scanner.app.view_registry[view_func]
            except KeyError:
                view_import_path = (
                    f"{inspect.getmodule(view_func).__name__}.{view_func.__name__}"
                )
                raise Exception(
                    f'Could not associate route "{route_name}" with unconfigured view "{view_import_path}".'
                )

            route_mapper = scanner.app.route_mapper
            # TODO: This is a dirty hack, shouldn't access private members. Need to find a better way.
            if route_name in route_mapper._routenames:
                # TODO: Add custom exception with more details.
                raise Exception(f'Route name "{route_name}" is already in use.')
            scanner.app.route_mapper.connect(
                route_name,
                route_path,
                conditions=conditions,
                action=decorated_view_func,
            )

        venusian.attach(view_func, callback, "femtow-routes")
        return view_func

    return decorator


def exception_route(exception: Exception) -> Callable:
    def decorator(view_func: Callable) -> Callable:
        def callback(scanner, name, ob):
            decorated_view_func = scanner.app.view_registry[view_func]
            scanner.app.exception_view_registry[exception] = decorated_view_func

        venusian.attach(view_func, callback, "femtow-routes")
        return view_func

    return decorator
