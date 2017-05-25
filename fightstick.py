import pyglet
from pyglet.gl import glViewport, glMatrixMode, glOrtho, glLoadIdentity, glScalef
from pyglet.gl import GL_PROJECTION, GL_MODELVIEW
from configparser import ConfigParser

##Main scene:##
pyglet.resource.path.append("theme")
pyglet.resource.reindex()
window = pyglet.window.Window(width=640, height=390,
                              caption="Fightstick Display",
                              resizable=True, vsync=True)
window.set_icon(pyglet.resource.image("icon.png"))
config = ConfigParser()
FIGHTSTICK_PLUGGED = False


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    scale_x = width / 640.0
    scale_y = height / 390.0
    glScalef(scale_x, scale_y, 1.0)


_layout = {
    "background": (0, 0),
    "stick": (119, 154),
    "select": (50, 318),
    "start": (50, 318),
    "x": (256, 83),
    "y": (336, 113),
    "lt": (421, 112),
    "rt": (507, 109),
    "a": (275, 173),
    "b": (354, 203),
    "lb": (440, 202),
    "rb": (527, 199),
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

##Load the button mapping config##
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

##Helper function to make a sprite##
def _make_sprite(name, batch, group, visible=True):
    image = pyglet.resource.image(_images[name])
    position = _layout[name]
    sprite = pyglet.sprite.Sprite(image, *position, batch=batch, group=group)
    sprite.visible = visible
    return sprite

##A scene that tells you to try again if no stick is detected.##
class TryAgainScene:
    def __init__(self, window_instance):
        self.window = window_instance
        self.missing_img = pyglet.resource.image("missing.png")

        @self.window.event
        def on_draw():
            self.window.clear()
            self.missing_img.blit(0, 0)

##The main scene, with all fightstick events wired up.##
class MainScene:
    def __init__(self, window_instance, fightstick):
        self.window = window_instance
        self.batch = pyglet.graphics.Batch()
        self.fightstick = fightstick
        self.fightstick.open()


        ##Ordered groups to handle draw order of the sprites:##
        self.bg = pyglet.graphics.OrderedGroup(0)
        self.fg = pyglet.graphics.OrderedGroup(1)


        ##Create all sprites using helper function (name, batch, group, visible):##
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
        self.triggerpoint = 0.8
        self.deadzone = 0.2

        ##Mapping and press/axis/abs event section below##
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
                if abs(xvalue) > self.deadzone:
                    center_x += (xvalue * 50)
                if abs(yvalue) > self.deadzone:
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
                if value > self.triggerpoint:
                    self.rt_spr.visible = True
                elif value < -self.triggerpoint:
                    self.rt_spr.visible = False
            if trigger == "righttrigger":
                if value > self.triggerpoint:
                    self.lt_spr.visible = True
                elif value < -self.triggerpoint:
                    self.lt_spr.visible = False


        ##Window event to draw everything when necessary:##
        @self.window.event
        def on_draw():
            self.window.clear()
            self.batch.draw()

##Enforce aspect ratio by readjusting the window height.##
def enforce_aspect_ratio(dt):
    aspect_ratio = 1.641025641
    target_width = int(window.height * aspect_ratio)
    target_height = int(window.width / aspect_ratio)

    if window.width != target_width and window.height != target_height:
        window.set_size(window.width, target_height)


##Load up either the full scene, or just the "try again" scene.##
def set_scene(dt):
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
    set_scene(0)     # Call it once immediately
    pyglet.clock.schedule_interval(set_scene, 3.0)
    pyglet.clock.schedule_interval(enforce_aspect_ratio, 1.0)
    pyglet.clock.schedule_interval(lambda dt: None, 1/60.0)
    pyglet.app.run()
