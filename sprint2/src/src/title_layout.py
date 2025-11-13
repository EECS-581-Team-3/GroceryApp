from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.metrics import dp
import os

font_path = os.path.join(os.path.dirname(__file__), "carterOne.ttf")

class TitleLayout(AnchorLayout):
    def __init__(self, **kwargs):
        super(TitleLayout, self).__init__(anchor_x='center', anchor_y='center', **kwargs)
        self.add_widget(Label(text='Pantry Pro', font_name=font_path, font_size=65, color=(0.078,0.369,0.447,1), size_hint_x=.3, size_hint_y=None, height=dp(10)))