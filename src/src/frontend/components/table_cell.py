from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Line

class TableCell(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint_y = None
        self.height = 40
        self.halign = "center"
        self.valign = "middle"
        self.text_size = (self.width, None)
        self.bind(size=self._update_text_size)

        with self.canvas.before:
            Color(0.88, 0.95, 0.97, 1)
            self._bg = Rectangle(pos=self.pos, size=self.size)

            Color(0.0, 0.33, 0.43, 1)
            self._border = Line(rectangle=(*self.pos, *self.size), width=1.8)

        self.bind(pos=self._update_graphics, size=self._update_graphics)

    def _update_text_size(self, *args):
        self.text_size = (self.width, None)

    def _update_graphics(self, *args):
        self._bg.pos = self.pos
        self._bg.size = self.size
        self._border.rectangle = (*self.pos, *self.size)
