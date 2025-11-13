from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class TwoColumnButtonScrollViewApp(App):
    def build(self):
        # Root scroll view
        scroll_view = ScrollView(size_hint=(1, 1))

        # GridLayout with 2 columns
        layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Generate 100 buttons
        for i in range(1, 101):
            btn = Button(
                text=f"Button {i}",
                size_hint_y=None,
                height=40
            )
            layout.add_widget(btn)

        scroll_view.add_widget(layout)
        return scroll_view


if __name__ == "__main__":
    TwoColumnButtonScrollViewApp().run()
