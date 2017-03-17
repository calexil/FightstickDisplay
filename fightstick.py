import pyglet


pyglet.resource.path.append("images")
pyglet.resource.reindex()
window = pyglet.window.Window(width=640, height=390, style=pyglet.window.Window.WINDOW_STYLE_TOOL)
batch = pyglet.graphics.Batch()

# TODO: handle the situation where there are no fightsticks attached, instead of crashing
joysticks = pyglet.input.get_joysticks()
if len(joysticks) > 0:
    fightstick = joysticks[0]
else:
    fightstick = None

# Load some images to be used by the program:
base_img = pyglet.resource.image("fightstickblank.png")
redcircle_img = pyglet.resource.image("redcircle.png")
select_img = pyglet.resource.image("select.png")
start_img = pyglet.resource.image("start.png")

# Ordered Groups to handle draw order of the sprites:
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

# Create all of the sprites for everything. Some are not visible by default:
base_sprite = pyglet.sprite.Sprite(img=base_img, x=0, y=0, batch=batch, group=background)
stick_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=150, y=200, batch=batch, group=foreground)
pyglet.sprite.Sprite._visible = False       # Default to not-visible:
select_sprite = pyglet.sprite.Sprite(img=select_img, x=50, y=50, batch=batch, group=foreground)
start_sprite = pyglet.sprite.Sprite(img=start_img, x=50, y=150, batch=batch, group=foreground)
lp_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=50, y=50, batch=batch, group=foreground)
mp_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=150, y=50, batch=batch, group=foreground)
hp_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=200, y=50, batch=batch, group=foreground)
lb_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=250, y=50, batch=batch, group=foreground)
lk_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=300, y=50, batch=batch, group=foreground)
mk_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=350, y=50, batch=batch, group=foreground)
hk_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=400, y=50, batch=batch, group=foreground)
rb_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=450, y=50, batch=batch, group=foreground)


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
    center_x = 150
    center_y = 200
    if axis == 'x':
        center_x += value * 25
    elif axis == 'y':
        center_y += value * 25
    stick_sprite.position = center_x, center_y


@fightstick.event
def on_joyhat_motion(js, hat_x, hat_y):
    center_x = 150
    center_y = 200
    center_x += hat_x * 25
    center_y += hat_y * 25
    stick_sprite.position = center_x, center_y


@window.event
def on_draw():
    window.clear()
    batch.draw()


if __name__ == "__main__":
    pyglet.app.run()
