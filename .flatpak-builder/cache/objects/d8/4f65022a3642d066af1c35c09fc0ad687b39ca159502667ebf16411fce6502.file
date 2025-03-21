#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import platform
import psutil
import datetime

class DemoWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="System Information Viewer")
        self.set_default_size(600, 400)
        self.set_border_width(10)

        # Create a vertical box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # Create a scrolled window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(scrolled, True, True, 0)

        # Create a vertical box for the system info
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        scrolled.add(info_box)

        # Collect system information
        system_info = [
            ("OS", platform.system() + " " + platform.release()),
            ("Architecture", platform.machine()),
            ("CPU Cores", str(psutil.cpu_count())),
            ("CPU Usage", f"{psutil.cpu_percent()}%"),
            ("Memory Total", f"{psutil.virtual_memory().total / (1024**3):.2f} GB"),
            ("Memory Available", f"{psutil.virtual_memory().available / (1024**3):.2f} GB"),
            ("Boot Time", datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))
        ]

        # Add system information to the window
        for label, value in system_info:
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
            label_widget = Gtk.Label(label=f"{label}:")
            label_widget.set_halign(Gtk.Align.START)
            value_widget = Gtk.Label(label=value)
            value_widget.set_halign(Gtk.Align.START)
            hbox.pack_start(label_widget, False, False, 0)
            hbox.pack_start(value_widget, False, False, 0)
            info_box.pack_start(hbox, False, False, 0)

        # Add refresh button
        refresh_button = Gtk.Button(label="Refresh")
        refresh_button.connect("clicked", self.on_refresh_clicked)
        vbox.pack_start(refresh_button, False, False, 0)

        # Add quit button
        quit_button = Gtk.Button(label="Quit")
        quit_button.connect("clicked", self.on_quit_clicked)
        vbox.pack_start(quit_button, False, False, 0)

    def on_refresh_clicked(self, button):
        # TODO: Update system information
        pass

    def on_quit_clicked(self, button):
        Gtk.main_quit()

win = DemoWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()