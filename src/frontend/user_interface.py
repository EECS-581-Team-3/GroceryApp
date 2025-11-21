# user_inferface.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
import os

from backend.inventory_manager import InventoryManager
from backend.item import Item
from backend.grocery_list import GroceryList

from frontend.screens.home_screen import HomeScreen
from frontend.screens.edit_sm_screen import EditSMScreen
from frontend.screens.pantry_screen import PantryScreen
from frontend.screens.fridge_screen import FridgeScreen
from frontend.screens.freezer_screen import FreezerScreen
from frontend.screens.storage_manager_screen import StorageManagerScreen
from frontend.screens.grocery_screen import GroceryScreen

Window.size = (500, 750)
Window.clearcolor = (0.84, 0.95, 1, 1)

class InventoryApp(App):
    def build(self):
        self.inventory_manager = InventoryManager()
        self.sm = ScreenManager()
        self.storage_locations = ['Pantry', 'Fridge', 'Freezer']

        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(EditSMScreen(self.inventory_manager, name='edit_SM'))
        self.sm.add_widget(PantryScreen(self.inventory_manager))
        self.sm.add_widget(FridgeScreen(self.inventory_manager))
        self.sm.add_widget(FreezerScreen(self.inventory_manager))
        self.sm.add_widget(StorageManagerScreen(self.inventory_manager, name='store manager'))
        self.sm.add_widget(GroceryScreen(name='grocery'))

        return self.sm

