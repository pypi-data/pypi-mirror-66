from gweld.libs.svg_lib import add_tag
from gweld import VisElement

class BGElement(VisElement):
    def plot(self, tree, vis):
        add_tag(tree, 'rect', attributes={
            'x': '0',
            'y': '0',
            'width': str(vis.style.width),
            'height': str(vis.style.height),
            'fill': vis.style.background_colour
        })
