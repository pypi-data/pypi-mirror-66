"""
vis.py
======

Module containing the core visualisation object.
"""

from gweld import Data, Chart, Bar, VisElement, Style
from gweld.libs.svg_lib import add_tag, root_tag, to_string

class Vis:
    """
    A visualisation object. The core object worked with to create visualisations.
    """
    def __init__(self, data=Data(), chart=Bar(), elements=[], style=Style()):
        self.init()

        self.data = data
        self.chart = chart
        self.elements += elements
        self.style = style

    def init(self):
        self.elements = []

    def __repr__(self):
        return f'Chart(data={self.data!r}, chart={self.chart!r}, style={self.style!r})'

    def __add__(self, other):
        if isinstance(other, Data):
            return Vis(data=other, chart=self.chart, elements=self.elements, style=self.style)
        if isinstance(other, Chart):
            return Vis(data=self.data, chart=other, elements=self.elements, style=self.style)
        if isinstance(other, VisElement):
            return Vis(data=self.data, chart=self.chart, elements=self.elements+[other], style=self.style)
        if isinstance(other, Style):
            return Vis(data=self.data, chart=self.chart, elements=self.elements, style=other)
        raise TypeError

    def plot(self):
        tree = root_tag(self.style.width, self.style.height)
        add_tag(tree, 'style', text=self.style.css)

        for element in self.chart.elements:
            element.plot(tree, self)
        
        self.chart.plot(tree, self)

        for element in self.elements:
            element.plot(tree, self)

        return to_string(tree)
