from dash_infra import Component, as_component
from dash_infra.components import ComponentGroup
from dash_infra.html_helpers.divs import Row, Col
from dash_core_components import Slider
from dash_html_components import Div
from dash_infra.components.storage import PickleStorage

store = PickleStorage("store")
slider = as_component(Slider, "input", container=Col)
square_div = as_component(Div, "square", container=Col)
cube_div = as_component(Div, "cube", container=Col)
sqrt_div = as_component(Div, "sqrt", container=Col)
sum_div = as_component(Div, "sum", container=Col)

group = ComponentGroup("main", slider, square_div, cube_div, sqrt_div,)
