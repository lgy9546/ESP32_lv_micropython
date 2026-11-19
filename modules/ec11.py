# ec11.py
import lvgl as lv
from machine import Pin
import time

class EC11:
    def __init__(self, pin_a, pin_b, pin_sw=None):
        self.a = Pin(pin_a, Pin.IN, Pin.PULL_UP)
        self.b = Pin(pin_b, Pin.IN, Pin.PULL_UP)
        self.sw = Pin(pin_sw, Pin.IN, Pin.PULL_UP) if pin_sw else None
        self.last = (self.a(), self.b())
        self.diff = 0

    def read_cb(self, indev, data):
        a, b = self.a(), self.b()
        if (a, b) != self.last:
            if self.last == (1,0):
                self.diff += 1
            elif self.last == (0,1):
                self.diff -= 1
            self.last = (a,b)
        data.enc_diff = self.diff
        data.state = 0 if (self.sw and self.sw()) else 1
        self.diff = 0
        return False
