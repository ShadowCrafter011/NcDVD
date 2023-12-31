#!/home/lukas/player/venv/bin/python3


from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from remote import Remote
import sys


class Grid(GridLayout):
    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)

        self.cols = 1

        self.keypresses = []

        self.add_widget(Label(text="Hello, World!", font_size=64))

        remote = Remote()
        remote.bind(on_keypress=self.reset)
        remote.bind(on_keypress=self.add_key)

    def add_key(self, instance, keycode, *args):        
        keypress_label = Label(text=f"Keypress {keycode}")
        self.add_widget(keypress_label)
        self.keypresses.append(keypress_label)

    def reset(self, instance, keycode, *args):
        if keycode != "KEY_HOME": return
        [self.remove_widget(keypress) for keypress in self.keypresses]


class NcDVD(App):
    def build(self):
        return Grid()
    

def run():
    Window.borderless = True
    Window.fullscreen = "auto"
    Window.show_cursor = False

    NcDVD().run()


if __name__ == "__main__":
    run()
