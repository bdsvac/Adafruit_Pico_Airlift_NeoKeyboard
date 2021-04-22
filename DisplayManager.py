import adafruit_imageload
import board
import busio
import displayio
import gc
import terminalio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_st7735r import ST7735R
from digitalio import DigitalInOut, Direction, Pull

class DisplayManager:
    def __init__(self, spi):
        self.display_width = 128
        self.display_height = 128
        self.font = bitmap_font.load_font("/assets/Helvetica-Bold-16.bdf")
        tft_cs = board.GP8
        tft_dc = board.GP5
        tft_res = board.GP6
        display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_res)
        self.display = ST7735R(display_bus, width=self.display_width, height=self.display_height, colstart=1, rowstart=1, rotation=0)
        self.splash = displayio.Group(max_size=10)
        self.display.show(self.splash)

    def Clear(self):
        self.splash = displayio.Group(max_size=10)
        self.display.show(self.splash)

    def AppendText(self, text, x = 0, y = 0):
        color = 0x00FF00
        text_area = label.Label(self.font, text=text, color=color)
        text_area.x = x
        text_area.y = y
        self.splash.append(text_area)
        self.display.show(self.splash)

    def ShowText(self, text, x = 0, y = 0):
        color = 0x00FF00
        text_area = label.Label(self.font, text=text, color=color)
        text_area.x = x
        text_area.y = y
        self.display.show(text_area)

    def ShowImage(self):
        bitmap, palette = adafruit_imageload.load("/assets/key.bmp",
            bitmap=displayio.Bitmap, palette=displayio.Palette)
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
        group = displayio.Group()
        group.append(tile_grid)
        self.display.show(group)
