from gweld import TextStyle

class CircleTextStyle(TextStyle):
    @property
    def css(self):
        return f'''
            .{self.text_type}_label_upper_left {{
                font-size: {self.size}px;
                text-anchor: {self.anchor if self.anchor == 'middle' else 'start'};
                dominant-baseline: {self.baseline if self.baseline == 'middle' else 'auto'};
            }}

            .{self.text_type}_label_upper_right {{
                font-size: {self.size}px;
                text-anchor: {self.anchor if self.anchor == 'middle' else 'end'};
                dominant-baseline: {self.baseline if self.baseline == 'middle' else 'auto'};
            }}

            .{self.text_type}_label_lower_left {{
                font-size: {self.size}px;
                text-anchor: {self.anchor if self.anchor == 'middle' else 'start'};
                dominant-baseline: {self.baseline if self.baseline == 'middle' else 'hanging'};
            }}

            .{self.text_type}_label_lower_right {{
                font-size: {self.size}px;
                text-anchor: {self.anchor if self.anchor == 'middle' else 'end'};
                dominant-baseline: {self.baseline if self.baseline == 'middle' else 'hanging'};
            }}
        '''
