import usb_hid
from adafruit_hid.mouse import Mouse

class MouseManager:
    def __init__(self):
        self.sensitivity = 5
        self.enabled = False
        self.mouse = Mouse(usb_hid.devices)

    def MoveLeft(self):
        if self.enabled:
            self.mouse.move(x = self.sensitivity * -1)

    def MoveRight(self):
        if self.enabled:
            self.mouse.move(x = self.sensitivity)

    def MoveUp(self):
        if self.enabled:
            self.mouse.move(y = self.sensitivity)

    def MoveDown(self):
        if self.enabled:
            self.mouse.move(y = self.sensitivity * -1)

    def LeftClick(self):
        if self.enabled:
            self.mouse.press(Mouse.LEFT_BUTTON)

    def RightClick(self):
        if self.enabled:
            self.mouse.press(Mouse.RIGHT_BUTTON)
