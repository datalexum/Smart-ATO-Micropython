from utime import sleep
from app import float_switch
from app import buzzer
from machine import Signal, Pin, Timer
from app.libs.ssd1306 import SSD1306_I2C
import _thread

class StateMachine:
    def __init__(self, fs1_pin, fs2_pin, fs3_pin, pump_pin, buzzer_pin, lcd: SSD1306_I2C) -> None:
        self.state = 'FULL'
        self.fs1 = float_switch.FloatSwitch(fs1_pin)
        self.fs2 = float_switch.FloatSwitch(fs2_pin)
        self.fs3 = float_switch.FloatSwitch(fs3_pin)
        self.pump = Signal(pump_pin, Pin.OUT, invert=True)
        self.buzzer = buzzer.Buzzer(buzzer_pin)
        self.error_timer = {'timer': Timer(0), 'status': False}
        self.empty_timer = {'timer': Timer(1), 'status': False}
        self.lcd = lcd
        self.thread_run = False
        _thread.start_new_thread(self.run_forever, ())
    
    def callback_error(self):
        self.buzzer.play_error_sound()
        self.error_timer['timer'].init(mode=Timer.ONE_SHOT, period=600000, callback=self.callback_error)
        self.error_timer['status'] = True

    def callback_empty(self):
        self.buzzer.play_empty_sound()
        self.empty_timer['timer'].init(mode=Timer.ONE_SHOT, period=600000, callback=self.callback_empty)
        self.empty_timer['status'] = True
    
    def start(self):
        self.thread_run = True
    
    def stop(self):
        self.thread_run = False


    def get_state(self):
        return self.state
    
    def run_forever(self):
        while True:
            if self.thread_run:
                self.set_state()
            sleep(1)

    def set_state(self):
        self.buzzer.buzzer_off()
        if self.state == 'FULL':
            self.pump.off()
            self.lcd.fill(0)
            self.lcd.text("Ready", 10, 13)
            self.lcd.show()
            if self.fs1.is_opened() and self.fs2.is_opened():
                self.state = 'ERROR'
            elif self.fs3.is_opened():
                self.state = 'EMPTY'
            elif self.fs1.is_opened() and self.fs2.is_closed():
                self.state = 'DOSING'
        if self.state == 'DOSING':
            self.pump.on()
            self.lcd.fill(0)
            self.lcd.text("Dosing", 10, 13)
            self.lcd.show()
            if self.fs1.is_opened() and self.fs2.is_opened():
                self.state = 'ERROR'
            elif self.fs3.is_opened():
                self.state = 'EMPTY'
            elif self.fs1.is_closed():
                self.state = 'FULL'
        if self.state == 'EMPTY':
            self.pump.off()
            self.lcd.fill(0)
            self.lcd.text("Empty", 10, 13)
            self.lcd.show()
            if not self.empty_timer['status']:
                self.buzzer.play_empty_sound()
                self.empty_timer['timer'].init(mode=Timer.ONE_SHOT, period=600000, callback=self.callback_empty)
                self.empty_timer['status'] = True
            
            if self.fs1.is_opened() and self.fs2.is_opened():
                self.empty_timer['timer'].deinit()
                self.empty_timer['status'] = False
                self.state = 'ERROR'
            elif self.fs3.is_closed():
                self.empty_timer['timer'].deinit()
                self.empty_timer['status'] = False
                self.state = 'FULL'
        if self.state == 'ERROR':
            self.pump.off()
            if not self.error_timer['status']:
                self.lcd.fill(0)
                self.lcd.text("ERROR", 10, 13)
                self.lcd.show()
                self.buzzer.play_empty_sound()
                self.error_timer['timer'].init(mode=Timer.ONE_SHOT, period=600000, callback=self.callback_error)
                self.error_timer['status'] = True
