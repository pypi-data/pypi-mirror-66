from gweld.libs.util_lib import calculate_y_scale, calculate_chart_size, calculate_margins
from gweld.libs.svg_lib import root_tag, add_tag, add_text
from gweld import Chart, AxisElement, BGElement
import math

class Bar(Chart):
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

        width_per_bar = size[0] / len(vis.data)
        bar_width = width_per_bar * vis.style.bar_width

        for i, item in enumerate(vis.data):
            height = (item / y_scale[-1]) * size[1]
            centre_x = i * width_per_bar + width_per_bar/2

            add_tag(inner_tree, 'rect', attributes={
                'width': str(bar_width),
                'height': str(height),
                'x': str(centre_x - bar_width/2),
                'y': str(size[1] - height),
                'class': 'data_colour'
            })

            if vis.style.show_values == 'all' or (vis.style.show_values == 'limits' and
                    (item == vis.data.max or item == vis.data.min)):
                label_y = size[1] - height - vis.style.text_styles["value"].size/2
                add_text(tree, (margins[0] + centre_x, margins[1] + label_y), str(item), vis.style.text_styles['value'])

            if vis.data.labels:
                if not i % vis.style.x_axis_interval:
                    label_y = size[1] + vis.style.text_styles["x_axis"].size/2
                    add_text(tree, (margins[0] + centre_x, margins[1] + label_y), str(vis.data.labels[i]), vis.style.text_styles['x_axis'])

        return tree

    def _calculate_y_scale(self, data, tick_count=5):
        # Algorithm from: https://stackoverflow.com/a/326746
        lower_bound = 0 # No support for negative numbers.... yet
        upper_bound = data.max

        if upper_bound == 0:
            upper_bound = 1

        data_range = upper_bound - lower_bound
        coarse_tick_size = data_range / (tick_count-1)
        magnitude = math.ceil(math.log(coarse_tick_size, 10)) # Yay floating point arithmetic!

        for tick_size in [0.1, 0.125, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.9, 1]:
            if coarse_tick_size/10**magnitude <= tick_size:
                tick_size *= 10**magnitude
                break

        if not tick_size % 1:
            tick_size = int(tick_size)

        scale = [0]
        while tick_count-1 > 0:
            scale.append(round(scale[-1]+tick_size, 3))

            if scale[-1] > upper_bound:
                break
            tick_count -= 1

        return scale
