from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        btn = Button(
            text="Click Me",
            size_hint=(None, None),
            size=(150, 50),
            background_normal='',              # remove default image
            background_color=(0.2, 0.6, 0.8, 1),  # solid teal background
            color=(1, 1, 1, 1)                 # white text
        )

        layout.add_widget(btn)
        return layout

if __name__ == "__main__":
    MyApp().run()
