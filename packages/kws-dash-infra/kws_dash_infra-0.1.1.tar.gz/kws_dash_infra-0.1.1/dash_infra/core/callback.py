from functools import wraps
from inspect import signature, Signature

from dash.dependencies import Input, Output, State


class Callback(object):
    def __init__(self, func=None, inputs=None, outputs=None, states=None):
        self.dash_inputs = inputs or []
        self.dash_outputs = outputs or []
        self.dash_states = states or []
        self.current_inputs = []
        self.func = func

    def pre_function_hook(self, *inputs):
        assert len(inputs) == (len(self.dash_inputs) + len(self.dash_states))
        self.current_inputs = inputs
        return self._pre_function_hook(*inputs)

    def post_function_hook(self, *function_output):
        return self._post_function_hook(*function_output)

    def _pre_function_hook(self, *inputs):
        return inputs

    def _post_function_hook(self, *function_output):
        return function_output

    def _json(self, *args, **kwargs):
        raise NotImplementedError

    def json(self, *args, **kwargs):
        return self._json(self.func(*args, **kwargs))

    def run(self, *args):
        function_inputs = self.pre_function_hook(*args)
        function_output = self.func(*function_inputs)
        return self.post_function_hook(function_output)

    @classmethod
    def as_callback(cls, func):
        callback = cls(func)
        return callback

    def __call__(self, *args):
        return self.func(*args)

    def register(self, outputs, inputs, states):
        self.set_inputs(inputs)
        self.set_outputs(outputs)
        self.set_states(states)

    def set_inputs(self, inputs):
        if inputs is not None:
            self.dash_inputs = [Input(id, prop) for id, prop in inputs]

    def set_outputs(self, outputs):
        if outputs is not None:
            self.dash_outputs = [Output(id, prop) for id, prop in outputs]

    def set_states(self, states):
        if states is not None:
            self.dash_states = [State(id, prop) for id, prop in states]

    @property
    def description(self):
        return {
            "name": self.name,
            "parameters": self.parameters,
            "docstring": self.func.__doc__,
            "return_type": self.return_type,
        }

    @property
    def name(self):
        return self.func.__name__

    @property
    def parameters(self):
        sig = signature(self.func)
        params = []
        for name, param in sig.parameters.items():
            param_doc = {"name": name}
            if param.annotation is not param.empty:
                param_doc["type"] = str(param.annotation)
            if param.default is not param.empty:
                param_doc["default"] = param.default

            params.append(param_doc)

        return params

    @property
    def return_type(self):
        t = signature(self.func).return_annotation
        if t != Signature.empty:
            return t
        return
