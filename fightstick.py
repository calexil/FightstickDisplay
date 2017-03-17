import pyglet


pyglet.resource.path.append("images")
pyglet.resource.reindex()
window = pyglet.window.Window(width=640, height=390, vsync=False)
batch = pyglet.graphics.Batch()

# TODO: handle the situation where there are no fightsticks attached, instead of crashing
joysticks = pyglet.input.get_joysticks()
if len(joysticks) > 0:
    fightstick = joysticks[0]
    fightstick.open()
else:
    fightstick = None

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
lp_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=258, y=80, batch=batch, group=foreground)
mp_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=350, y=80, batch=batch, group=foreground)
hp_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=450, y=80, batch=batch, group=foreground)
lb_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=550, y=80, batch=batch, group=foreground)
lk_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=250, y=200, batch=batch, group=foreground)
mk_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=350, y=200, batch=batch, group=foreground)
hk_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=450, y=200, batch=batch, group=foreground)
rb_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=550, y=200, batch=batch, group=foreground)
background_sprite.visible = True
stick_sprite.visible = True


@fightstick.event
def on_joybutton_press(js, button):
    if button == 0:
        lp_sprite.visible = True
    if button == 1:
        mp_sprite.visible = True
    if button == 2:
        hp_sprite.visible = True
    if button == 3:
        lb_sprite.visible = True
    if button == 4:
        lk_sprite.visible = True
    if button == 5:
        mk_sprite.visible = True
    if button == 6:
        hk_sprite.visible = True
    if button == 7:
        rb_sprite.visible = True
    if button == 8:
        select_sprite.visible = True
    if button == 9:
        start_sprite.visible = True


@fightstick.event
def on_joybutton_release(js, button):
    if button == 0:
        lp_sprite.visible = False
    if button == 1:
        mp_sprite.visible = False
    if button == 2:
        hp_sprite.visible = False
    if button == 3:
        lb_sprite.visible = False
    if button == 4:
        lk_sprite.visible = False
    if button == 5:
        mk_sprite.visible = False
    if button == 6:
        hk_sprite.visible = False
    if button == 7:
        rb_sprite.visible = False
    if button == 8:
        select_sprite.visible = False
    if button == 9:
        start_sprite.visible = False


@fightstick.event
def on_joyaxis_motion(js, axis, value):
    if axis == 'x':
        x = 118 + (value * 50)
        stick_sprite.x = x
    elif axis == 'y':
        y = 155 + -(value * 50)
        stick_sprite.y = y


# TODO: test this on a joystick that uses the hat instead of x/y axis:
@fightstick.event
def on_joyhat_motion(js, hat_x, hat_y):
    center_x = 118
    center_y = 155
    x = center_x + (hat_x * 50)
    y = center_y + (hat_y * 50)
    stick_sprite.position = x, y


@window.event
def on_draw():
    window.clear()
    batch.draw()


if __name__ == "__main__":
    pyglet.clock.schedule_interval(lambda dt: None, 1/30.0)
    pyglet.app.run()
