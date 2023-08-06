"""
An application to visualize powers of 2 and 3.

"""

from werkzeug.serving import run_simple

from dash_infra import KWSDashApp
from dash_infra import KWSSuperApp

try:
    from .components import group
    from .callbacks import square, cube
except:
    from components import group
    from callbacks import square, cube

dash_app = KWSDashApp("A multplier component", doc=__doc__)
dash_app.register_component(group)
dash_app.register_callback(
    square, outputs=[("square", "figure")], inputs=[("input", "value")]
)
dash_app.register_callback(
    cube, outputs=[("cube", "figure")], inputs=[("input", "value")]
)


if __name__ == "__main__":
    dash_app.run_server(debug=True)
