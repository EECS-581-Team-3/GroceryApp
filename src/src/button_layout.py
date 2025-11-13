from button_model import ButtonModel
from kivy.uix.boxlayout import BoxLayout


class ButtonLayout(BoxLayout):
    def __init__(self, pantry_callback, grocery_callback, **kwargs):
        super(ButtonLayout, self).__init__(orientation='vertical', spacing=30, padding=40, **kwargs)
        btn1 = ButtonModel(text="My Pantry", callback=pantry_callback)
        self.add_widget(btn1)
        btn2 = ButtonModel(text="Grocery List", callback=grocery_callback)
        self.add_widget(btn2)

