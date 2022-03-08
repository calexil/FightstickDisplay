import os
import sys
import urllib.request
from configparser import ConfigParser

import pyglet
from pyglet.util import debug_print
from pyglet.math import Mat4, Vec3


_debug_flag = len(sys.argv) > 1 and sys.argv[1] in ('-D', '-d', '--debug')
_debug_print = debug_print(_debug_flag)


pyglet.resource.path.append("theme")
pyglet.resource.reindex()

window = pyglet.window.Window(640, 390, caption="Fightstick Display", resizable=True, vsync=False)
window.set_icon(pyglet.resource.image("icon.png"))
config = ConfigParser()


# Parse and add additional SDL style controller mappings.
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


_layout = {
    "background": (0, 0),
    "stick": (119, 154),
    "select": (50, 318),
    "start": (50, 318),
    "a": (256, 83),
    "b": (336, 113),
    "rt": (421, 112),
    "lt": (507, 109),
    "x": (275, 173),
    "y": (354, 203),
    "rb": (440, 202),
    "lb": (527, 199),
}

_images = {
    'background': 'background.png',
    'stick': 'stick.png',
    'select': 'select.png',
    'start': 'start.png',
    'x': 'button.png',
    'y': 'button.png',
    'lt': 'button.png',
    'rt': 'button.png',
    'a': 'button.png',
    'b': 'button.png',
    'lb': 'button.png',
    'rb': 'button.png',
}


def load_configuration():
    # Load the button mapping configuration.
    global _layout, _images
    layout = _layout.copy()
    images = _images.copy()
    loaded_configs = config.read('theme/layout.ini')
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
            print("Invalid theme/layout.ini file. Falling back to default.")
    else:
        print("No theme/layout.ini file found. Falling back to default.")


def save_configuration():
    with open('theme/layout.ini', 'w') as file:
        config.write(file)


def _make_sprite(name, batch, group, visible=True):
    # Helper function to make a Sprite.
    image = pyglet.resource.image(_images[name])
    position = _layout[name]
    sprite = pyglet.sprite.Sprite(image, *position, batch=batch, group=group)
    sprite.visible = visible
    return sprite


#########################
#   Scene definitions:
#########################

class _BaseScene:
    manager:    None

    def activate(self):
        pass

    def deactivate(self):
        pass


class RetryScene(_BaseScene):
    """A scene that tells you to try again if no stick is detected."""
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.missing_img = pyglet.resource.image("missing.png")
        self.sprite = pyglet.sprite.Sprite(img=pyglet.resource.image("missing.png"), batch=self.batch)

    def on_button_press(self, controller, button):
        # If a Controller button was pressed, one must be plugged in.
        self.manager.set_scene('main')


class ConfigScene(_BaseScene):
    """A scene to allow deadzone configuration."""
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        bar = pyglet.resource.image("bar.png")
        knob = pyglet.resource.image("knob.png")
        bg_img = pyglet.resource.image('deadzone.png')
        self.bg = pyglet.sprite.Sprite(bg_img, batch=self.batch, group=pyglet.graphics.Group(-1))

        self.stick_slider = pyglet.gui.Slider(100, 150, bar, knob, edge=0, batch=self.batch)
        self.stick_slider.set_handler('on_change', self._stick_slider_handler)
        self.stick_label = pyglet.text.Label("Stick Deadzone: 0.0", x=300, y=300, batch=self.batch)

        self.trigger_slider = pyglet.gui.Slider(100, 100, bar, knob, edge=0, batch=self.batch)
        self.trigger_slider.set_handler('on_change', self._trigger_slider_handler)
        self.trigger_label = pyglet.text.Label("Trigger Deadzone: 0.0", x=300, y=200, batch=self.batch)

    def activate(self):
        self.stick_slider.value = self.manager.stick_deadzone * 100
        self.trigger_slider.value = self.manager.trigger_deadzone * 100
        self.manager.window.push_handlers(self.stick_slider)
        self.manager.window.push_handlers(self.trigger_slider)

    def deactivate(self):
        self.manager.window.remove_handlers(self.stick_slider)
        self.manager.window.remove_handlers(self.trigger_slider)

    def _stick_slider_handler(self, value):
        self.stick_label.text = f"Stick Deadzone: {value}"
        scaled_value = round(value / 100, 2)
        self.manager.stick_deadzone = scaled_value
        config.set('deadzones', 'stick', str(scaled_value))

    def _trigger_slider_handler(self, value):
        self.trigger_label.text = f"Trigger Deadzone: {value}"
        scaled_value = round(value / 100, 2)
        self.manager.trigger_deadzone = scaled_value
        config.set('deadzones', 'trigger', str(scaled_value))

    def on_button_press(self, controller, button):
        if button == "guide":
            save_configuration()
            self.manager.set_scene('main')


class MainScene(_BaseScene):
    """The main scene, with all fightstick events wired up."""
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        # Ordered groups to handle draw order of the sprites.
        self.bg = pyglet.graphics.Group(0)
        self.fg = pyglet.graphics.Group(1)
        # Create all sprites using helper function (name, batch, group, visible).
        self.background = _make_sprite('background', self.batch, self.bg)
        self.stick_spr = _make_sprite('stick', self.batch, self.fg)
        self.select_spr = _make_sprite('select', self.batch, self.fg, False)
        self.start_spr = _make_sprite('start', self.batch, self.fg, False)
        self.x_spr = _make_sprite('x', self.batch, self.fg, False)
        self.y_spr = _make_sprite('y', self.batch, self.fg, False)
        self.a_spr = _make_sprite('a', self.batch, self.fg, False)
        self.b_spr = _make_sprite('b', self.batch, self.fg, False)
        self.rb_spr = _make_sprite('rb', self.batch, self.fg, False)
        self.lb_spr = _make_sprite('lb', self.batch, self.fg, False)
        self.rt_spr = _make_sprite('rt', self.batch, self.fg, False)
        self.lt_spr = _make_sprite('lt', self.batch, self.fg, False)

        # Mapping of (Input names : Sprite names).
        self.button_mapping = {"a": self.a_spr, "b": self.b_spr, "x": self.x_spr, "y": self.y_spr,
                               "rightshoulder": self.rb_spr, "leftshoulder": self.lb_spr,
                               "righttrigger": self.rt_spr, "lefttrigger": self.lt_spr,
                               "back": self.select_spr, "start": self.start_spr}

    def on_button_press(self, controller, button):
        assert _debug_print(f"Pressed Button: {button}")
        if button == "guide":
            self.manager.set_scene('config')
        pressed_button = self.button_mapping.get(button, None)
        if pressed_button:
            pressed_button.visible = True

    def on_button_release(self, controller, button):
        pressed_button = self.button_mapping.get(button, None)
        if pressed_button:
            pressed_button.visible = False

    def on_stick_motion(self, controller, stick, xvalue, yvalue):
        if stick == "leftstick":
            center_x, center_y = _layout['stick']
            if abs(xvalue) > self.manager.stick_deadzone:
                center_x += (xvalue * 50)
                assert _debug_print(f"Moved Stick: {stick}, {xvalue, yvalue}")
            if abs(yvalue) > self.manager.stick_deadzone:
                center_y += (yvalue * 50)
                assert _debug_print(f"Moved Stick: {stick}, {xvalue, yvalue}")
            self.stick_spr.position = center_x, center_y

    def on_dpad_motion(self, controller, dpleft, dpright, dpup, dpdown):
        assert _debug_print(f"Dpad  Left:{dpleft}, Right:{dpright}, Up:{dpup}, Down:{dpdown}")
        center_x, center_y = _layout["stick"]
        if dpup:
            center_y += 50
        elif dpdown:
            center_y -= 50
        if dpleft:
            center_x -= 50
        elif dpright:
            center_x += 50
        self.stick_spr.position = center_x, center_y

    def on_trigger_motion(self, controller, trigger, value):
        assert _debug_print(f"Pulled Trigger: {trigger}")
        if trigger == "lefttrigger":
            if value > self.manager.trigger_deadzone:
                self.lt_spr.visible = True
            elif value < -self.manager.trigger_deadzone:
                self.lt_spr.visible = False
        if trigger == "righttrigger":
            if value > self.manager.trigger_deadzone:
                self.rt_spr.visible = True
            elif value < -self.manager.trigger_deadzone:
                self.rt_spr.visible = False


#####################################################
#   SceneManager class to handle Scene Switching:
#####################################################

class SceneManager:
    """A Scene Management class.

    The SceneManager is responsible for switching between
    the various scenes cleanly. This includes setting and
    removing Window and Controller events handlers. Global
    state (deadzone, etc.) is also defined here.

    """
    def __init__(self, window_instance):
        self.window = window_instance
        self.window.push_handlers(self)

        controllers = pyglet.input.get_controllers()
        if not controllers:
            print("No controllers found")
            exit()

        self.fightstick = controllers[0]
        self.fightstick.open()

        self._scenes = {}
        self._current_scene = None

        # Global state for all Scenes:
        self.stick_deadzone = float(config.get('deadzones', 'stick', fallback='0.2'))
        self.trigger_deadzone = float(config.get('deadzones', 'trigger', fallback='0.8'))

    def add_scene(self, name, instance):
        instance.manager = self
        self._scenes[name] = instance

    def set_scene(self, name):
        if self._current_scene:
            self.window.remove_handlers(self._current_scene)
            self.fightstick.remove_handlers(self._current_scene)
            self._current_scene.deactivate()

        new_scene = self._scenes[name]
        self.window.push_handlers(new_scene)
        self.fightstick.push_handlers(new_scene)

        self._current_scene = new_scene
        self._current_scene.activate()

    def enforce_aspect_ratio(self, dt):
        # Enforce aspect ratio by readjusting the window height.
        aspect_ratio = 1.641025641
        target_width = int(window.height * aspect_ratio)
        target_height = int(window.width / aspect_ratio)

        if self.window.width != target_width and self.window.height != target_height:
            self.window.set_size(window.width, target_height)

    # Window Events:

    def on_draw(self):
        self.window.clear()
        self._current_scene.batch.draw()

    def on_resize(self, width, height):
        projection_matrix = Mat4.orthogonal_projection(0, width, 0, height, 0, 1)
        scale_x = width / 640.0
        scale_y = height / 390.0
        self.window.projection = projection_matrix.scale(Vec3(scale_x, scale_y, 1))
        self.window.viewport = 0, 0, width, height
        return pyglet.event.EVENT_HANDLED


if __name__ == "__main__":
    load_configuration()

    scene_manager = SceneManager(window_instance=window)
    scene_manager.add_scene('main', MainScene())
    scene_manager.add_scene('retry', RetryScene())
    scene_manager.add_scene('config', ConfigScene())

    scene_manager.set_scene('main')

    pyglet.clock.schedule_interval(scene_manager.enforce_aspect_ratio, 0.3)
    pyglet.app.run()
