from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.core.window import Window
from inventory_manager import InventoryManager
from item import Item
from typing import List

from grocery_list import GroceryList
import os

from title_layout import TitleLayout
from button_layout import ButtonLayout
from button_model import ButtonModel
from home_button import HomeButtonModel
from edit_button import EditButtonModel
from confirm_button import ConfirmButtonModel

Window.size = (500, 750)
Window.clearcolor = (0.84, 0.95, 1, 1)

folder_path = os.path.join(os.path.dirname(__file__), 'images')
top_img_path = os.path.join(folder_path, 'top.png')
bottom_img_path = os.path.join(folder_path, 'bottom.png')

class HomePage(BoxLayout):
    def __init__(self, **kwargs):
        super(HomePage, self).__init__(orientation='vertical', spacing=0, **kwargs)
        title = TitleLayout()
        self.add_widget(title)
        self.add_widget(Image(source=top_img_path, size_hint=(.5, .5), pos_hint={'x':.25, 'y':1}))
        self.add_widget(Image(source=bottom_img_path, size_hint=(.5, .5), pos_hint={'x':.25, 'y':0}))
        buttons = ButtonLayout(pantry_callback=self.go_inventory, grocery_callback=self.go_grocery)
        self.add_widget(buttons)

    def go_inventory(self, instance):
        App.get_running_app().sm.current = 'store manager'

    def go_grocery(self, instance):
        App.get_running_app().sm.current = 'grocery'

class StorageManagerPage(BoxLayout):
    def __init__(self, inventory_manager: InventoryManager, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.inventory_manager = inventory_manager
        self.locations = App.get_running_app().storage_locations
        self.build_layout()

    def build_layout(self):
        self.clear_widgets()
        self.add_widget(Label(text='Storage Manager', font_size=24, font_name='Verdana', size_hint_y=None, height=dp(50), color=(0.078,0.369,0.447,1)))
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
        return btns
    
    
class EditSMPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.locations = App.get_running_app().storage_locations
        self.add_widget(Label(text='Test', color=(0,0,0,1)))
        self.build_layout()

    def build_layout(self):
        self.clear_widgets()
        self.add_widget(Label(text='Edit Storage', font_size=24, 
                              font_name='Verdana', size_hint_y=None,
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


class GroceryPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=dp(12), spacing=dp(8), **kwargs)

        app = App.get_running_app()
        if not hasattr(app, 'grocery_list') or app.grocery_list is None:
            app.grocery_list = GroceryList()
        self.grocery_list: GroceryList = app.grocery_list

        self.add_widget(Label(text='Grocery List', font_size=20, size_hint_y=None, height=dp(40)))
        self.add_widget(Button(text='Back to Home', size_hint_y=None, height=dp(40), on_press=self.go_home))

        row = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        self.name_input = TextInput(hint_text='Name', multiline=False)
        self.qty_input = TextInput(hint_text='Qty', multiline=False, input_filter='int', size_hint_x=None, width=dp(80))
        add_btn = Button(text='Add', size_hint_x=None, width=dp(80), on_press=self._on_add)
        row.add_widget(self.name_input)
        row.add_widget(self.qty_input)
        row.add_widget(add_btn)
        self.add_widget(row)

        self.scroll = ScrollView()
        self.list_grid = GridLayout(cols=1, size_hint_y=None, spacing=dp(6), padding=dp(6))
        self.list_grid.bind(minimum_height=self.list_grid.setter('height'))
        self.scroll.add_widget(self.list_grid)
        self.add_widget(self.scroll)

        self.refresh()

    def go_home(self, instance):
        App.get_running_app().sm.current = 'home'

    def _on_add(self, instance):
        name = (self.name_input.text or '').strip()
        if not name:
            return
        try:
            qty = int(self.qty_input.text) if self.qty_input.text.strip() != '' else 1
        except ValueError:
            qty = 1

        try:
            item = Item(name, qty)
        except Exception:
            item = Item(name, qty)  

        item.quantity = qty
        setattr(item, 'picked', False)

        try:
            self.grocery_list.add_item(item)
        except Exception:
            if not hasattr(self.grocery_list, 'items'):
                self.grocery_list.items = {}
            self.grocery_list.items[item.name] = item

        self.name_input.text = ''
        self.qty_input.text = ''
        self.refresh()

    def refresh(self):
        self.list_grid.clear_widgets()
        items = getattr(self.grocery_list, 'items', {}) or {}
        for it in sorted(items.values(), key=lambda i: i.name.lower()):
            line = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(8))

            lbl = Label(text=f'{it.name} — {it.quantity}', size_hint_x=0.8, halign='left')
            lbl.bind(size=lbl.setter('text_size'))
            line.add_widget(lbl)

            picked_cb = CheckBox(active=getattr(it, 'picked', False), size_hint_x=None, width=dp(40))
            picked_cb.bind(active=lambda cb, val, n=it.name: self._set_picked(n, val))
            line.add_widget(picked_cb)

            remove_btn = Button(text='Remove', size_hint_x=None, width=dp(80))
            remove_btn.bind(on_press=lambda btn, n=it.name: self._remove_item(n))
            line.add_widget(remove_btn)

            self.list_grid.add_widget(line)

    def _set_picked(self, name: str, picked: bool):
        items = getattr(self.grocery_list, 'items', {})
        itm = items.get(name)
        if not itm:
            return
        setattr(itm, 'picked', bool(picked))

    def _remove_item(self, name: str):
        items = getattr(self.grocery_list, 'items', {})
        items.pop(name, None)
        self.refresh()


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(HomePage())

class StoreManagerScreen(Screen):
    def __init__(self, inventory_manager: InventoryManager, **kwargs):
        super().__init__(**kwargs)
        self.page = StorageManagerPage(inventory_manager)
        self.add_widget(self.page)
    
    def on_enter(self, *args):
        self.page.on_enter()

class GroceryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(GroceryPage())

class EditSMScreen(Screen):
    def __init__(self, inventory_manager: InventoryManager, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(EditSMPage())

class InventoryApp(App):
    def build(self):
        self.inventory_manager = InventoryManager()
        self.sm = ScreenManager()
        self.storage_locations = ['Pantry', 'Fridge', 'Freezer']
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(EditSMScreen(self.inventory_manager, name='edit_SM'))
        self.sm.add_widget(StoreManagerScreen(self.inventory_manager, name='store manager'))
        self.sm.add_widget(GroceryScreen(name='grocery'))
        return self.sm

if __name__ == '__main__':
    InventoryApp().run()