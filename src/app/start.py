from app.libs.ota_updater import OTAUpdater
from secrets_config import WIFI_PASSWORD, WIFI_SSID
from machine import Pin, PWM, Signal, I2C, reset
from utime import sleep
from app.libs.ssd1306 import SSD1306_I2C


def boot():
    pass


def main():
    o = OTAUpdater(
        "https://github.com/datalexum/Smart-ATO-Micropython",
        main_dir="app",
        github_src_dir="src/app",
    )
    OTAUpdater._using_network(WIFI_SSID, WIFI_PASSWORD)
    update_available = o.check_for_update_to_install_during_next_reboot()

    buzzer = PWM(Pin(10))
    buzzer.freq(500)

    if update_available:
        buzzer.duty_u16(1000)
        sleep(3)
        buzzer.duty_u16(0)
        reset()

    print("Now in version 0.0.6")

    i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=40000)
    oled = SSD1306_I2C(128, 32, i2c)
    oled.fill(0)
    # Abstand Oben 8, Abstand links 10, Max. zwei Reihen a 15 Zeichen
    oled.text("World:", 10, 8)
    oled.show()
    oled.text("Hello - {}".format(o.get_version('app')), 10, 18)
    oled.show()

    # Empty
    for i in range(3):
        buzzer.duty_u16(1000)
        sleep(0.1)
        buzzer.duty_u16(0)
        sleep(0.1)

    # Error
    for i in range(3):
        buzzer.duty_u16(1000)
        sleep(0.25)
        buzzer.duty_u16(0)
        sleep(0.25)
        buzzer.duty_u16(1000)
        sleep(1)
        buzzer.duty_u16(0)
        sleep(1)

    buzzer.duty_u16(0)

    # Initialisierung von GPIO14 als Ausgang
    device = Signal(21, Pin.OUT, invert=True)

    # LED einschalten
    print("EIN")
    device.on()

    # 3 Sekunden warten
    switch1 = Pin(18, Pin.IN, Pin.PULL_DOWN)
    switch2 = Pin(19, Pin.IN, Pin.PULL_DOWN)
    switch3 = Pin(20, Pin.IN, Pin.PULL_DOWN)
    for i in range(120):
        oled.fill(0)
        st = "{}: {},{},{}".format(i, switch1.value(), switch2.value(), switch3.value())
        oled.text(st, 10, 8)
        oled.show()
        sleep(1)

    # LED ausschalten
    print("AUS")
    device.off()
