import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_requests as requests
import board
import gc
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError
from digitalio import DigitalInOut
from secrets import secrets

class WiFiManager:
    def __init__(self, spi):
        esp32_cs = DigitalInOut(board.GP13)
        esp32_busy = DigitalInOut(board.GP14)
        esp32_reset = DigitalInOut(board.GP15)
        self.esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_busy, esp32_reset)
        socket.set_interface(self.esp)
        requests.set_socket(socket, self.esp)

        #if self.esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
        #    print("ESP32 found and in idle mode")
        #    print("Firmware vers.", self.esp.firmware_version)
        #    print("MAC addr:", [hex(i) for i in self.esp.MAC_address])

        #for ap in self.esp.scan_networks():
        #    print("\t%s\t\tRSSI: %d" % (str(ap['ssid'], 'utf-8'), ap['rssi']))


    def EnsureConnection(self):
        while not self.esp.is_connected:
            try:
                self.esp.connect_AP(secrets["ssid"], secrets["password"])
            except RuntimeError as e:
                print("could not connect to AP, retrying: ", e)
                continue

    def GetOutsideTemp(self):
        self.EnsureConnection()

        JSON_URL = "http://api.openweathermap.org/data/2.5/weather?q=" + secrets["openweather_location"] + "&appid=" + secrets["openweather_token"] + "&units=metric"

        print("Fetching weather data")
        r = requests.get(JSON_URL)
        print(r.status_code)
        print("-" * 40)
        #text_area1.text = r.json()['main']['temp_max']
        print("The current temperature is",r.json()['main']['temp_max'],"C")
        c = float(r.json()['main']['temp_max'])
        f = (c * 9/5) + 32
        fStr = str(round(f))
        print("-" * 40)
        r.close()
        r = None
        gc.collect()
        return fStr + " F"

    def SendSlackMessage(self, message):
        self.EnsureConnection()

        data = {
          "channel": secrets["slack_channel_id"],
          "text": message + " (sent from IOT Device)"
        }

        headers = {
            "Authorization": "Bearer " + secrets["slack_user_token"],
            "Accept": "application/json",
        }

        url = "https://slack.com/api/chat.postMessage"
        resp = requests.post(url, headers=headers, data=data)
        if (not resp is None):
            print("HEADERS:")
            print(resp.headers)
            print("TEXT:")
            print(resp.text)
            print("END TEXT")
            resp.close()
            resp = None
            gc.collect()

    def GetInsideTemps(self):
        self.EnsureConnection()
        io = IO_HTTP(secrets["aio_username"], secrets["aio_key"], requests)

        aio_feed0_name = "upstairs"
        aio_feed1_name = "downstairs"
        aio_feed2_name = "basement"

        feed0 = None
        feed1 = None
        feed2 = None

        if (feed0 is None):
            try:
                feed0 = io.get_feed(aio_feed0_name)
            except:
                print("Can't get " + aio_feed0_name + " feed.")
        if (feed1 is None):
            try:
                feed1 = io.get_feed(aio_feed1_name)
            except:
                print("Can't get " + aio_feed1_name + " feed.")
        if (feed2 is None):
            try:
                feed2 = io.get_feed(aio_feed2_name)
            except:
                print("Can't get " + aio_feed2_name + " feed.")

        try:
            t0 = io.receive_data(feed0["key"])
            t1 = io.receive_data(feed1["key"])
            t2 = io.receive_data(feed2["key"])

            feed0 = None
            feed1 = None
            feed2 = None
            io = None
            gc.collect()

            return t0["value"], t1["value"], t2["value"]
        except:
            return None, None, None