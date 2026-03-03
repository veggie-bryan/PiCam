import board
import digitalio
from adafruit_rgb_display import st7789
from PIL import Image
import time

# -----------------------------
# DISPLAY SETUP (KNOWN GOOD)
# -----------------------------
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

DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 320

# -----------------------------
# IMAGE PATH (CHANGE AS NEEDED)
# -----------------------------
path = "/home/bryan/photos/20260122_181941_503.jpg"

print("Opening image...")
img = Image.open(path).convert("RGB")

print("Original size:", img.size)

# Rotate 90 degrees (try 90 or 270 if direction is wrong)
img = img.rotate(270, expand=True)

print("After rotation:", img.size)

img.thumbnail((DISPLAY_WIDTH, DISPLAY_HEIGHT), Image.BILINEAR)

print("Scaled size:", img.size)

background = Image.new("RGB", (DISPLAY_WIDTH, DISPLAY_HEIGHT), (0, 0, 0))

x = (DISPLAY_WIDTH - img.width) // 2
y = (DISPLAY_HEIGHT - img.height) // 2

background.paste(img, (x, y))

display.image(background)

time.sleep(10)