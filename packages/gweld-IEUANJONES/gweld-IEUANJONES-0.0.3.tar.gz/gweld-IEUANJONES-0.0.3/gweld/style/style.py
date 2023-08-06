from gweld import TextStyle, CircleTextStyle

class Style:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.bar_width = 0.8
        self.data_colour = '#f00'
        self.data_colours = ['#ed4334','#27ca42','#2546eb','#eadc45','#faab43']
        self.background_colour = '#efefef'

        self.axis_font_size = 24
        self.axis_stroke_colour = '#000'
        self.axis_stroke_width = '2'

        self.show_grid_lines = True 
        self.grid_lines_stroke_colour = '#a7a7a7'
        self.grid_lines_stroke_width = 1
        
        self.x_axis_interval = 1 # Show every n items on the x axis
        self.y_axis_tick_number = 7

        self.pie_inner_radius = 0.5 # Move out to separate function in future
        self.pie_value_radius = 1.1 # Move out to separate function in future

        self.text_styles = {
            'x_axis': TextStyle('x_axis'),
            'y_axis': TextStyle('y_axis'),
            'value': TextStyle('value'),
            'circle_value': CircleTextStyle('circle_value')
        }
        self.show_values = 'none'

        # L U R D
        self.margin = (0.05, 0.05, 0.05, 0.1)

    def __iadd__(self, other):
        if isinstance(other, TextStyle):
            if other.text_type:
                self.text_styles[other.text_type] = other
            else:
                print(f'Invalid text_type: TextStyle({other.text_type})')
                raise TypeError
        else:
            raise TypeError

        return self

    @property
    def css(self):
        css = ''

        for text_type in self.text_styles:
            css += self.text_styles[text_type].css

        css += f'''
        .data_colour {{
            fill: {self.data_colour};
        }}
        
        .line_chart_data_line {{
            stroke-width: 2px;
        }}
        
        .axis {{
            stroke: {self.axis_stroke_colour};
            stroke-width: {self.axis_stroke_width}px;
        }}

        .grid_lines {{
            stroke: {self.grid_lines_stroke_colour};
            stroke-width: {self.grid_lines_stroke_width}px;
        }}
        '''

        return css
