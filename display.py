import board
import digitalio
from adafruit_rgb_display import st7789
from PIL import Image, ImageDraw, ImageFont

class CameraDisplay:
    def __init__(self):
        # SPI setup
        cs = digitalio.DigitalInOut(board.CE1)
        dc = digitalio.DigitalInOut(board.D5)
        rst = digitalio.DigitalInOut(board.D6)

        spi = board.SPI()

        self.display = st7789.ST7789(
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

        self.width = 240
        self.height = 320

    # -----------------------------
    # Clear Screen
    # -----------------------------
    def clear(self):
        img = Image.new("RGB", (self.width, self.height), (0, 0, 0))
        self.display.image(img)

    # -----------------------------
    # Show Text (for debugging/UI)
    # -----------------------------
    def show_text(self, text):
        img = Image.new("RGB", (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        draw.text((20, self.height // 2), text, fill=(255, 255, 255))

        self.display.image(img)

    # -----------------------------
    # Show Image (FINAL VERSION)
    # -----------------------------
    def show_image(self, path):
        img = Image.open(path).convert("RGB")

        # Rotate for portrait-mounted display
        img = img.rotate(270, expand=True)

        # Preserve aspect ratio
        img.thumbnail((self.width, self.height), Image.BILINEAR)

        # Letterbox background
        background = Image.new("RGB", (self.width, self.height), (0, 0, 0))

        x = (self.width - img.width) // 2
        y = (self.height - img.height) // 2

        background.paste(img, (x, y))

        self.display.image(background)
