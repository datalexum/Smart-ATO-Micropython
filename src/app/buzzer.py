from machine import PWM, Pin
from utime import sleep

class Buzzer:
    def __init__(self, pin) -> None:
        self.buzzer = PWM(Pin(pin))
        self.buzzer.freq(500)
    
    def play_error_sound(self):
        self.buzzer.freq(500)
        for i in range(3):
            self.buzzer.duty_u16(1000)
            sleep(0.25)
            self.buzzer.duty_u16(0)
            sleep(0.25)
            self.buzzer.duty_u16(1000)
            sleep(1)
            self.buzzer.duty_u16(0)
            sleep(1)

    def play_empty_sound(self):
        self.buzzer.freq(500)
        for i in range(3):
            self.buzzer.duty_u16(1000)
            sleep(0.1)
            self.buzzer.duty_u16(0)
            sleep(0.1)
    
    def buzzer_off(self):
        self.buzzer.duty_u16(0)