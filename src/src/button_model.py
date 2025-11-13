from kivy.graphics import RoundedRectangle, Color
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.uix.label import Label
from kivy.metrics import dp

class ButtonModel(ButtonBehavior, Widget):
    text = StringProperty("Click Me")
    callback = ObjectProperty(None)
    bg_color = ListProperty([0.61, 0.867, 0.937, 1])
    outline_color = ListProperty([0.078, 0.369, 0.447, 1])
    pressed_color = ListProperty([0.45, 0.7, 0.8, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = kwargs.get("text", self.text)
        self.callback = kwargs.get("callback", self.callback)
        
        with self.canvas.before:
            self._outline_color = Color(*self.outline_color)
            self.outline = RoundedRectangle(pos=(self.x - dp(6), self.y - dp(6)), size=(self.width + dp(12), self.height + dp(12)), radius=[15])
            self._bg_color = Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])

        self.label = Label(text=self.text, color = (0.078,0.369,0.447,1), font_size=30, size_hint=(None, None), bold=True)
        self.add_widget(self.label)
        self.bind(pos=self.update_graphics, size=self.update_graphics, text=self.update_text,
                  bg_color=self._update_colors, outline_color=self._update_colors)
        self.bind(pos=self._update_label_pos, size=self._update_label_pos)
        self.update_graphics()
        
    def update_graphics(self, *args):
        sw = self.width + 12
        sh = self.height + 12
        sx = self.pos[0] - 6
        sy = self.pos[1] - 6
        self.outline.size = (sw, sh)
        self.outline.pos = (sx, sy)
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _update_label_pos(self, *args):
        self.label.center = self.center

    def update_text(self, *args):
        self.label.text = self.text

    def _update_colors(self, *args):
        self._outline_color.rgba = self.outline_color
        self._bg_color.rgba = self.bg_color

    def on_press(self):
        self.bg_color = self.pressed_color
        if callable(self.callback):
            try:
                self.callback(self)
            except TypeError:
                self.callback()
    
    def on_release(self):
        self.bg_color = [0.61, 0.867, 0.937, 1]
