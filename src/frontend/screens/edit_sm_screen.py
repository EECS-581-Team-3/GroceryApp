# edit_sm_screen.py
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.core.window import Window

from backend.inventory_manager import InventoryManager
from frontend.components.home_button import HomeButtonModel
from frontend.components.confirm_button import ConfirmButtonModel

Window.size = (500, 750)
Window.clearcolor = (0.84, 0.95, 1, 1)


class EditSMScreen(Screen):
    def __init__(self, inventory_manager: InventoryManager, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(EditSMPage())


class EditSMPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.locations = App.get_running_app().storage_locations
        self.add_widget(Label(text='Test', color=(0,0,0,1)))
        self.build_layout()

    def build_layout(self):
        self.clear_widgets()
        self.add_widget(Label(text='Edit Storage', font_size=24, 
                              font_name='Roboto', size_hint_y=None,
                              height=dp(50), color=(0.078,0.369,0.447,1)))
        
        rows = BoxLayout(orientation='vertical', spacing=10)
        
        for name in self.locations:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(44), spacing=10, padding=3) 
            row.add_widget(TextInput(text=name, multiline=False, background_color=(0.61, 0.867, 0.937, 1), foreground_color=(0.078,0.369,0.447,1)))
            row.add_widget(Button(text='-', background_normal='', background_color=(0.61, 0.867, 0.937, 1), color=(0.078,0.369,0.447,1), font_size=20, bold=True))
            rows.add_widget(row)
        
        add_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(44), spacing=10, padding=3)
        self.name_input = TextInput(hint_text='Name', multiline=False, background_color=(0.61, 0.867, 0.937, 1), foreground_color=(0.078,0.369,0.447,1))
        add_btn = Button(text='+', background_normal='', background_color=(0.61, 0.867, 0.937, 1), color=(0.078,0.369,0.447,1), font_size=20, bold=True)
        add_row.add_widget(self.name_input)
        add_row.add_widget(add_btn)
        rows.add_widget(add_row)

        self.add_widget(rows)

        self.scroll = ScrollView()
        self.list_grid = GridLayout(cols=1, size_hint_y=None, spacing=dp(6), padding=dp(6))
        self.list_grid.bind(minimum_height=self.list_grid.setter('height'))
        self.scroll.add_widget(self.list_grid)
        self.add_widget(self.scroll)

        footer = BoxLayout(orientation='horizontal', spacing=80, padding=125)
        home_btn = HomeButtonModel(callback=self.go_home)
        confirm_btn = ConfirmButtonModel(callback=self.go_SM)
        footer.add_widget(home_btn)
        footer.add_widget(confirm_btn)
        self.add_widget(footer)

    def go_SM(self):
        App.get_running_app().sm.current = 'store manager'
    
    def go_home(self):
        App.get_running_app().sm.current = 'home'

