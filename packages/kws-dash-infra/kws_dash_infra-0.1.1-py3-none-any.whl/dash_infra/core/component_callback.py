from dash.dependencies import Output, Input, State

from .callback import Callback


class ComponentCallback(Callback):
    @classmethod
    def as_callback(cls, outputs, inputs=None, states=None):
        def wrapper(func):
            callback = cls(func)
            callback.outputs = [Output(id, prop) for id, prop in outputs]
            if inputs:
                callback.inputs = [Input(id, prop) for id, prop in inputs]

            if states:
                callback.states = [State(id, prop) for id, prop in states]
            return callback

        return wrapper
