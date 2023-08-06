from abc import ABC
from copy import deepcopy

from dash_html_components import Div

from .component_callback import ComponentCallback
from ..html_helpers.divs import Row


class Component(object):
    ids = set()

    def __init__(self, id):
        if id in self.ids:
            raise ValueError("ID already exists")

        self.ids.add(id)
        self.id = id
        self.callbacks = self.find_callbacks()

    def find_callbacks(self):
        callbacks = set()
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, ComponentCallback):
                callbacks.add(attr)

        return callbacks

    def layout(self):
        raise NotImplementedError

    @classmethod
    def from_config(cls, config):
        id = config.get("id")
        if id is None:
            raise AttributeError("No id provided in config")
        component = cls(id)
        for key, value in config.items():
            component.__setattr__(key, value)

        return component


def as_component(dash_object, id, *args, container=Div, **kwargs):
    class Wrapper(Component):
        def layout(self):
            return container([dash_object(id=id)])

    return Wrapper(id)
