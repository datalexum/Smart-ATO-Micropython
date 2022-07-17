from app.libs.ota_updater import OTAUpdater
from secrets_config import WIFI_PASSWORD, WIFI_SSID
from machine import Pin, PWM, Signal, I2C, reset
from utime import sleep
from app.libs.ssd1306 import SSD1306_I2C
from app.state_machine import StateMachine


def boot():
    pass


def main():
    i2c = I2C(1, sda=Pin(16), scl=Pin(17), freq=40000)
    oled = SSD1306_I2C(128, 32, i2c)
    
    o = OTAUpdater(
        "https://github.com/datalexum/Smart-ATO-Micropython",
        main_dir="app",
        github_src_dir="src/app",
    )

    oled.text("Welcome from", 10, 8)
    oled.text("version {}".format(o.get_version('app')), 10, 18)
    oled.show()

    oled.fill(0)
    oled.text("Checking for", 10, 8)
    oled.text("update...", 10, 18)
    oled.show()
    
    OTAUpdater._using_network(WIFI_SSID, WIFI_PASSWORD)
    update_available = o.check_for_update_to_install_during_next_reboot()

    if update_available:
        buzzer = PWM(Pin(10))
        buzzer.freq(500)
        oled.fill(0)
        oled.text("Update found!", 10, 8)
        oled.text("Restarting...", 10, 18)
        oled.show()
        buzzer.duty_u16(1000)
        sleep(3)
        buzzer.duty_u16(0)
        reset()
    else:
        oled.fill(0)
        oled.text("No update found", 10, 8)
        oled.show()
        sleep(3)

    sm = StateMachine(fs1_pin=18, fs2_pin=19, fs3_pin=23, pump_pin=21, buzzer_pin=4, lcd=oled)
    sm.start()

