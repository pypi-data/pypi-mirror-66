"""
A demo storage application
"""

from dash_infra import KWSDashApp
from callbacks import square, cube, square_root, sum_callback
from components import group, store, sum_div

dash_app = KWSDashApp("Storage application", doc=__doc__)
dash_app.register_component(group)
dash_app.register_component(sum_div)

dash_app.register_callback(
    square, outputs=[("square", "children")], inputs=[("input", "value")]
).add_storage_output(store)

dash_app.register_callback(
    cube, outputs=[("cube", "children")], inputs=[("input", "value")]
).add_storage_output(store)

dash_app.register_callback(
    square_root, outputs=[("sqrt", "children")], inputs=[("input", "value")]
).add_storage_output(store)

dash_app.register_component(store)

sum_callback.use_storage_inputs(store, "square", "cube", "square_root")
dash_app.register_callback(sum_callback, outputs=[("sum", "children")])

if __name__ == "__main__":
    dash_app.run_server(debug=True)
