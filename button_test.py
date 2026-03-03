from gpiozero import Button
from signal import pause

btn = Button(17, pull_up=True)
btn.when_pressed = lambda: print("CAPTURE PRESSED")
pause()