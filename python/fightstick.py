from gi.repository import Gtk, GdkPixbuf, Gdk
import os, sys

class GUI:
	def __init__(self):
		window = Gtk.Window()
		window.set_title ("Fightstick Display")
		window.connect_after('destroy', self.destroy)

		window.show_all()

	def destroy(window, self):
		Gtk.main_quit()

def main():
	app = GUI()
	Gtk.main()

if __name__ == "__main__":
    sys.exit(main())
