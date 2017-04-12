import pyglet
from simplui import Theme, Frame, Dialogue, Slider, Button, Label, VLayout
import sys
import json
import io
# Some initial pyglet setup:
pyglet.resource.path.append("theme")
pyglet.resource.reindex()
window = pyglet.window.Window(width=640, height=391, caption="Fightstick Display", vsync=True)
window.set_icon(pyglet.resource.image("icon.png"))
batch = pyglet.graphics.Batch()

controllers = pyglet.input.get_game_controllers()
if len(controllers) > 0:
    fightstick = controllers[0]
    fightstick.open()
else:
    print("No FightStick detected. Please reconnect and try again!")
    sys.exit(1)

layout = {
    "background": (0, 0),
    "stick": (119, 155),
    "select": (0, 0),
    "start": (0, 0),
    "x": (257, 85),
    "y": (337, 115),
    "rt": (422, 114),
    "lt": (508, 111),
    "a": (276, 175),
    "b": (355, 205),
    "lb": (441, 204),
    "rb": (528, 201),
}

# Attempt to load in an alternate layout file for different themes:
try:
    default_layout = layout.copy()
    loaded_layout = json.load(pyglet.resource.file("layout.json"))
    for key in loaded_layout:
        default_layout[key] = loaded_layout[key]
    layout = default_layout.copy()
except:
    print("Invalid layout.json file. Falling back to default layout.")

# Load some images to be used by the program:
background_img = pyglet.resource.image("background.png")
stick_img = pyglet.resource.image("stick.png")
button_img = pyglet.resource.image("button.png")
select_img = pyglet.resource.image("select.png")
start_img = pyglet.resource.image("start.png")

# Ordered Groups to handle draw order of the sprites:
bg = pyglet.graphics.OrderedGroup(0)
fg = pyglet.graphics.OrderedGroup(1)

# Create all of the sprites for everything. Some are not visible by default:
pyglet.sprite.Sprite._visible = False
background_sprite = pyglet.sprite.Sprite(background_img, *layout['background'], batch=batch, group=bg)
stick_sprite = pyglet.sprite.Sprite(stick_img, *layout['stick'], batch=batch, group=fg)
select_sprite = pyglet.sprite.Sprite(select_img, *layout['select'], batch=batch, group=fg)
start_sprite = pyglet.sprite.Sprite(start_img, *layout['start'], batch=batch, group=fg)
x_sprite = pyglet.sprite.Sprite(button_img, *layout['x'], batch=batch, group=fg)
y_sprite = pyglet.sprite.Sprite(button_img, *layout['y'], batch=batch, group=fg)
rb_sprite = pyglet.sprite.Sprite(button_img, *layout['rb'], batch=batch, group=fg)
lb_sprite = pyglet.sprite.Sprite(button_img, *layout['lb'], batch=batch, group=fg)
a_sprite = pyglet.sprite.Sprite(button_img, *layout['a'], batch=batch, group=fg)
b_sprite = pyglet.sprite.Sprite(button_img, *layout['b'], batch=batch, group=fg)
rt_sprite = pyglet.sprite.Sprite(button_img, *layout['rt'], batch=batch, group=fg)
lt_sprite = pyglet.sprite.Sprite(button_img, *layout['lt'], batch=batch, group=fg)
background_sprite.visible = True
stick_sprite.visible = True


button_mapping = {
    "a": x_sprite,
    "b": y_sprite,
    "x": rb_sprite,
    "y": lb_sprite,
    "leftshoulder": a_sprite,
    "rightshoulder": b_sprite,
    None: rt_sprite,
    None: lt_sprite,
    "back": select_sprite,
    "start": start_sprite,
}


@fightstick.event
def on_button_press(controller, button):
    pressed_button = button_mapping.get(button)
    # XXX: avoid crash if the button is not mapped:
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
        center_x, center_y = layout['stick']
        center_x += (xvalue * 50)
        center_y += (yvalue * 50)
        stick_sprite.position = center_x, center_y
    elif stick == "rightstick":
        # TODO: confirm these are setting the right buttons:
        if xvalue > 0.8:
            rt_sprite.visible = True
        elif xvalue < -0.8:
            rt_sprite.visible = False
        if yvalue > 0.8:
            lt_sprite.visible = True
        elif yvalue < -0.8:
            lt_sprite.visible = False


@fightstick.event
def on_dpad_motion(controller, dpleft, dpright, dpup, dpdown):
    center_x, center_y = layout["stick"]
    if dpup:
        center_y += 50
    elif dpdown:
        center_y -= 50
    if dpleft:
        center_x -= 50
    elif dpright:
        center_x += 50
    stick_sprite.position = center_x, center_y


@fightstick.event
def on_trigger_motion(controller, trigger, value):
    # TODO: confirm these are setting the right buttons:
    if trigger == "lefttrigger":
        if value > 0.8:
            rt_sprite.visible = True
        elif value < -0.8:
            rt_sprite.visible = False
    if trigger == "righttrigger":
        if value > 0.8:
            lt_sprite.visible = True
        elif value < -0.8:
            lt_sprite.visible = False


####################################################
#   User interface starts here:
####################################################
frame = Frame(theme=Theme('theme/menutheme'), w=window.width, h=window.height)
window.push_handlers(frame)

# TODO: use this in trigger and stick events above ^^^
DEADZONE = 0.15


def toggle_menu(button):
    if options_window.parent is not None:
        frame.remove(options_window)
    else:
        frame.add(options_window)


def update_deadzone(slider):
    global DEADZONE
    DEADZONE = slider.value
    deadzone_label = frame.get_element_by_name("deadzone")
    deadzone_label.text = "Analog Deadzone: {}".format(round(slider.value, 2))


def remap_buttons(button):
    # in process TODO REMAP
    pass


config_layout = VLayout(children=[
    Label("Analog Deadzone: {}".format(round(DEADZONE, 2)), name="deadzone"),
    Slider(w=200, min=0.0, max=1.0, value=0.2, action=update_deadzone),
    Button("Remap Buttons", w=2, action=remap_buttons)
])
# Removing this until its more elegant, very ugly right now
# options_button = Button("Menu", name="options_button", x=565, y=370, action=toggle_menu)
#options_window = Dialogue("Options", name="options_window", x=300, y=360, content=config_layout)

# frame.add(options_button)


@window.event
def on_draw():
    window.clear()
    batch.draw()
    frame.draw()


if __name__ == "__main__":
    pyglet.clock.schedule_interval(lambda dt: None, 1/60.0)
    pyglet.app.run()
