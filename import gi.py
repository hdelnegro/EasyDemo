import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Demo App")
        self.set_border_width(10)
        self.set_default_size(300, 150)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        label = Gtk.Label(label="Welcome to Flatpak!")
        vbox.pack_start(label, True, True, 0)

        button = Gtk.Button(label="Close")
        button.connect("clicked", Gtk.main_quit)
        button.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(button, False, False, 0)

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
