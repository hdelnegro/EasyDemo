#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import platform
import psutil
import datetime
import socket
import netifaces
import os

class DemoWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="System Information Viewer")
        self.set_default_size(600, 400)

        # Load CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            .header-label { font-size: 24px; font-weight: bold; margin: 10px; }
            .info-label { font-size: 14px; margin: 5px; }
            .info-value { font-size: 14px; margin: 5px; }
            .view-button { font-weight: bold; padding: 8px 15px; margin: 0 5px; }
            .view-button:checked { background: #3498db; color: white; }
        """)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Create header bar
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.set_title("System Information Viewer")
        self.set_titlebar(header)

        # Create main box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        # Create button box for view selection
        view_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        view_box.set_halign(Gtk.Align.CENTER)
        view_box.set_margin_top(10)
        view_box.set_margin_bottom(10)

        # Create view buttons
        self.sysinfo_button = Gtk.RadioButton.new_with_label_from_widget(None, "System")
        self.network_button = Gtk.RadioButton.new_with_label_from_widget(self.sysinfo_button, "Network")
        self.storage_button = Gtk.RadioButton.new_with_label_from_widget(self.sysinfo_button, "Storage")

        for button in [self.sysinfo_button, self.network_button, self.storage_button]:
            button.get_style_context().add_class("view-button")
            view_box.pack_start(button, False, False, 0)
            button.connect("toggled", self.on_view_button_toggled)

        vbox.pack_start(view_box, False, False, 0)

        # Create stack for different views
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        
        # Create grids for different views
        self.sysinfo_grid = self.create_grid()
        self.network_grid = self.create_grid()
        self.storage_grid = self.create_grid()

        # Add grids to stack
        self.stack.add_named(self.sysinfo_grid, "sysinfo")
        self.stack.add_named(self.network_grid, "network")
        self.stack.add_named(self.storage_grid, "storage")

        # Create main box
        vbox.pack_start(self.stack, True, True, 0)

        # Add refresh and quit buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)
        button_box.set_margin_bottom(20)

        # Update refresh button
        refresh_button = Gtk.Button()
        refresh_button.set_label("Refresh")
        refresh_icon = Gtk.Image.new_from_icon_name("view-refresh-symbolic", Gtk.IconSize.BUTTON)
        refresh_button.set_image(refresh_icon)
        refresh_button.set_always_show_image(True)
        refresh_button.connect("clicked", self.on_refresh_clicked)
        button_box.pack_start(refresh_button, False, False, 0)

        # Update quit button
        quit_button = Gtk.Button()
        quit_button.set_label("Quit")
        quit_icon = Gtk.Image.new_from_icon_name("application-exit-symbolic", Gtk.IconSize.BUTTON)
        quit_button.set_image(quit_icon)
        quit_button.set_always_show_image(True)
        quit_button.connect("clicked", self.on_quit_clicked)
        button_box.pack_start(quit_button, False, False, 0)

        vbox.pack_end(button_box, False, False, 0)

        # Initialize views
        self.update_current_view()

    def create_grid(self):
        grid = Gtk.Grid()
        grid.set_column_spacing(40)
        grid.set_row_spacing(10)
        grid.set_margin_start(50)
        grid.set_margin_end(20)
        grid.set_margin_top(20)
        grid.set_margin_bottom(20)
        return grid

    def get_system_info(self):
        return [
            ("OS", platform.system() + " " + platform.release()),
            ("Architecture", platform.machine()),
            ("CPU Cores", str(psutil.cpu_count())),
            ("CPU Usage", f"{psutil.cpu_percent()}%"),
            ("Memory Total", f"{psutil.virtual_memory().total / (1024**3):.2f} GB"),
            ("Memory Available", f"{psutil.virtual_memory().available / (1024**3):.2f} GB"),
            ("Boot Time", datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))
        ]

    def get_network_info(self):
        info = []
        try:
            hostname = socket.gethostname()
            
            # Get default interface info
            gw_info = netifaces.gateways().get('default', {}).get(netifaces.AF_INET, [None, None])
            if not gw_info[1]:  # If no default interface found, use first available
                interfaces = netifaces.interfaces()
                default_iface = next((i for i in interfaces if i != 'lo'), None)
            else:
                default_iface = gw_info[1]

            if default_iface:
                addrs = netifaces.ifaddresses(default_iface)
                ipv4_info = addrs.get(netifaces.AF_INET, [{}])[0]
                
                # Try to get MAC address, but don't fail if unavailable
                try:
                    mac = addrs.get(netifaces.AF_LINK, [{'addr': 'N/A'}])[0]['addr']
                except:
                    mac = 'N/A'

                # Get DNS servers
                dns = []
                try:
                    with open('/etc/resolv.conf', 'r') as f:
                        for line in f:
                            if line.startswith('nameserver'):
                                dns.append(line.split()[1])
                except:
                    dns = ['N/A']

                info = [
                    ("Hostname", hostname),
                    ("Interface", default_iface),
                    ("IPv4 Address", ipv4_info.get('addr', 'N/A')),
                    ("Netmask", ipv4_info.get('netmask', 'N/A')),
                    ("Gateway", gw_info[0] or 'N/A'),
                    ("DNS Servers", ', '.join(dns)),
                    ("MAC Address", mac)
                ]
            else:
                info = [("Error", "No network interface found")]
        except Exception as e:
            info = [("Error", f"Network information unavailable: {str(e)}")]
        return info

    def get_storage_info(self):
        info = []
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                info.append((
                    partition.mountpoint,
                    f"Total: {usage.total / (1024**3):.1f}GB, "
                    f"Used: {usage.used / (1024**3):.1f}GB, "
                    f"Free: {usage.free / (1024**3):.1f}GB "
                    f"({usage.percent}% used)"
                ))
            except Exception:
                pass
        return info

    def update_grid(self, grid, info):
        for child in grid.get_children():
            grid.remove(child)

        for row, (label, value) in enumerate(info):
            label_widget = Gtk.Label(label=f"{label}:")
            label_widget.get_style_context().add_class("info-label")
            label_widget.set_halign(Gtk.Align.START)
            
            value_widget = Gtk.Label(label=value)
            value_widget.get_style_context().add_class("info-value")
            value_widget.set_halign(Gtk.Align.START)
            value_widget.set_line_wrap(True)
            
            grid.attach(label_widget, 0, row, 1, 1)
            grid.attach(value_widget, 1, row, 1, 1)
        
        grid.show_all()

    def update_current_view(self):
        if self.sysinfo_button.get_active():
            self.stack.set_visible_child_name("sysinfo")
            self.update_grid(self.sysinfo_grid, self.get_system_info())
        elif self.network_button.get_active():
            self.stack.set_visible_child_name("network")
            self.update_grid(self.network_grid, self.get_network_info())
        else:
            self.stack.set_visible_child_name("storage")
            self.update_grid(self.storage_grid, self.get_storage_info())

    def on_view_button_toggled(self, button):
        if button.get_active():
            self.update_current_view()

    def on_refresh_clicked(self, button):
        self.update_current_view()

    def on_quit_clicked(self, button):
        Gtk.main_quit()

win = DemoWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()