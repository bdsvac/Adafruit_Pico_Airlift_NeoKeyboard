import board
import busio
import displayio
import time
from ButtonManager import ButtonManager
from DisplayManager import DisplayManager
from LightManager import LightManager
from MouseManager import MouseManager
from WiFiManager import WiFiManager

displayio.release_displays()
spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
bm = ButtonManager()
lm = LightManager()
mm = MouseManager()
mm.enabled = False
wm = WiFiManager(spi)
dm = DisplayManager(spi)
dm.ShowImage()
print("init done")

while True:
    if bm.LeftButtonClicked():
        lm.Run((0, 0, 255))
        lm.enabled = True

        dm.ShowImage()

    if bm.RightButtonClicked():
        lm.Run((0, 255, 0))
        #lm.enabled = False
    if bm.Button1Clicked():
        mm.LeftClick()
        lm.Run((255, 255, 255))
    if bm.Button2Clicked():
        mm.MoveUp()
        lm.Run((255, 100, 0))
    if bm.Button3Clicked():
        mm.RightClick()
        lm.Run((255, 0, 0))

        t1 = wm.GetOutsideTemp()
        dm.Clear()
        dm.AppendText("Outside Temp", x = 5, y = 10)
        dm.AppendText(t1, x = 10, y = 30)
        #dm.ShowText(wm.GetOutsideTemp())

    if bm.Button4Clicked():
        mm.MoveLeft()

        wm.SendSlackMessage("SHOW and TELL! :tada:")

        lm.Run((255, 0, 255))
    if bm.Button5Clicked():
        mm.MoveDown()
        lm.Run((255, 255, 0))
    if bm.Button6Clicked():
        mm.MoveRight()
        lm.Run((0, 255, 255))

        t1, t2, t3 = wm.GetInsideTemps()
        if not t1 is None:
            dm.Clear()
            dm.AppendText("Upstairs", x = 5, y = 10)
            dm.AppendText(t1 + " F", x = 10, y = 30)

            dm.AppendText("Downstairs", x = 5, y = 50)
            dm.AppendText(t2 + " F", x = 10, y = 70)

            dm.AppendText("Basement", x = 5, y = 90)
            dm.AppendText(t3 + " F", x = 10, y = 110)


    time.sleep(0.001)