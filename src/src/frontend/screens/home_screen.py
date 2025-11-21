# home_screen.py
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window

import os
from pathlib import Path

from frontend.components.title_layout import TitleLayout
from frontend.components.button_layout import ButtonLayout

Window.size = (500, 750)
Window.clearcolor = (0.84, 0.95, 1, 1)

folder_path = Path("frontend/images/")
top_img_path = folder_path / "top.png"
bottom_img_path = folder_path / "bottom.png"


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(HomePage())

class HomePage(BoxLayout):
    def __init__(self, **kwargs):
        super(HomePage, self).__init__(orientation='vertical', spacing=0, **kwargs)
        title = TitleLayout()
        self.add_widget(title)
        self.add_widget(Image(source=str(top_img_path), size_hint=(.5, .5), pos_hint={'x':.25, 'y':1}))
        self.add_widget(Image(source=str(bottom_img_path), size_hint=(.5, .5), pos_hint={'x':.25, 'y':0}))
        buttons = ButtonLayout(pantry_callback=self.go_inventory, grocery_callback=self.go_grocery)
        self.add_widget(buttons)

    def go_inventory(self, instance):
        App.get_running_app().sm.current = 'store manager'

    def go_grocery(self, instance):
        App.get_running_app().sm.current = 'grocery'
