from gweld.libs.svg_lib import add_text
from gweld import VisElement

class TextElement(VisElement):
    def __init__(self, text, pos, style):
        self.text = text
        self.pos = pos
        self.style = style

    def plot(self, tree, vis):
        x = self.pos[0] + margins[0]
        y = self.pos[1] + margins[1]

        add_text(tree, (x, y), self.text, self.style)
