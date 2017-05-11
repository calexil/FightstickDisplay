import pyglet
from configparser import ConfigParser

#######################################################
#   Main scene:
#######################################################
pyglet.resource.path.append("theme")
pyglet.resource.reindex()
window = pyglet.window.Window(width=640, height=391, caption="Fightstick Display", resizable=True)
window.set_icon(pyglet.resource.image("icon.png"))
config = ConfigParser()
FIGHTSTICK_PLUGGED = False


@window.event
def on_resize(width, height):
    pyglet.gl.glLoadIdentity()
    scale_x = width / 640
    scale_y = height / 391
    pyglet.gl.glScalef(scale_x, scale_y, 1.0)


_layout = {
    "background": (0, 0),
    "stick": (119, 155),
    "select": (50, 319),
    "start": (50, 319),
    "x": (256, 84),
    "y": (336, 114),
    "lt": (421, 113),
    "rt": (507, 110),
    "a": (275, 174),
    "b": (354, 204),
    "lb": (440, 203),
    "rb": (527, 200),
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


def _make_sprite(name, batch, group, visible=True):
    """Helper function to make a sprite"""
    image = pyglet.resource.image(_images[name])
    position = _layout[name]
    sprite = pyglet.sprite.Sprite(image, *position, batch=batch, group=group)
    sprite.visible = visible
    return sprite


class TryAgainScene:
    """A scene that tells you to try again if no stick is detected."""
    def __init__(self, window_instance):
        self.window = window_instance
        self.missing_img = pyglet.resource.image("missing.png")

        @self.window.event
        def on_draw():
            self.window.clear()
            self.missing_img.blit(0, 0)


class MainScene:
    """The main scene, with all fightstick events wired up."""
    def __init__(self, window_instance, fightstick):
        self.window = window_instance
        self.batch = pyglet.graphics.Batch()
        self.fightstick = fightstick
        self.fightstick.open()

        ####################################################
        # Ordered Groups to handle draw order of the sprites:
        ####################################################
        self.bg = pyglet.graphics.OrderedGroup(0)
        self.fg = pyglet.graphics.OrderedGroup(1)

        ####################################################
        # Create all sprites using helper function (name, batch, group, visible):
        ####################################################
        self.background = _make_sprite('background', self.batch, self.bg)
        self.stick_spr = _make_sprite('stick', self.batch, self.fg)
        self.select_spr = _make_sprite('select', self.batch, self.fg, False)
        self.start_spr = _make_sprite('start', self.batch, self.fg, False)
        self.x_spr = _make_sprite('x', self.batch, self.fg, False)
        self.y_spr = _make_sprite('y', self.batch, self.fg, False)
        self.a_spr = _make_sprite('a', self.batch, self.fg, False)
        self.b_spr = _make_sprite('b', self.batch, self.fg, False)
        self.lb_spr = _make_sprite('lb', self.batch, self.fg, False)
        self.rb_spr = _make_sprite('rb', self.batch, self.fg, False)
        self.rt_spr = _make_sprite('lt', self.batch, self.fg, False)
        self.lt_spr = _make_sprite('rt', self.batch, self.fg, False)

        button_mapping = {"a": self.x_spr, "b": self.y_spr, "x": self.rb_spr, "y": self.lb_spr,
                          "leftshoulder": self.a_spr, "rightshoulder": self.b_spr,
                          "righttrigger": self.rt_spr, "lefttrigger": self.lt_spr,
                          "back": self.select_spr, "start": self.start_spr}

        @fightstick.event
        def on_button_press(controller, button):
            pressed_button = button_mapping.get(button)
            if pressed_button:
                pressed_button.visible = True

        @fightstick.event
        def on_button_release(controller, button):
            pressed_button = button_mapping.get(button)
            if pressed_button:
                pressed_button.visible = False

        @fightstick.event
        def on_stick_motion(controller, stick, xvalue, yvalue):
            if stick == "leftstick":
                center_x, center_y = _layout['stick']
                center_x += (xvalue * 50)
                center_y += (yvalue * 50)
                self.stick_spr.position = center_x, center_y

        @fightstick.event
        def on_dpad_motion(controller, dpleft, dpright, dpup, dpdown):
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

        @fightstick.event
        def on_trigger_motion(controller, trigger, value):
            if trigger == "lefttrigger":
                if value > 0.5:
                    self.rt_spr.visible = True
                elif value < -0.5:
                    self.rt_spr.visible = False
            if trigger == "righttrigger":
                if value > 0.5:
                    self.lt_spr.visible = True
                elif value < -0.5:
                    self.lt_spr.visible = False

        ###################################################
        # Window event to draw everything when necessary:
        ###################################################
        @self.window.event
        def on_draw():
            self.window.clear()
            self.batch.draw()


####################################################
# Load up either the full scene, or just the "try again" scene.
####################################################
def set_scene(dt):
    global FIGHTSTICK_PLUGGED
    controllers = pyglet.input.get_game_controllers()

    # print(len(controllers), "controllers")
    # print("plugged", FIGHTSTICK_PLUGGED)

    if len(controllers) > 0 and FIGHTSTICK_PLUGGED is False:
        controller = controllers[0]
        scene = MainScene(window, controller)
        FIGHTSTICK_PLUGGED = True
    elif len(controllers) == 0:
        scene = TryAgainScene(window)
        FIGHTSTICK_PLUGGED = False


if __name__ == "__main__":
    load_configuration()
    set_scene(0)     # Call it once immediately
    pyglet.clock.schedule_interval(set_scene, 3.0)
    pyglet.clock.schedule_interval(lambda dt: None, 1/60.0)
    pyglet.app.run()
