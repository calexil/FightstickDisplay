import pyglet
from simplui import Theme, Frame, Dialogue, Slider, Button, Label, VLayout
import json
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

#######################################################
#   These are constant no matter which scene:
#######################################################
pyglet.resource.path.append("theme")
pyglet.resource.reindex()
window = pyglet.window.Window(width=640, height=391, caption="Fightstick Display", vsync=True)
window.set_icon(pyglet.resource.image("icon.png"))
e = ("Invalid layout.json file. Falling back to default layout.")

_layout = {
    "background": (0, 0),
    "stick": (119, 155),
    "select": (0, 0),
    "start": (0, 0),
    "x": (256, 84),
    "y": (336, 114),
    "lt": (421, 113),
    "rt": (507, 110),
    "a": (275, 174),
    "b": (354, 204),
    "lb": (440, 203),
    "rb": (527, 200),
}


def layout_default():
    global _layout
    try:
        loaded_layout = json.load(pyglet.resource.file("layout.json"))
        default_layout = _layout.copy()
        for key in loaded_layout:
            default_layout[key] = loaded_layout[key]
        _layout = default_layout.copy()
    except Exception as e:
        print(e)


def _make_sprite(img, pos, batch, group, visible=True):
    """Helper function to make a sprite"""
    image = pyglet.resource.image(img)
    sprite = pyglet.sprite.Sprite(image, *pos, batch=batch, group=group)
    sprite.visible = visible
    return sprite


class TryAgainScene:
    """A scene that tells you to try again if no stick is detected."""
    def __init__(self, window_instance):
        self.window = window_instance
        self.missing_img = pyglet.resource.image("missing.png")

        @self.window.event
        def on_draw():
            window.clear()
            self.missing_img.blit(0, 0)


class MainScene:
    """The main cene, with all fightstick events wired up."""
    def __init__(self, window_instance, fightstick):
        self.window = window_instance
        self.batch = pyglet.graphics.Batch()
        self.fightstick = fightstick
        self.fightstick.open()

        # Ordered Groups to handle draw order of the sprites:
        self.bg = pyglet.graphics.OrderedGroup(0)
        self.fg = pyglet.graphics.OrderedGroup(1)

        # Create all sprites using helper function (image name, position, batch, group, visible):
        self.background = _make_sprite("background.png", _layout['background'], self.batch, self.bg)
        self.stick_spr = _make_sprite("stick.png", _layout['stick'], self.batch, self.fg)
        self.select_spr = _make_sprite("select.png", _layout['select'], self.batch, self.fg, False)
        self.start_spr = _make_sprite("start.png", _layout['start'], self.batch, self.fg, False)
        self.x_spr = _make_sprite("button.png", _layout['x'], self.batch, self.fg, False)
        self.y_spr = _make_sprite("button.png", _layout['y'], self.batch, self.fg, False)
        self.a_spr = _make_sprite("button.png", _layout['a'], self.batch, self.fg, False)
        self.b_spr = _make_sprite("button.png", _layout['b'], self.batch, self.fg, False)
        self.lb_spr = _make_sprite("button.png", _layout['lb'], self.batch, self.fg, False)
        self.rb_spr = _make_sprite("button.png", _layout['rb'], self.batch, self.fg, False)
        self.rt_spr = _make_sprite("button.png", _layout['lt'], self.batch, self.fg, False)
        self.lt_spr = _make_sprite("button.png", _layout['rt'], self.batch, self.fg, False)

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

        ####################################################
        #   User interface starts here:
        ####################################################
        self.triggerpoint = 0.8
        self.deadzone = 0.2
        self.frame = Frame(theme=Theme('theme/menutheme'), w=window.width, h=window.height)
        self.window.push_handlers(self.frame)

        @self.window.event
        def on_key_press(key, modifiers):
            if key == pyglet.window.key.SPACE:
                if config_window.parent is not None:
                    self.frame.remove(config_window)
                else:
                    self.frame.add(config_window)

        def update_trigger_point(slider):
            self.triggerpoint = slider.value
            deadzone_label = self.frame.get_element_by_name("triggerpoint")
            deadzone_label.text = "Analog Trigger Point: {}".format(round(slider.value, 2))

        def remap_buttons(button):
            # TTD add code here to remap buttons
            pass

        config_layout = VLayout(children=[
            Label("Analog Trigger Point: {}".format(round(self.triggerpoint, 2)), name="triggerpoint"),
            Slider(w=200, min=0.0, max=1.0, value=self.triggerpoint, action=update_trigger_point),
            Button("Remap Buttons", w=2, action=remap_buttons)
        ])
        config_window = Dialogue("Configuration", name="config_window", x=400, y=360, content=config_layout)

        ###################################################
        #   Window event to draw everything when necessary:
        ###################################################
        @self.window.event
        def on_draw():
            window_instance.clear()
            self.batch.draw()
            self.frame.draw()


if __name__ == "__main__":
    controllers = pyglet.input.get_game_controllers()

    # Load up either the full scene, or just the "try again" scene.
    if len(controllers) > 0:
        controller = controllers[0]
        scene = MainScene(window, controller)
    elif len(controllers) <= 0:
        scene = TryAgainScene(window)

    pyglet.clock.schedule_interval(lambda dt: None, 1/60.0)
    pyglet.app.run()
