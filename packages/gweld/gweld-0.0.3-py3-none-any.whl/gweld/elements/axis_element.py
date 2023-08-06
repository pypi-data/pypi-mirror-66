from gweld.libs.util_lib import calculate_y_scale, calculate_chart_size, calculate_margins
from gweld.libs.svg_lib import add_tag, add_text
from gweld import VisElement

class AxisElement(VisElement):
    def plot(self, tree, vis):
        margins = calculate_margins(vis)
        size = calculate_chart_size(vis, margins)
        size = (size[0]+1, size[1]+1)

        y_scale = calculate_y_scale(vis.data, vis.style.y_axis_tick_number)

        inner_tree = add_tag(tree, 'svg', attributes={
            'viewBox': f'0 0 {size[0]}, {size[1]}',
            'x': str(margins[0]-1),
            'y': str(margins[1]),
            'width': str(size[0]),
            'height': str(size[1])
        })

        for i in range(1, len(y_scale)):
            y_pos = size[1] - i * size[1]/(len(y_scale)-1)
            if vis.style.show_grid_lines:
                add_tag(inner_tree, 'line', attributes={
                    'x1': '0',
                    'x2': str(size[0]),
                    'y1': str(y_pos),
                    'y2': str(y_pos),
                    'class': 'grid_lines'
                })
        
        # Axes
        
        add_tag(inner_tree, 'line', attributes={
            'x1': str(0),
            'x2': str(0),
            'y1': str(size[1]),
            'y2': str(0),
            'class': 'axis'
        })
        
        add_tag(inner_tree, 'line', attributes={
            'x1': str(0),
            'x2': str(size[0]),
            'y1': str(size[1]),
            'y2': str(size[1]),
            'class': 'axis'
        })
        
        for i, label in enumerate(y_scale):
            y_pos = margins[0] + size[1] - i * size[1]/(len(y_scale)-1)
            add_text(tree, (margins[0]-5, y_pos), str(label), vis.style.text_styles['y_axis'])
