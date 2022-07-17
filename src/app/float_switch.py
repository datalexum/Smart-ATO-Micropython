from machine import Pin

class FloatSwitch:
    def __init__(self, pin) -> None:
        self.pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        self.state = self.pin.value
    
    def is_opened(self):
        return not bool(self.state())
    
    def is_closed(self):
        return bool(self.state())
