import codecs
import pickle

from dash.dependencies import Input, Output
from dash_html_components import Div

from dash_infra import Component, ComponentCallback


class Storage(Component):
    def __init__(self, id):
        super().__init__(id)
        self.callback_map = dict()
        self.html_storage = []

    def layout(self):
        return Div(self.html_storage, id=self.id, className="hide")

    def _serializer(self, *outputs):
        raise NotImplementedError

    def _deserializer(self, encoded_input):
        raise NotImplementedError

    def create_storage_callback(self, callback, key=None):
        key = key or callback.func.__name__
        storage_key = f"{self.id}-{key}"
        self.html_storage.append(Div(id=storage_key, className="hide"))

        self.callbacks.add(
            ComponentCallback(
                self._serializer,
                inputs=[
                    Input(o.component_id, o.component_property)
                    for o in callback.dash_outputs
                ],
                outputs=[Output(storage_key, "children")],
            )
        )
        return storage_key

    def add_deserializer(self, callback):
        old_func = callback._pre_function_hook

        def wrapper(*encoded_input):
            inputs = self._deserializer(*encoded_input)
            return old_func(*inputs)

        callback._pre_function_hook = wrapper

    def storage_key(self, key):
        return f"{self.id}-{key}"


class PickleStorage(Storage):
    def _serializer(self, *outputs):
        if len(outputs) == 1:
            outputs = outputs[0]

        return pickle.dumps(outputs, 0).decode()

    def _deserializer(self, *encoded_inputs):
        return [pickle.loads(inp.encode()) for inp in encoded_inputs]
