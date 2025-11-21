# freezer_screen.py
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

from backend.inventory_manager import InventoryManager
from frontend.components.table_cell import TableCell
from frontend.components.back_button import BackButtonModel
from frontend.components.home_button import HomeButtonModel
from frontend.components.edit_button import EditButtonModel

Window.size = (500, 750)
Window.clearcolor = (0.84, 0.95, 1, 1)


class FreezerScreen(Screen):
    def __init__(self, inventory_manager: InventoryManager, **kwargs):
        super().__init__(name='freezer', **kwargs)
        self.page = FreezerPage(inventory_manager)
        self.add_widget(self.page)
    
    def on_enter(self, *args):
        self.page.on_enter()


class FreezerPage(BoxLayout):
    def __init__(self, inventory_manager: InventoryManager, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.inventory_manager = inventory_manager
        self.build_layout()

    def build_layout(self):
        self.clear_widgets()
        
        self.add_widget(
            Label(
                text="[b]Freezer[/b]",
                markup=True,
                font_size="28sp",
                size_hint_y=None,
                height=dp(50),
                color=(0.0, 0.33, 0.43, 1),
            )
        )

        add_section = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(8),
            padding=(dp(12), dp(8))
        )
        
        self.item_name_input = TextInput(
            hint_text='Item Name',
            multiline=False,
            size_hint_x=0.4,
            background_color=(0.61, 0.867, 0.937, 1),
            foreground_color=(0.078, 0.369, 0.447, 1)
        )
        
        self.item_qty_input = TextInput(
            hint_text='Qty',
            multiline=False,
            input_filter='int',
            size_hint_x=0.2,
            background_color=(0.61, 0.867, 0.937, 1),
            foreground_color=(0.078, 0.369, 0.447, 1)
        )
        
        add_btn = Button(
            text='Add Item',
            size_hint_x=0.3,
            background_normal='',
            background_color=(0.61, 0.867, 0.937, 1),
            color=(0.078, 0.369, 0.447, 1),
            bold=True,
            on_press=self.add_item
        )
        
        add_section.add_widget(self.item_name_input)
        add_section.add_widget(self.item_qty_input)
        add_section.add_widget(add_btn)
        self.add_widget(add_section)

        scroll = ScrollView(size_hint=(1, 1))
        self.grid = GridLayout(
            cols=3,
            spacing=0,
            padding=0,
            size_hint_y=None,
            row_force_default=True,
            row_default_height=dp(40),
        )
        self.grid.bind(minimum_height=self.grid.setter("height"))

        for h in ("Qty", "Item", "Status"):
            self.grid.add_widget(
                TableCell(
                    text=h,
                    bold=True,
                    color=(0.0, 0.33, 0.43, 1),
                )
            )

        scroll.add_widget(self.grid)
        self.add_widget(scroll)

        footer = BoxLayout(
            orientation='horizontal', 
            spacing=80, 
            padding=125,
            size_hint_y=None,
            height=dp(100)
        )
        home_btn = HomeButtonModel(callback=self.go_home)
        edit_btn = EditButtonModel(callback=self.go_back)
        footer.add_widget(home_btn)
        footer.add_widget(edit_btn)
        self.add_widget(footer)
        
        self.refresh_items()

    def add_item(self, instance):
        """Add a new item to the freezer."""
        name = (self.item_name_input.text or '').strip()
        if not name:
            return
        
        try:
            qty = int(self.item_qty_input.text) if self.item_qty_input.text.strip() else 1
        except ValueError:
            qty = 1
        
        qty = max(1, qty)

        try:
            in_stock = qty > 0
            self.inventory_manager.addItem(name, qty, in_stock)

            all_items = self.inventory_manager.all_items()
            item = None
            for it in all_items:
                if it.name.lower() == name.lower():
                    item = it
                    break
            if item:
                item.location = 'Freezer'
                print(f"Added item: {item.name}, Qty: {item.quantity}, Location: {item.location}")
                
        except Exception as e:
            print(f"Error adding item: {e}")
            import traceback
            traceback.print_exc()

        self.item_name_input.text = ''
        self.item_qty_input.text = ''

        self.refresh_items()

    def refresh_items(self):
        self.grid.clear_widgets()
        
        for h in ("Qty", "Item", "Status"):
            self.grid.add_widget(
                TableCell(
                    text=h,
                    bold=True,
                    color=(0.0, 0.33, 0.43, 1),
                )
            )

        all_items = self.inventory_manager.all_items()
        freezer_items = [item for item in all_items if getattr(item, 'location', None) == 'Freezer']

        freezer_items.sort(key=lambda x: x.name.lower())

        for item in freezer_items:
            qty = item.quantity
            name = item.name
            status = "In Stock" if item.in_stock else "Out"
            
            self.grid.add_widget(TableCell(text=str(qty), color=(0, 0, 0, 1)))
            self.grid.add_widget(TableCell(text=name, color=(0, 0, 0, 1)))
            self.grid.add_widget(TableCell(text=status, color=(0, 0, 0, 1)))

    def on_enter(self, *args):
        self.refresh_items()

    def go_back(self, instance):
        App.get_running_app().sm.current = 'store manager'

    def go_home(self, instance):
        App.get_running_app().sm.current = 'home'

    def go_edit(self, instance):
        App.get_running_app().sm.current = 'edit_SM'


