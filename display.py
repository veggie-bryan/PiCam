import board
import digitalio
from adafruit_rgb_display import st7789
from PIL import Image, ImageDraw


class CameraDisplay:
    def __init__(self):
        self.cs = digitalio.DigitalInOut(board.CE1)
        self.dc = digitalio.DigitalInOut(board.D5)
        self.rst = digitalio.DigitalInOut(board.D6)
        self.spi = board.SPI()

        self.width = 240
        self.height = 320

        self.display = st7789.ST7789(
            self.spi,
            cs=self.cs,
            dc=self.dc,
            rst=self.rst,
            width=self.width,
            height=self.height,
            x_offset=0,
            y_offset=0,
            baudrate=40000000,
        )

    def clear(self):
        img = Image.new("RGB", (self.width, self.height), "black")
        self.display.image(img)

    def show_text(self, text):
        img = Image.new("RGB", (self.width, self.height), "black")
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), text, fill="white")
        self.display.image(img)

    def show_image(self, image_path):
        img = Image.open(image_path).convert("RGB")
        img = img.resize((self.width, self.height))
        self.display.image(img)
