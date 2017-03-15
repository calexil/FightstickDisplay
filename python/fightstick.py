#!/usr/bin/python
# -*- coding: utf-8 -*-
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import os, sys, time
import inputs
from inputs import devices
print(devices.gamepads)
from inputs import get_gamepad
file_name = ("images/fightstickclear.png")
up = ("images/up.png")


events = get_gamepad()
for event in events:
    event.code=('ABS_HAT0Y', -1)
    self.overlay = Gtk.Overlay()
    self.add(self.overlay)
    self.image.set_from_file(up)

class GUI:

	def __init__(self):
            self.window = Gtk.Window()
            self.image = Gtk.Image()
            self.image.set_from_file(file_name)
            self.image.set_size_request(width=640, height=391)
            self.window.set_title ("Fightstick Display")
            self.window.add(self.image)
            self.window.show_all()
            self.window.connect_after('destroy', self.destroy)
            
	def destroy(window, self):
		Gtk.main_quit()

def main():
	app = GUI()
	Gtk.main()

if __name__ == "__main__":
    sys.exit(main())
