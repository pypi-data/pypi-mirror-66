from typing import Callable

import logging
import pathlib
import pkgutil
from dataclasses import dataclass

import backlash
import venusian
from routes import Mapper
from webob import Request
from webob.exc import HTTPNotFound

from femtow import defaults

logger = logging.getLogger(__file__)


@dataclass
class FemtowConfig:
    import_name: str
    debug: bool = False

    @property
    def working_path(self) -> pathlib.Path:
        loader = pkgutil.get_loader(self.import_name)
        return pathlib.Path(loader.get_filename(self.import_name)).absolute().parents[0]


class Femtow:
    def __init__(self, import_name: str, config: FemtowConfig = None) -> None:
        self.config = config or FemtowConfig(import_name)

        self.current_request = None
        self.exception_view_registry = {}
        self.route_mapper = Mapper()

        self.view_params = {}
        self.view_registry = {}

        self._scanner = venusian.Scanner(app=self)
        self._config = config
        self._app = self._femtow

        if self.config.debug:
            self._app = backlash.DebuggedApplication(
                self._femtow, context_injectors=[self._femtow_backlash_context]
            )

    def __call__(self, environ: dict, start_response: Callable) -> "webob.Response":
        return self._app(environ, start_response)

    def _femtow(self, environ: dict, start_response: Callable) -> "webob.Response":
        self.current_request = request = Request(environ)
        try:
            response = self._build_response(request, environ)
        except Exception as e:
            logger.exception(e)
            response = self._build_exception_response(request, e)

        return response(environ, start_response)

    def scan(self, package) -> None:
        self._scanner.scan(defaults.view_params, categories=["femtow-view-params"])

        self._scanner.scan(package, categories=["femtow-view-params"])
        self._scanner.scan(package, categories=["femtow-views"])
        self._scanner.scan(package, categories=["femtow-routes"])

    def _build_response(self, request: Request, environ: dict) -> Callable:
        match_dict = self.route_mapper.match(request.path, environ)
        if not match_dict:
            raise HTTPNotFound(f"No route for path ${request.path} configured.")
        view = match_dict.pop("action")
        request.match_dict = match_dict
        return view()

    def _build_exception_response(
        self, request: Request, exception: Exception
    ) -> Callable:
        request.exception = exception
        try:
            return self._get_exception_view(exception)()
        except StopIteration:  # TODO: Raise a different exception in get_exception_view
            raise exception

    def _get_exception_view(self, exception: Exception) -> Callable:
        return next(
            view
            for exception_class, view in self.exception_view_registry.items()
            if isinstance(exception, exception_class)
        )

    @staticmethod
    def _femtow_backlash_context(environ: dict) -> dict:
        return {"request": Request(environ)}
