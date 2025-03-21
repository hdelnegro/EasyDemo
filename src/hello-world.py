import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class HelloWorldApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Hello World")
        self.set_border_width(10)
        self.set_default_size(200, 100)

        label = Gtk.Label(label="Hello, World!")
        self.add(label)

win = HelloWorldApp()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
