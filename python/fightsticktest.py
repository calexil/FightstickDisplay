#!/usr/bin/python
# -*- coding: utf-8 -*-
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from multiprocessing import Process
import os, sys, time, inputs
from inputs import devices
print(devices.gamepads)
from inputs import get_gamepad
file_name = ("images/fightstickclear.png")
up = ("images/up.png")
down = ("images/down.png")
left = ("images/left.png")
right = ("images/right.png")
select = ("images/select.png")
start = ("images/start.png")
upright = ("images/upright.png")
downright = ("images/downright.png")
upleft = ("images/upleft.png")
downleft = ("images/downleft.png")
lp = ("images/lp.png")
mp = ("images/mp.png")
hp = ("images/hp.png")
lb = ("images/lb.png")
lk = ("images/lk.png")
mk = ("images/mk.png")
hk = ("images/hk.png")
rb = ("images/rb.png")
classWindow = Gtk.Window()

class GUI:

	def __init__(self):
            self.window = classWindow
            self.image = Gtk.Image()
            self.background_image = self.image.set_from_file(file_name)
            self.image.set_size_request(width=640, height=391)
            self.window.set_title ("Fightstick Display")
            self.window.add(self.image)
            self.window.show_all()
            self.window.connect_after('destroy', self.destroy)

	def destroy(window, self):
		Gtk.main_quit()


def inputloop():
	testImage = Gtk.Image()
	testImage.set_from_file(mk)
	testImage.show()
	classWindow.add(testImage)
	
	while 1:
		events = get_gamepad()
		for event in events:
			print(event.code, event.state)

def main():
	Process(target=inputloop).start()
	app = GUI()
	Gtk.main()

if __name__ == "__main__":
    sys.exit(main())
