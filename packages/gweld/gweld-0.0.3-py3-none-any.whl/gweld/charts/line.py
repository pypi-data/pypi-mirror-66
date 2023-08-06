from gweld.libs.util_lib import calculate_y_scale, calculate_chart_size, calculate_margins
from gweld.libs.svg_lib import root_tag, add_tag, add_text
from gweld import Chart, DataSet, Data, AxisElement, BGElement
import math

class Line(Chart):
    def init(self):
        self.elements = [BGElement(), AxisElement()]

    def plot(self, tree, vis):
        if len(vis.data) == 0:
            return tree

        margins = calculate_margins(vis)
        size = calculate_chart_size(vis, margins)

        y_scale = calculate_y_scale(vis.data, vis.style.y_axis_tick_number)

        inner_tree = add_tag(tree, 'svg', attributes={
            'viewBox': f'0 0 {size[0]}, {size[1]}',
            'x': str(margins[0]),
            'y': str(margins[1]),
            'width': str(size[0]),
            'height': str(size[1])
        })

        if isinstance(vis.data, DataSet):
            for i, data in enumerate(vis.data):
                self._plot_line(vis, data, y_scale[-1], size[0], size[1], vis.style.data_colours[i%len(data)], inner_tree)
        elif isinstance(vis.data, Data):
            self._plot_line(vis, vis.data, y_scale[-1], size[0], size[1], vis.style.data_colour, inner_tree)
        else:
            raise Exception
        
        if vis.data.labels:
            for i, label in enumerate(vis.data.labels):
                if not i % vis.style.x_axis_interval:
                    width_per_node = size[0] / (len(vis.data)-1)
                    x = margins[0] + i * width_per_node

                    label_y = margins[1] + size[1] + vis.style.text_styles["x_axis"].size/2
                    add_text(tree, (x, label_y), str(label), vis.style.text_styles['x_axis'])

        return tree

    def _plot_line(self, vis, data, max_value, plot_width, plot_height, colour, tree):
        width_per_node = plot_width / (len(data)-1)
        points = []

        for i, item in enumerate(data):
            x = i * width_per_node
            y = plot_height - (item / max_value) * plot_height
            points.append((x, y))

            if vis.style.show_values == 'all' or (vis.style.show_values == 'limits' and
                    (item == data.max or item == data.min)):
                label_y = y - vis.style.text_styles["value"].size/2

                add_text(tree, (x, label_y), str(item), vis.style.text_styles['value'])

        add_tag(tree, 'polyline', attributes={
            'points': ' '.join([f'{str(point[0])}, {str(point[1])}' for point in points]),
            'fill': 'none',
            'stroke': colour,
            'class': 'line_chart_data_line'
        })
