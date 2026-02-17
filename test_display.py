import board
import digitalio
from adafruit_rgb_display import st7789
from PIL import Image, ImageDraw
import time

cs = digitalio.DigitalInOut(board.CE1)
dc = digitalio.DigitalInOut(board.D5)
rst = digitalio.DigitalInOut(board.D6)

spi = board.SPI()

display = st7789.ST7789(
    spi,
    cs=cs,
    dc=dc,
    rst=rst,
    width=240,
    height=320,
    x_offset=0,
    y_offset=0,
    baudrate=40000000,
)

def fill(color):
    img = Image.new("RGB", (240, 320), color)
    display.image(img)

print("RED")
fill((255,0,0))
time.sleep(1)

print("GREEN")
fill((0,255,0))
time.sleep(1)

print("BLUE")
fill((0,0,255))
time.sleep(1)

print("WHITE")
fill((255,255,255))
time.sleep(1)

img = Image.new("RGB", (240,240), "black")
draw = ImageDraw.Draw(img)
draw.text((20,110), "DISPLAY OK", fill="white")
display.image(img)

print("DONE")
time.sleep(5)
