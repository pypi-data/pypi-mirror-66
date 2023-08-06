from copy import deepcopy
from typing import Dict

from dash import Dash
from dash_html_components import Div

from dash_infra.components import ComponentGroup
from ..html_helpers.divs import Container


class KWSDashApp:
    def __init__(self, name="Default Dash App", doc=""):
        self.name = name
        self.component_layouts = []
        self.component_callbacks = []
        self.api_callbacks = []
        self.doc = doc

    def register_component(self, group_or_component, top=True):
        if top:
            self.component_layouts.append(group_or_component.layout())

        for callback in group_or_component.callbacks:
            self.component_callbacks.append(callback)

        if isinstance(group_or_component, ComponentGroup):
            for component in group_or_component.components:
                self.register_component(component, top=False)

    def register_callback(self, callback, outputs, inputs=None, states=None):
        callback = deepcopy(callback)
        callback.register(outputs, inputs, states)
        self.api_callbacks.append(callback)
        return callback

    def instanciate(self, *args, **kwargs):
        app = Dash(
            *args,
            **kwargs,
            suppress_callback_exceptions=True,
            external_stylesheets=[
                "https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"
            ],
            external_scripts=[
                "https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js",
            ]
        )

        for callback in self.component_callbacks + self.api_callbacks:
            app.callback(
                callback.dash_outputs, callback.dash_inputs, callback.dash_states
            )(callback.run)

        app.layout = Container(self.component_layouts, id="main")

        return app

    def run_server(self, *args, **kwargs):
        return self.instanciate().run_server(*args, **kwargs)
