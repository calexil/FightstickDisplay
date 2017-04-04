import pyglet
import sys
import json


pyglet.resource.path.append("theme")
pyglet.resource.reindex()
window = pyglet.window.Window(width=640, height=391, vsync=True)
window.set_icon(pyglet.resource.image("icon.png"))
batch = pyglet.graphics.Batch()

controllers = pyglet.input.get_game_controllers()
if len(controllers) > 0:
    fightstick = controllers[0]
    fightstick.open()
else:
    print("No FightStick detected. Please attach and try again!")
    sys.exit(1)

layout = {
    "background": (0, 0),
    "stick": (118, 155),
    "select": (0, 0),
    "start": (0, 0),
    "lp": (257, 85),
    "mp": (337, 115),
    "hp": (422, 114),
    "lb": (508, 111),
    "lk": (276, 175),
    "mk": (355, 205),
    "hk": (441, 204),
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
lp_sprite = pyglet.sprite.Sprite(button_img, *layout['lp'], batch=batch, group=fg)
mp_sprite = pyglet.sprite.Sprite(button_img, *layout['mp'], batch=batch, group=fg)
hp_sprite = pyglet.sprite.Sprite(button_img, *layout['hp'], batch=batch, group=fg)
lb_sprite = pyglet.sprite.Sprite(button_img, *layout['lb'], batch=batch, group=fg)
lk_sprite = pyglet.sprite.Sprite(button_img, *layout['lk'], batch=batch, group=fg)
mk_sprite = pyglet.sprite.Sprite(button_img, *layout['mk'], batch=batch, group=fg)
hk_sprite = pyglet.sprite.Sprite(button_img, *layout['hk'], batch=batch, group=fg)
rb_sprite = pyglet.sprite.Sprite(button_img, *layout['rb'], batch=batch, group=fg)
background_sprite.visible = True
stick_sprite.visible = True


button_mapping = {
    "a": lp_sprite,
    "b": mp_sprite,
    "x": hp_sprite,
    "y": lb_sprite,
    "leftshoulder": lk_sprite,
    "rightshoulder": mk_sprite,
    None: hk_sprite,
    None: rb_sprite,
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
            hk_sprite.visible = True
        elif xvalue < -0.8:
            hk_sprite.visible = False
        if yvalue > 0.8:
            rb_sprite.visible = True
        elif yvalue < -0.8:
            rb_sprite.visible = False


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
            hk_sprite.visible = True
        elif value < -0.8:
            hk_sprite.visible = False
    if trigger == "righttrigger":
        if value > 0.8:
            rb_sprite.visible = True
        elif value < -0.8:
            rb_sprite.visible = False


@window.event
def on_draw():
    window.clear()
    batch.draw()


if __name__ == "__main__":
    pyglet.clock.schedule_interval(lambda dt: None, 1/30.0)
    pyglet.app.run()
