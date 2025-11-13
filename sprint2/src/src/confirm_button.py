from kivy.uix.image import Image
from kivy.graphics import RoundedRectangle, Color
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.metrics import dp
import os

folder_path = os.path.join(os.path.dirname(__file__), 'images')
img_path = os.path.join(folder_path, 'confirm.png')

class ConfirmButtonModel(ButtonBehavior, Widget):
    callback = ObjectProperty(None)
    bg_color = ListProperty([0.61, 0.867, 0.937, 1])
    outline_color = ListProperty([0.078, 0.369, 0.447, 1])
    pressed_color = ListProperty([0.45, 0.7, 0.8, 1])


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        self.size = (dp(75),dp(75))

        self.callback = kwargs.get("callback", self.callback)

        with self.canvas.before:
            self._outline_color = Color(*self.outline_color)
            self.outline = RoundedRectangle(pos=(self.x - dp(6), self.y - dp(6)), size=(self.width + dp(12), self.height + dp(12)), radius=[15])
            self._bg_color = Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])

        self.logo = Image(source=img_path, size_hint=(.5, .5))
        self.add_widget(self.logo)
        self.bind(pos=self.update_graphics, size=self.update_graphics,
                  bg_color=self._update_colors, outline_color=self._update_colors)
        self.bind(pos=self._update_logo_pos, size=self._update_logo_pos)
        self.update_graphics()
        
    def update_graphics(self, *args):
        sw = self.width + 10
        sh = self.height + 10
        sx = self.pos[0] - 5
        sy = self.pos[1] - 5
        self.outline.size = (sw, sh)
        self.outline.pos = (sx, sy)
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _update_logo_pos(self, *args):
        self.logo.center = self.center


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
