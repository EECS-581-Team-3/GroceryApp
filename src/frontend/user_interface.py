# user_interface.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from backend.inventory_manager import InventoryManager

from frontend.screens.home_screen import HomeScreen
from frontend.screens.edit_sm_screen import EditSMScreen
from frontend.screens.storage_manager_screen import StorageManagerScreen
from frontend.screens.grocery_screen import GroceryScreen

Window.size = (500, 750)
Window.clearcolor = (0.84, 0.95, 1, 1)


class InventoryApp(App):
    def build(self):
        self.inventory_manager = InventoryManager()
        self.sm = ScreenManager()

        self.storage_locations = []

        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(EditSMScreen(self.inventory_manager, name='edit_SM'))
        self.sm.add_widget(StorageManagerScreen(self.inventory_manager, name='store manager'))
        self.sm.add_widget(GroceryScreen(name='grocery'))

        return self.sm
