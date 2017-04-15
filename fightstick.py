import pyglet
from simplui import Theme, Frame, Dialogue, Slider, Button, Label, VLayout
import sys
import json

pyglet.resource.path.append("theme")
pyglet.resource.reindex()
window = pyglet.window.Window(width=640, height=391, caption="Fightstick Display", vsync=True)
window.set_icon(pyglet.resource.image("icon.png"))
batch = pyglet.graphics.Batch()
controllers = pyglet.input.get_game_controllers()
e = ("Invalid layout.json file. Falling back to default layout.")

# Load some images to be used by the program:
background_img = pyglet.resource.image("background.png")
missing_img = pyglet.resource.image("missing.png")
stick_img = pyglet.resource.image("stick.png")
button_img = pyglet.resource.image("button.png")
select_img = pyglet.resource.image("select.png")
start_img = pyglet.resource.image("start.png")

# Runthe controller check
if len(controllers) > 0:
    fightstick = controllers[0]
    fightstick.open()
elif len(controllers) <= 0:
    print("No FightStick detected. Please reconnect and try again!")
    sys.exit(1)

layout = {
    "background": (0, 0),
    "stick": (119, 155),
    "select": (0, 0),
    "start": (0, 0),
    "x": (256, 84),
    "y": (336, 114),
    "rt": (421, 113),
    "lt": (507, 110),
    "a": (275, 174),
    "b": (354, 204),
    "lb": (440, 203),
    "rb": (527, 200),
}

# Attempt to load in an alternate layout file for different themes:
def layout_default():
    try:
        default_layout = layout.copy()
        loaded_layout = json.load(pyglet.resource.file("layout.json"))
        for key in loaded_layout:
            default_layout[key] = loaded_layout[key]
        layout = default_layout.copy()
    except Exception as e:
        print(e)

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
    "righttrigger": rt_sprite,
    "lefttrigger": lt_sprite,
    "back": select_sprite,
    "start": start_sprite,
}

@fightstick.event
def on_button_press(controller, button):
    pressed_button = button_mapping.get(button)
# avoid crash if the button is not mapped:
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
# TTD confirm these are setting the right buttons:
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
# TTD confirm these are setting the right buttons:
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

# TTD: use this in trigger and stick events above ^^^
class triggerpoint:
    def __init__(self, triggerpoint):
        self.triggerpoint = triggerpoint

triggerpoint = 0.8

@window.event
def on_key_press(key, modifiers):
# Toggle the menu when pressing the space key.
    if key == pyglet.window.key.SPACE:
        if config_window.parent is not None:
            frame.remove(config_window)
        else:
            frame.add(config_window)

def update_trigger_point(slider):
    triggerpoint = slider.value
    deadzone_label = frame.get_element_by_name("triggerpoint")
    deadzone_label.text = "Analog Trigger Point: {}".format(round(slider.value, 2))
    print(triggerpoint)
def remap_buttons(button):
# TTD add code here to remap buttons
    pass

config_layout = VLayout(children=[
    Label("Analog Trigger Point: {}".format(round(triggerpoint, 2)), name="triggerpoint"),
    Slider(w=200, min=0.0, max=1.0, value=triggerpoint, action=update_trigger_point),
    Button("Remap Buttons", w=2, action=remap_buttons)
])
config_window = Dialogue("Configuration", name="config_window", x=400, y=360, content=config_layout)

@window.event
def on_draw():
    window.clear()
    batch.draw()
    frame.draw()

if __name__ == "__main__":
    pyglet.clock.schedule_interval(lambda dt: None, 1/60.0)
    pyglet.app.run()
