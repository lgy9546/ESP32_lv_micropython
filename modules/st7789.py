# st7789.py
import lvgl as lv
from machine import SPI, Pin

class ST7789:
    def __init__(self, spi, cs, dc, rst, width=240, height=320, rot=0):
        self.spi = spi
        self.cs = Pin(cs, Pin.OUT, value=1)
        self.dc = Pin(dc, Pin.OUT, value=1)
        self.rst = Pin(rst, Pin.OUT, value=1)
        self.w = width
        self.h = height
        self.rot = rot
        self.buf = bytearray(self.w * 40 * 2)
        self.disp_drv = lv.disp_drv_create()
        self.disp_drv.set_flush_cb(self._flush)
        self.disp_drv.set_draw_buf(lv.draw_buf_create(self.buf, len(self.buf), 0))
        self.disp_drv.set_resolution(self.w, self.h)
        self._reset()
        self._init_reg()
        self.disp_drv.register()

    def _reset(self):
        self.rst(0)
        import time
        time.sleep_ms(10)
        self.rst(1)
        time.sleep_ms(10)

    def _wr_cmd(self, cmd):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytes([cmd]))
        self.cs(1)

    def _wr_data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def _init_reg(self):
        self._wr_cmd(0x36)
        self._wr_data(b'\x00')
        self._wr_cmd(0x3A)
        self._wr_data(b'\x55')
        self._wr_cmd(0x21)
        self._wr_cmd(0x11)
        import time
        time.sleep_ms(120)
        self._wr_cmd(0x29)

    def _flush(self, drv, area, color):
        x1 = area.x1
        y1 = area.y1
        x2 = area.x2
        y2 = area.y2
        self._wr_cmd(0x2A)
        self._wr_data(bytes([0, x1, 0, x2]))
        self._wr_cmd(0x2B)
        self._wr_data(bytes([0, y1, 0, y2]))
        self._wr_cmd(0x2C)
        self.dc(1)
        self.cs(0)
        self.spi.write(color.__dereference__())
        self.cs(1)
        drv.flush_ready()
