# grocery_screen.py
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.metrics import dp
from kivy.core.window import Window

import os

from backend.item import Item
from backend.grocery_list import GroceryList

Window.size = (500, 750)
Window.clearcolor = (0.84, 0.95, 1, 1)

folder_path = os.path.join(os.path.dirname(__file__), 'images')
top_img_path = os.path.join(folder_path, 'top.png')
bottom_img_path = os.path.join(folder_path, 'bottom.png')

class GroceryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(GroceryPage())


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



