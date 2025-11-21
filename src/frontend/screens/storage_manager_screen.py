# storage_manager_screen.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.core.window import Window

import os
from typing import List

from backend.inventory_manager import InventoryManager
from frontend.components.button_model import ButtonModel
from frontend.components.home_button import HomeButtonModel
from frontend.components.edit_button import EditButtonModel


class StorageManagerScreen(Screen):
    def __init__(self, inventory_manager: InventoryManager, **kwargs):
        super().__init__(**kwargs)
        self.page = StorageManagerPage(inventory_manager)
        self.add_widget(self.page)
    
    def on_enter(self, *args):
        self.page.on_enter()

class StorageManagerPage(BoxLayout):
    def __init__(self, inventory_manager: InventoryManager, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.inventory_manager = inventory_manager
        self.locations = App.get_running_app().storage_locations
        self.build_layout()

    def build_layout(self):
        self.clear_widgets()
        self.add_widget(Label(text='Storage Manager', font_size=24, font_name='Roboto', size_hint_y=None, height=dp(50), color=(0.078,0.369,0.447,1)))
        gridlayout = GridLayout(cols=2, spacing=40, padding=30)
        for btn in self.generate_buttons(self.locations):
            gridlayout.add_widget(btn)
            print(btn.callback)
        self.add_widget(gridlayout)
        footer = BoxLayout(orientation='horizontal', spacing=80, padding=125)
        home_btn = HomeButtonModel(callback=self.go_home)
        edit_btn = EditButtonModel(callback=self.go_edit_SM)
        footer.add_widget(home_btn)
        footer.add_widget(edit_btn)
        self.add_widget(footer)

    def on_enter(self, *args):
        self.build_layout()

    def go_edit_SM(self, instance):
        App.get_running_app().sm.current = 'edit_SM'

    def go_home(self, instance):
        App.get_running_app().sm.current = 'home'

    def generate_buttons(self, titles: List[str]) -> List[ButtonModel]:
        # takes in list of strings and creates list of button 
        # models with titles and callbacks in format of go_{title}
        btns = []
        for title in titles:
            callback_name = f"go_{title.lower()}"
            def method(self, instance=None, name=title.lower()):
                App.get_running_app().sm.current = name
            setattr(StorageManagerPage, callback_name, method)
            callback = getattr(self, callback_name)
            btn = ButtonModel(text=title, callback=callback)
            btns.append(btn)
        self.generate_screens()
        return btns
    
    def generate_screens(self):
        sm = App.get_running_app().sm
        for name in self.locations:
            _name = name.lower()
            if _name in ['pantry', 'fridge', 'freezer']:
                continue
            if not sm.has_screen(_name):
                sm.add_widget(LocationTemplateScreen(title=_name))
                
