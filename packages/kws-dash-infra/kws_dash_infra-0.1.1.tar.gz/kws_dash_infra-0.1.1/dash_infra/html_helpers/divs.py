from functools import partial

from dash_html_components import Div

from . import CustomElement


CustomDiv = CustomElement(Div)

Row = partial(CustomDiv, className="row")


def Col(*args, s=12, m=8, l=4, **kwargs):
    class_name = f"col s{s} m{m} l{l}"
    return CustomDiv(*args, **kwargs, className=class_name)


def Container(*args, fluid=True, **kwargs):
    return CustomDiv(*args, **kwargs, className="container")
