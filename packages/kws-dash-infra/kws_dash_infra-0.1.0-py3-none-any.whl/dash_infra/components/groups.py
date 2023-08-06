from dash_infra  import Component
from dash_infra.html_helpers.divs import Row

class ComponentGroup(Component):
    def __init__(self, id, *components):
        super().__init__(id)
        self.components = components

    def layout(self, container=Row, classes=None):
        return container([c.layout() for c in self.components], classes=None)