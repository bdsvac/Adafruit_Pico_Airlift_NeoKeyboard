import board
from digitalio import DigitalInOut, Direction, Pull

class ButtonManager:
    def __init__(self):
        self.enabled = True
        self.LeftButton = self.InitButton(board.GP27)
        self.RightButton = self.InitButton(board.GP26)
        self.Button1 = self.InitButton(board.GP21)
        self.Button2 = self.InitButton(board.GP20)
        self.Button3 = self.InitButton(board.GP19)
        self.Button4 = self.InitButton(board.GP18)
        self.Button5 = self.InitButton(board.GP17)
        self.Button6 = self.InitButton(board.GP16)

    def InitButton(self, pin):
        btn = DigitalInOut(pin)
        btn.direction = Direction.INPUT
        btn.pull = Pull.UP
        return btn

    def Clicked(self, btn, waitForRelease = False):
        if not btn.value:
            if waitForRelease:
                while not btn.value:
                    pass
            return True
        return False;

    def LeftButtonClicked(self, waitForRelease = False):
        return self.Clicked(self.LeftButton, waitForRelease)

    def RightButtonClicked(self, waitForRelease = False):
        return self.Clicked(self.RightButton, waitForRelease)

    def Button1Clicked(self, waitForRelease = False):
        return self.Clicked(self.Button1, waitForRelease)

    def Button2Clicked(self, waitForRelease = False):
        return self.Clicked(self.Button2, waitForRelease)

    def Button3Clicked(self, waitForRelease = False):
        return self.Clicked(self.Button3, waitForRelease)

    def Button4Clicked(self, waitForRelease = False):
        return self.Clicked(self.Button4, waitForRelease)

    def Button5Clicked(self, waitForRelease = False):
        return self.Clicked(self.Button5, waitForRelease)

    def Button6Clicked(self, waitForRelease = False):
        return self.Clicked(self.Button6, waitForRelease)
