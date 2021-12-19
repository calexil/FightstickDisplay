import os
import sys
import urllib.request
from configparser import ConfigParser

import pyglet
from pyglet.util import debug_print


_debug_flag = len(sys.argv) > 1 and sys.argv[1] in ('-D', '--debug')
_debug_print = debug_print(_debug_flag)


pyglet.resource.path.append("theme")
pyglet.resource.reindex()

window = pyglet.window.Window(640, 390, caption="Fightstick Display", resizable=True, vsync=False)
window.set_icon(pyglet.resource.image("icon.png"))

config = ConfigParser()
FIGHTSTICK_PLUGGED = False

# Parse and add additional SDL controller mappings.
url = "https://raw.githubusercontent.com/gabomdq/SDL_GameControllerDB/master/gamecontrollerdb.txt"
try:
    with urllib.request.urlopen(url) as response, open(os.path.dirname(__file__) + "/gamecontrollerdb.txt", 'wb') as f:
        f.write(response.read())
except Exception:
    if os.path.exists("gamecontrollerdb.txt"):
        try:
            pyglet.input.gamecontroller.add_mappings_from_file("gamecontrollerdb.txt")
            print("Added additional controller mappings from 'gamecontrollerdb.txt'")
        except Exception:
            print("Failed to parse 'gamecontrollerdb.txt'. Please open an issue on GitHub.")


@window.event
def on_resize(width, height):
    projection_matrix = pyglet.math.Mat4.orthogonal_projection(0, width, 0, height, 0, 1)
    scale_x = width / 640.0
    scale_y = height / 390.0
    window.projection = projection_matrix.scale(scale_x, scale_y, 1)
    window.viewport = 0, 0, width, height
    return pyglet.event.EVENT_HANDLED


_layout = {
    "background" : (0, 0),
    "select" : (50, 318),
    "start" : (50, 318),
    "up" : (237, 10),
    "down" : (133, 217),
    "left" : (47, 217),
    "right" : (209, 176),
    "a" : (284, 124),
    "b" : (364, 158),
    "x" : (290, 214),
    "y" : (369, 247),
    "rb" : (456, 246),
    "lb" : (543, 234),
    "rt" : (456, 159),
    "lt" : (540, 146),
}

_images = {
    'background': 'backgroundHB.png',
    'select': 'select.png',
    'start': 'start.png',
    'up' : 'buttonhblg.png',
    'down' : 'buttonhb.png',
    'left' : 'buttonhb.png',
    'right' : 'buttonhb.png',
    'a': 'buttonhb.png',
    'b': 'buttonhb.png',    
    'x': 'buttonhb.png',
    'y': 'buttonhb.png',
    'lt': 'buttonhb.png',
    'rt': 'buttonhb.png',
    'lb': 'buttonhb.png',
    'rb': 'buttonhb.png',
}


def load_configuration():
    # Load the button mapping configuration.
    global _layout, _images
    layout = _layout.copy()
    images = _images.copy()
    loaded_configs = config.read('theme/layouthb.ini')
    if len(loaded_configs) > 0:
        try:
            for key, value in config.items('layout'):
                x, y = value.split(', ')
                layout[key] = int(x), int(y)
            for key, value in config.items('images'):
                images[key] = value
            _layout = layout.copy()
            _images = images.copy()
        except KeyError:
            print("Invalid theme/layouthb.ini file. Falling back to default.")
    else:
        print("No theme/layouthb.ini file found. Falling back to default.")


def _make_sprite(name, batch, group, visible=True):
    # Helper function to make the batch sprite
    image = pyglet.resource.image(_images[name])
    position = _layout[name]
    sprite = pyglet.sprite.Sprite(image, *position, batch=batch, group=group)
    sprite.visible = visible
    return sprite


class TryAgainScene:
    # A scene that tells you to try plugging a controller in again if no stick is detected
    def __init__(self, window_instance):
        self.window = window_instance
        self.missing_img = pyglet.resource.image("missing.png")

        @self.window.event
        def on_draw():
            self.window.clear()
            self.missing_img.blit(0, 0)


class MainScene:
    # The Main Scene, with all fightstick events rigged.
    def __init__(self, window_instance, fightstick):
        self.window = window_instance
        self.batch = pyglet.graphics.Batch()
        self.fightstick = fightstick
        self.fightstick.open()
        # Ordered groups to handle draw order of the sprites
        self.bg = pyglet.graphics.Group(0)
        self.fg = pyglet.graphics.Group(1)
        # Create all sprites using helper function (name, batch, group, visible)
        self.background = _make_sprite('background', self.batch, self.bg)
        self.select_spr = _make_sprite('select', self.batch, self.fg, False)
        self.start_spr = _make_sprite('start', self.batch, self.fg, False)
        self.up_spr = _make_sprite('up', self.batch, self.fg, False)
        self.down_spr = _make_sprite('down', self.batch, self.fg, False)
        self.left_spr = _make_sprite('left', self.batch, self.fg, False)
        self.right_spr = _make_sprite('right', self.batch, self.fg, False)
        self.a_spr = _make_sprite('a', self.batch, self.fg, False)
        self.b_spr = _make_sprite('b', self.batch, self.fg, False)        
        self.x_spr = _make_sprite('x', self.batch, self.fg, False)
        self.y_spr = _make_sprite('y', self.batch, self.fg, False)
        self.rt_spr = _make_sprite('rt', self.batch, self.fg, False)
        self.lt_spr = _make_sprite('lt', self.batch, self.fg, False)
        self.rb_spr = _make_sprite('rb', self.batch, self.fg, False)        
        self.lb_spr = _make_sprite('lb', self.batch, self.fg, False)
        self.triggerpoint = 0.8
        self.deadzone = 0.2

        # Mapping and press/axis/abs event section below
        button_mapping = {"back": self.select_spr, "start": self.start_spr, 
                          "up": self.up_spr, "down": self.down_spr, "left": self.left_spr, "right": self.right_spr, 
                          "a": self.a_spr, "b": self.b_spr, "x": self.x_spr, "y": self.y_spr, 
                          "rightshoulder": self.rb_spr, "leftshoulder": self.lb_spr,                  
                          "righttrigger": self.rt_spr, "lefttrigger": self.lt_spr,}

        @fightstick.event
        def on_button_press(controller, button):
            assert _debug_print(f"Pressed Button: {button}")
            pressed_button = button_mapping.get(button, None)
            if pressed_button:
                pressed_button.visible = True

        @fightstick.event
        def on_button_release(controller, button):
            pressed_button = button_mapping.get(button, None)
            if pressed_button:
                pressed_button.visible = False

        #TODO UDLR, the dpad hats need to alert the main window to draw the sprites
        @fightstick.event
        def on_dpad_motion(controller, dpleft, dpright, dpup, dpdown):
            assert _debug_print(f"Dpad  Left:{dpleft}, Right:{dpright}, Up:{dpup}, Down:{dpdown}")         
            if dpup == True:
                self.up_spr.visible = True
            elif dpup == False:
                self.up_spr.visible = False
            if dpdown == True:
                self.down_spr.visible = True
            elif dpdown == False:
                self.down_spr.visible = False
            if dpleft == True:
                self.left_spr.visible = True
            elif dpleft == False:
                self.left_spr.visible = False
            if dpright == True:
                self.right_spr.visible = True
            elif dpright == False:
                self.right_spr.visible = False

        @fightstick.event
        def on_trigger_motion(controller, trigger, value):
            assert _debug_print(f"Pulled Trigger: {trigger}")
            if trigger == "lefttrigger":
                if value > self.triggerpoint:
                    self.lt_spr.visible = True
                elif value < -self.triggerpoint:
                    self.lt_spr.visible = False
            if trigger == "righttrigger":
                if value > self.triggerpoint:
                    self.rt_spr.visible = True
                elif value < -self.triggerpoint:
                    self.rt_spr.visible = False

        # Window event to draw everything when necessary
        @self.window.event
        def on_draw():
            self.window.clear()
            self.batch.draw()


def enforce_aspect_ratio(dt):
    # Enforce aspect ratio by readjusting the window height
    aspect_ratio = 1.641025641
    target_width = int(window.height * aspect_ratio)
    target_height = int(window.width / aspect_ratio)

    if window.width != target_width and window.height != target_height:
        window.set_size(window.width, target_height)


def set_scene(dt=0):
    # Load up either the full scene, or just the "try again" scene
    global FIGHTSTICK_PLUGGED
    controllers = pyglet.input.get_game_controllers()
    if len(controllers) > 0 and FIGHTSTICK_PLUGGED is False:
        controller = controllers[0]
        scene = MainScene(window, controller)
        FIGHTSTICK_PLUGGED = True
    elif len(controllers) == 0:
        scene = TryAgainScene(window)
        FIGHTSTICK_PLUGGED = False


if __name__ == "__main__":
    load_configuration()
    set_scene()
    # Schedulers for scene change, aspect enforce, and main display cycles(fps)
    pyglet.clock.schedule_interval(set_scene, 2.0)
    pyglet.clock.schedule_interval(enforce_aspect_ratio, 0.3)
    pyglet.app.run()
