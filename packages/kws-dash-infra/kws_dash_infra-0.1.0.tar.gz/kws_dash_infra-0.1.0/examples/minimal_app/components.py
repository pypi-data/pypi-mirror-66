from dash_core_components import Graph, Slider

from dash_infra import Component, ComponentCallback
from dash_infra.components.groups import ComponentGroup
from dash_infra.html_helpers.divs import CustomDiv as Div
from dash_infra.html_helpers.divs import Col


class GraphComponent(Component):
    @ComponentCallback.as_callback(outputs=[("test", "children")])
    def test(self):
        return 42

    def layout(self):
        return Col([Graph(id=self.id)])


class SliderComponent(Component):
    def layout(self):
        return Col(Slider(id=self.id))


graph_square = GraphComponent("square")
graph_cube = GraphComponent("cube")
slider = SliderComponent("input")
group = ComponentGroup("main", slider, graph_square, graph_cube)
