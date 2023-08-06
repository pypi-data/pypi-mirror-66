class TextStyle:
    def __init__(self, text_type):
        self.text_type = text_type 
        self.init()

    def init(self):
        self.size = 12
        self.angle = 0
        self._anchor = 'start'
        self.angle_anchor = 'start'
        self.baseline = 'bottom'
        self.base_offset = 0
        self.format = lambda x: x

    @property
    def anchor(self):
        return self._anchor if self.angle == 0 else self.angle_anchor

    @anchor.setter
    def anchor(self, anchor):
        self._anchor = anchor

    @property
    def css(self):
        return f'''
            .{self.text_type}_label {{
                font-size: {self.size}px;
                text-anchor: {self.anchor};
                dominant-baseline: {self.baseline};
            }}
        '''
