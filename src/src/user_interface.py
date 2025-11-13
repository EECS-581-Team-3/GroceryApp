from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.metrics import dp
from inventory_manager import InventoryManager
from item import Item
from grocery_list import GroceryList

class HomePage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=dp(20), spacing=dp(12), **kwargs)
        self.add_widget(Label(text='Pantry Pro', font_size=32, size_hint_y=None, height=dp(56)))
        self.add_widget(Button(text='Add Item to Inventory', size_hint_y=None, height=dp(48), on_press=self.go_add))
        self.add_widget(Button(text='View Inventory', size_hint_y=None, height=dp(48), on_press=self.go_inventory))
        self.add_widget(Button(text='View Grocery List', size_hint_y=None, height=dp(48), on_press=self.go_grocery))

    def go_add(self, instance):
        App.get_running_app().sm.current = 'add'

    def go_inventory(self, instance):
        App.get_running_app().sm.current = 'inventory'

    def go_grocery(self, instance):
        App.get_running_app().sm.current = 'grocery'

class InventoryPage(BoxLayout):
    def __init__(self, inventory_manager: InventoryManager, **kwargs):
        super().__init__(orientation='vertical', padding=dp(12), spacing=dp(8), **kwargs)
        self.inventory_manager = inventory_manager
        self.add_widget(Label(text='Inventory', font_size=24, size_hint_y=None, height=dp(48)))
        self.scroll = ScrollView(size_hint=(1, 1))
        self.grid = GridLayout(cols=1, size_hint_y=None, spacing=dp(6), padding=dp(6))
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        self.add_widget(self.scroll)
        footer = BoxLayout(size_hint_y=None, height=dp(56))
        footer.add_widget(Button(text='Back to Home', on_press=self.go_home))
        self.add_widget(footer)
        self.refresh()

    def refresh(self):
        self.grid.clear_widgets()
        for it in self.inventory_manager.all_items():
            status = 'In stock' if getattr(it, 'inStock', getattr(it, 'status', True)) else 'Out of stock'
            lbl = Label(text=f'{it.name} — {it.quantity} — {status}', size_hint_y=None, height=dp(32))
            self.grid.add_widget(lbl)

    def go_home(self, instance):
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



class AddItemPage(BoxLayout):
    def __init__(self, inventory_manager: InventoryManager, **kwargs):
        super().__init__(orientation='vertical', padding=dp(12), spacing=dp(8), **kwargs)
        self.inventory_manager = inventory_manager
        self.add_widget(Label(text='Add Item', font_size=24, size_hint_y=None, height=dp(48)))
        self.name_input = TextInput(hint_text='Item name', size_hint_y=None, height=dp(40))
        self.add_widget(self.name_input)
        self.qty_input = TextInput(hint_text='Quantity (integer)', input_filter='int', size_hint_y=None, height=dp(40))
        self.add_widget(self.qty_input)
        row = BoxLayout(size_hint_y=None, height=dp(40))
        row.add_widget(Label(text='In Stock:', size_hint_x=None, width=dp(90)))
        self.in_stock_checkbox = CheckBox(active=True)
        row.add_widget(self.in_stock_checkbox)
        self.add_widget(row)
        btn_row = BoxLayout(size_hint_y=None, height=dp(56))
        btn_row.add_widget(Button(text='Cancel', on_press=self.go_home))
        btn_row.add_widget(Button(text='Add', on_press=self.on_add))
        self.add_widget(btn_row)

    def on_add(self, instance):
        name = self.name_input.text.strip()
        qty_text = self.qty_input.text.strip()
        if not name:
            return
        quantity = int(qty_text) if qty_text else 0
        in_stock = bool(self.in_stock_checkbox.active)
        if hasattr(self.inventory_manager, 'addItem'):
            self.inventory_manager.addItem(name, quantity, in_stock)
        else:
            self.inventory_manager.add_item(name, quantity, in_stock)
        self.name_input.text = ''
        self.qty_input.text = ''
        app = App.get_running_app()
        app.sm.current = 'inventory'
        try:
            inventory_screen = app.sm.get_screen('inventory')
            for child in inventory_screen.children:
                if isinstance(child, InventoryPage):
                    child.refresh()
                    break
        except Exception:
            pass

    def go_home(self, instance):
        App.get_running_app().sm.current = 'home'

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(HomePage())

class InventoryScreen(Screen):
    def __init__(self, inventory_manager: InventoryManager, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(InventoryPage(inventory_manager))

class GroceryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(GroceryPage())

class AddItemScreen(Screen):
    def __init__(self, inventory_manager: InventoryManager, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(AddItemPage(inventory_manager))

class InventoryApp(App):
    def build(self):
        inv = {}
        self.inventory_manager = InventoryManager(inv)
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(AddItemScreen(self.inventory_manager, name='add'))
        self.sm.add_widget(InventoryScreen(self.inventory_manager, name='inventory'))
        self.sm.add_widget(GroceryScreen(name='grocery'))
        return self.sm

if __name__ == '__main__':
    InventoryApp().run()