import pyglet
import os, sys, time

pyglet.resource.path.append("images")
pyglet.resource.reindex()
window = pyglet.window.Window(width=640, height=391, vsync=True)
batch = pyglet.graphics.Batch()

controllers = pyglet.input.get_game_controllers()
if len(controllers) > 0:
    fightstick = controllers[0]
    fightstick.open()
else:
    print("No FightStick detected. Please attach and try again!")
    sys.exit(1)

# Load some images to be used by the program:
background_img = pyglet.resource.image("fightstickblank.png")
redcircle_img = pyglet.resource.image("redcircle.png")
select_img = pyglet.resource.image("select.png")
start_img = pyglet.resource.image("start.png")

# Ordered Groups to handle draw order of the sprites:
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

# Create all of the sprites for everything. Some are not visible by default:
pyglet.sprite.Sprite._visible = False
background_sprite = pyglet.sprite.Sprite(img=background_img, x=0, y=0, batch=batch, group=background)
stick_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=118, y=155, batch=batch, group=foreground)
select_sprite = pyglet.sprite.Sprite(img=select_img, x=0, y=0, batch=batch, group=foreground)
start_sprite = pyglet.sprite.Sprite(img=start_img, x=0, y=0, batch=batch, group=foreground)
lp_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=257, y=85, batch=batch, group=foreground)
mp_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=337, y=115, batch=batch, group=foreground)
hp_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=422, y=114, batch=batch, group=foreground)
lb_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=508, y=111, batch=batch, group=foreground)
lk_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=276, y=175, batch=batch, group=foreground)
mk_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=355, y=205, batch=batch, group=foreground)
hk_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=441, y=204, batch=batch, group=foreground)
rb_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=528, y=201, batch=batch, group=foreground)
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
def on_stick_motion(controller, axis, xvalue, yvalue):
    center_x = 118
    center_y = 155
    center_x += (xvalue * 50)
    center_y += (yvalue * 50)
    stick_sprite.position = center_x, center_y


@fightstick.event
def on_dpad_motion(controller, dpleft, dpright, dpup, dpdown):
    center_x = 118
    center_y = 155
    if dpup:
        center_y += 50
    elif dpdown:
        center_y -= 50
    if dpleft:
        center_x -= 50
    elif dpright:
        center_x += 50
    stick_sprite.position = center_x, center_y


@window.event
def on_draw():
    window.clear()
    batch.draw()


if __name__ == "__main__":
    pyglet.clock.schedule_interval(lambda dt: None, 1/30.0)
    pyglet.app.run()
