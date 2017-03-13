from gi.repository import Gtk, GdkPixbuf, Gdk
import os, sys, time
import pygame
import inspect

class Stick:
    def __init__(self):
        try:
            pygame.init()
            self.fightstick = pygame.joystick.Joystick(0)
            self.fightstick.init()
        except:
            print "Unable to connect to Fightstick"
            sys.exit(1)

    def read(self):
        pygame.event.pump()
        # Directions
        up, down, left, right = [0, 0, 0, 0]
        hat = self.fightstick.get_hat(0)
        if hat[0] == 1: right = 1
        elif hat[0] == -1: left = 1
        if hat[1] == 1: up = 1
        elif hat[1] == -1: down = 1
        # Punches
        lp = self.fightstick.get_button(keycodes.LP)
        mp = self.fightstick.get_button(keycodes.MP)
        hp = self.fightstick.get_button(keycodes.HP)
        # Kicks
        lk = self.fightstick.get_button(keycodes.LK)
        mk = self.fightstick.get_button(keycodes.MK)
        hk = self.fightstick.get_button(keycodes.HK)
        # Return
        return [up, down, left, right, lp, mp, hp, lk, mk, hk]


class GUI:

	def __init__(self):

    # Create an Image object for a PNG file.
        file_name = "~/$USER/FightstickDisplay/images/madcatzfightstick_paneltemplate.png"
        pixbuf = gtk.gdk.pixbuf_new_from_file(file_name)
        pixmap, mask = pixbuf.render_pixmap_and_mask()
        image = gtk.Image()
        image.set_from_pixmap(pixmap, mask)

        # window and images
        window = Gtk.Window()
        window.set_title ("Fightstick Display")
        window.connect_after('destroy', self.destroy)

        window.add(image)
        window.show_all()

	def destroy(window, self):
		Gtk.main_quit()

def main():
	app = GUI()
	Gtk.main()

if __name__ == "__main__":
    sys.exit(main())
