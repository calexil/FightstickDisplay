#!/usr/bin/python
# -*- coding: utf-8 -*-
#imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from multiprocessing import Process
import os, sys, time, inputs
from inputs import devices
print(devices.gamepads)
from inputs import get_gamepad
#Defs
background = ("images/fightstickclear.png")
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
app = None

# Start main code
#Render bg
class GUI:

	def __init__(self):
            self.window = Gtk.Window()
            self.image = Gtk.Image()
            self.background_image = self.image.set_from_file(background)
            self.image.set_size_request(width=640, height=391)
            self.window.set_title ("Fightstick Display")
            self.window.add(self.image)
            self.window.show_all()
            self.window.connect_after('destroy', self.destroy)

	def destroy(window, self):
		Gtk.main_quit()


def overlay(self):
    while 1:
        if (event.code) == ("ABS_HAT0Y") and (event.state) == (-1):
            window = Gtk.Window()
            overlay = Gtk.Overlay
            self.overlay.window.add()
            self.window.set_size_request(width=640, height=391)
            self.image.set_from_file(up)
            self.window.show_all()
        elif (event.code) == ("BTN_SELECT") and (event.state) == (4):
            print("close enough")

# Detect the button presses and load the print state
def inputloop():
    while 1:
        events = get_gamepad()
        for event in events:
#            print(event.code, event.state)
            if (event.code) == ("ABS_HAT0Y") and (event.state) == (-1):
                print("UP")
            elif (event.code) == ("ABS_HAT0Y") and (event.state) == (1):
                print("DOWN")
            elif (event.code) == ("ABS_HAT0X") and (event.state) == (-1):
                print("LEFT")
            elif (event.code) == ("ABS_HAT0X") and (event.state) == (1):
                print("RIGHT")
            elif (event.code) == ("BTN_NORTH") and (event.state) == (1):
                print("LP")
            elif (event.code) == ("BTN_WEST") and (event.state) == (1):
                print("MP")
            elif (event.code) == ("BTN_TR") and (event.state) == (1):
                print("HP")
            elif (event.code) == ("BTN_TL") and (event.state) == (1):
                print("LB")
            elif (event.code) == ("BTN_SOUTH") and (event.state) == (1):
                print("LK")
            elif (event.code) == ("BTN_EAST") and (event.state) == (1):
                print("MK")
            elif (event.code) == ("ABS_RZ") and (event.state) == (255):
                print("HK")
            elif (event.code) == ("ABS_Z") and (event.state) == (255):
                print("RB")
            elif (event.code) == ("BTN_START") and (event.state) == (1):
                print("START")
            elif (event.code) == ("BTN_SELECT") and (event.state) == (1):
                print("SELECT")


def main():
	Process(target=inputloop).start()
	app = GUI()
	Gtk.main()

if __name__ == "__main__":
    sys.exit(main())
