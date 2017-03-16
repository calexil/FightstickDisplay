import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Button Event")

        self.connect("button-press-event", self.on_button_pressed)
        self.connect("button-release-event", self.on_button_released)

        self.overlay = Gtk.Overlay()
        self.add(self.overlay)

        self.background_image = Gtk.Image.new_from_icon_name("web-browser", Gtk.IconSize.INVALID)
        self.background_image.set_pixel_size(256)
        self.overlay.add(self.background_image)

        self.image = Gtk.Image.new_from_icon_name("window-close-symbolic", Gtk.IconSize.INVALID)
        self.image.set_pixel_size(128)
        self.overlay.add_overlay(self.image)
        self.image.set_no_show_all(True)

    def on_button_pressed(self, widget, event):
        self.image.show()

    def on_button_released(self, widget, event):
        self.image.hide()

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
