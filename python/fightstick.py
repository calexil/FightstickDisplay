#!/usr/bin/python
# -*- coding: utf-8 -*-
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import os, sys, time
import pygame
import inspect
file_name = ("images/fightstick_paneltemplate.png")
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
