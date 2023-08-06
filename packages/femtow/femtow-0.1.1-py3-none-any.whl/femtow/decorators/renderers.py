import json
import os
from pathlib import Path

from mako.template import Template

TEMPLATE_PATH = Path(os.path.split(__file__)[0]).parents[0] / "templates"


def string_(view_dict, response):
    response.text = view_dict


def json_renderer(view_dict, response):
    response.text = json.dumps(view_dict)
    response.headers["Content-Type"] = "application/json; charset=UTF-8"


def mako_renderer(template):
    template = Template(filename=template)

    def mako_renderer_(view_dict, response):
        response.text = template.render(**view_dict)

    return mako_renderer_


def http_exception_renderer(status):

    template = Template(filename=str(TEMPLATE_PATH / "http-exception.mako"))

    def http_exception_renderer_(view_dict, response):
        response.text = template.render(status=status, **view_dict)
        response.status = status

    return http_exception_renderer_
