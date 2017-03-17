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
stick_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=50, y=50, batch=batch, group=foreground)
pyglet.sprite.Sprite._visible = False       # Default to not-visible:
select_sprite = pyglet.sprite.Sprite(img=select_img, x=50, y=50, batch=batch, group=foreground)
start_sprite = pyglet.sprite.Sprite(img=start_img, x=50, y=50, batch=batch, group=foreground)
lp_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=50, y=50, batch=batch, group=foreground)
mp_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=50, y=50, batch=batch, group=foreground)
hp_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=50, y=50, batch=batch, group=foreground)
lb_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=50, y=50, batch=batch, group=foreground)
lk_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=50, y=50, batch=batch, group=foreground)
mk_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=50, y=50, batch=batch, group=foreground)
hk_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=50, y=50, batch=batch, group=foreground)
rb_sprite = pyglet.sprite.Sprite(img=redcircle_img, x=50, y=50, batch=batch, group=foreground)


@fightstick.event
def on_button_press(button):
    print("Pressed button:  {0}".format(0))
    lp_sprite.visible = True
    mp_sprite.visible = True
    hp_sprite.visible = True
    lb_sprite.visible = True
    lk_sprite.visible = True
    mk_sprite.visible = True
    hk_sprite.visible = True
    rb_sprite.visible = True
    select_sprite.visible = True
    start_sprite.visible = True


@fightstick.event
def on_button_release(button):
    print("Released button: {0}".format(0))
    lp_sprite.visible = False
    mp_sprite.visible = False
    hp_sprite.visible = False
    lb_sprite.visible = False
    lk_sprite.visible = False
    mk_sprite.visible = False
    hk_sprite.visible = False
    rb_sprite.visible = False
    select_sprite.visible = False
    start_sprite.visible = False


@window.event
def on_draw():
    window.clear()
    batch.draw()


if __name__ == "__main__":
    pyglet.app.run()
