from gweld.libs.svg_lib import root_tag, add_tag, add_text
from gweld import Chart, BGElement
import math

class Pie(Chart):
    def init(self):
        self.elements = [BGElement()]

    def plot(self, tree, vis):
        if len(vis.data) == 0:
            return tree

        # Left, Right
        plot_x = (
            vis.style.width * vis.style.margin[0],
            vis.style.width * vis.style.margin[2]
        )
        # Up, Down
        plot_y = (
            vis.style.height * vis.style.margin[1],
            vis.style.height * vis.style.margin[3]
        )

        plot_width = vis.style.width - plot_x[0] - plot_x[1]
        plot_height = vis.style.height - plot_y[0] - plot_y[1]


        # Plot pie

        angles = self._calculate_angles(vis.data)
        centre = (plot_x[0] + plot_width/2, plot_y[0] + plot_height/2)
        radius = min(plot_width, plot_height)/2 * 0.9
        value_radius = radius * vis.style.pie_value_radius

        # SVG paths can't draw full circle. Backtrack to a circle if we
        # get too close
        if len(vis.data) == 1 or max(angles) > 1.99 * math.pi:
            add_tag(tree, 'circle', attributes={
                'cx': str(centre[0]),
                'cy': str(centre[1]),
                'r': str(radius),
                'fill': vis.style.data_colours[0]
            })
        else:
            x = centre[0]
            y = centre[1] - radius
            angle = 0

            for i, item in enumerate(vis.data):
                (old_x, old_y) = (x,y)
                angle += angles[i]
                x = centre[0] + radius * math.sin(angle)
                y = centre[1] + -(radius * math.cos(angle))
                big = 1 if angles[i] > math.pi else 0

                add_tag(tree, 'path', attributes={
                    'd': f'M{centre[0]},{centre[1]} L{old_x},{old_y} A{radius},{radius} 0 {big},1 {x},{y} Z',
                    'fill': vis.style.data_colours[(i%len(vis.data)) % len(vis.style.data_colours)]
                }, text=str((angles[i], angle)))

            angle = 0
            for i, item in enumerate(vis.data):
                angle += angles[i] / 2
                x = centre[0] + value_radius * math.sin(angle)
                y = centre[1] + -(value_radius * math.cos(angle))

                css_class = '_' 
                if angle < math.pi/2 or angle > math.pi*6/4:
                    css_class += 'upper'
                else:
                    css_class += 'lower'
                if angle < math.pi:
                    css_class += '_left'
                else:
                    css_class += '_right'

                add_text(
                    tree,
                    (x,y),
                    str(item),
                    vis.style.text_styles['circle_value'],
                    css_class
                )

                angle += angles[i] / 2

        add_tag(tree, 'circle', attributes={
            'cx': str(centre[0]),
            'cy': str(centre[1]),
            'r': str(radius * vis.style.pie_inner_radius),
            'fill': vis.style.background_colour
        })

        return tree

    def _calculate_angles(self, data):
        angles = []

        for item in data:
            angles.append(2 * math.pi * (item / sum(data)))

        return angles
