import json

import numpy as np

from dash_infra import Callback
from dash_infra.mixins.json_serializers import JSONSerializer


class FigureCallback(Callback, JSONSerializer):
    def _pre_function_hook(self, sample_size):
        if sample_size is None:
            return (np.array([50]),)
        return (np.linspace(0, 100, sample_size),)

    def _post_function_hook(self, *function_output):
        data = [dict(x=self.current_inputs[0], y=function_output[0], mode="markers")]
        return {"data": data},

    def _json(self, function_output):
        return self.numpy_to_json(function_output)


@FigureCallback.as_callback
def square(x: "Arrayable") -> np.ndarray:
    """
    Computes the square of x
    """
    return np.array(x) ** 2


@FigureCallback.as_callback
def cube(x):
    return np.array(x) ** 3
