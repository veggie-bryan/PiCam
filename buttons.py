from gpiozero import Button
from signal import pause

#GPIO Names
Capture_Pin = 17
Menu_Pin = 25
Left_Pin = 23
Right_Pin = 24
Up_Pin = 27
Down_Pin = 22

class CameraButtons:
    def __init__(self):
        self.capture = Button(Capture_Pin, pull_up=True, bounce_time=0.05)
        self.menu = Button(Menu_Pin, pull_up=True, bounce_time=0.05)
        self.left = Button(Left_Pin, pull_up=True, bounce_time=0.05)
        self.right = Button(Right_Pin, pull_up=True, bounce_time=0.05)
        self.up = Button(Up_Pin, pull_up=True, bounce_time=0.05)
        self.down = Button(Down_Pin, pull_up=True, bounce_time=0.05)

    def bind(self, on_capture, on_menu, on_left, on_right, on_up, on_down):
        self.capture.when_pressed = on_capture
        self.menu.when_pressed = on_menu
        self.left.when_pressed = on_left
        self.right.when_pressed = on_right
        self.up.when_pressed = on_up
        self.down.when_pressed = on_down

