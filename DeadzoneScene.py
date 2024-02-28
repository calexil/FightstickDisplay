# # Deadzone Interface, ?maybe TODO This doesn't work.
# class DeadzoneScene:
#     def __init__(self, window_instance):
#         self.window = window_instance
#         self.deadzone_img = pyglet.resource.image("deadzone.png")
#
#         @self.window.event
#         def on_button_press(controller, button):
#             assert _debug_print(f"Pressed Button: {button}")
#             pressed_button = button_mapping.get(button, None)
#             if pressed_button == 'guide':
#                 if config_window.parent is not None:
#                     self.frame.remove(config_window)
#                 else:
#                     self.frame.add(config_window)
#
#         def update_trigger_point(slider):
#             self.triggerpoint = slider.value
#             deadzone_label = self.frame.get_element_by_name("triggerpoint")
#             deadzone_label.text = "Analog Trigger Point: {}".format(round(slider.value, 2))
#
#         def on_draw():
#             self.window.clear()
#             self.deadzone_img.blit(0, 0)
