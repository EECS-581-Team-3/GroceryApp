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

from backend.inventory_manager import InventoryManager
from frontend.components.home_button import HomeButtonModel
from frontend.components.confirm_button import ConfirmButtonModel


class EditSMScreen(Screen):
    def __init__(self, inventory_manager: InventoryManager, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(EditSMPage())


class EditSMPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.locations = App.get_running_app().storage_locations
        self.build_layout()

    def build_layout(self):
        self.clear_widgets()
        self.add_widget(Label(
            text='Edit Storage Locations', 
            font_size=24, 
            font_name='Roboto', 
            size_hint_y=None,
            height=dp(50), 
            color=(0.078, 0.369, 0.447, 1)
        ))
        
        rows = BoxLayout(orientation='vertical', spacing=10, padding=10)

        for name in self.locations:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(44), spacing=10, padding=3)
            row.add_widget(Label(
                text=name, 
                color=(0.078, 0.369, 0.447, 1),
                size_hint_x=0.8
            ))
            remove_btn = Button(
                text='-', 
                background_normal='', 
                background_color=(0.61, 0.867, 0.937, 1), 
                color=(0.078, 0.369, 0.447, 1), 
                font_size=20, 
                bold=True,
                size_hint_x=0.2
            )
            remove_btn.bind(on_release=lambda inst, n=name: self.remove_location(n))
            row.add_widget(remove_btn)
            rows.add_widget(row)

        add_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(44), spacing=10, padding=3)
        self.name_input = TextInput(
            hint_text='New Location Name', 
            multiline=False, 
            background_color=(0.61, 0.867, 0.937, 1), 
            foreground_color=(0.078, 0.369, 0.447, 1)
        )
        add_btn = Button(
            text='+', 
            background_normal='', 
            background_color=(0.61, 0.867, 0.937, 1), 
            color=(0.078, 0.369, 0.447, 1), 
            font_size=20, 
            bold=True,
            on_press=self.add_location
        )
        add_row.add_widget(self.name_input)
        add_row.add_widget(add_btn)
        rows.add_widget(add_row)

        self.add_widget(rows)

        self.add_widget(BoxLayout(size_hint_y=1))

        footer = BoxLayout(orientation='horizontal', spacing=80, padding=125, size_hint_y=None, height=dp(100))
        home_btn = HomeButtonModel(callback=self.go_home)
        confirm_btn = ConfirmButtonModel(callback=self.go_SM)
        footer.add_widget(home_btn)
        footer.add_widget(confirm_btn)
        self.add_widget(footer)

    def remove_location(self, name):
        """Remove a storage location."""
        if name in self.locations:
            self.locations.remove(name)

            sm = App.get_running_app().sm
            screen_name = name.lower()
            if sm.has_screen(screen_name):
                screen = sm.get_screen(screen_name)
                sm.remove_widget(screen)
                print(f"Removed screen: {name}")
            
            self.build_layout()

    def add_location(self, instance):
        """Add a new storage location."""
        name = self.name_input.text.strip()
        if not name:
            return

        if any(loc.lower() == name.lower() for loc in self.locations):
            print(f"Location '{name}' already exists")
            return
        
        self.locations.append(name)
        self.name_input.text = ''
        self.build_layout()
        print(f"Added location: {name}")

    def go_SM(self):
        App.get_running_app().sm.current = 'store manager'
    
    def go_home(self):
        App.get_running_app().sm.current = 'home'