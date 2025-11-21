# location_template_screen.py
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

from frontend.components.button_model import ButtonModel
from backend.inventory_manager import InventoryManager

Window.size = (500, 750)
Window.clearcolor = (0.84, 0.95, 1, 1)

class LocationTemplateScreen(Screen):
    def __init__(self, title:str, **kwargs):
        super().__init__(name=title.lower(), **kwargs)
        self.add_widget(LocationTemplatePage(title))

class LocationTemplatePage(BoxLayout):
    def __init__(self, title:str, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.title = title
        self.build_layout()

    def build_layout(self):
        self.add_widget(Label(text=self.title, color=(0,0,0,1), font_size=25))
        self.add_widget(Button(text='home', on_press=self.go_home))
        
    def go_home(self, instance):
        App.get_running_app().sm.current = 'home'


