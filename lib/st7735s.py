import framebuf
import time
from machine import Pin, SPI, I2C

'''
import m5stickc_lcd
lcd = m5stickc_lcd.ST7735()
lcd.text('hello', 10, 10, 0xffff)
lcd.show()
'''

class ST7735(framebuf.FrameBuffer):

    # command definitions
    CMD_NOP = const(0x00)  # No Operation
    CMD_SWRESET = const(0x01)  # Software reset
    CMD_RDDID = const(0x04)  # Read Display ID
    CMD_RDDST = const(0x09)  # Read Display Status

    CMD_SLPIN = const(0x10)  # Sleep in & booster off
    CMD_SLPOUT = const(0x11)  # Sleep out & booster on
    CMD_PTLON = const(0x12)  # Partial mode on
    CMD_NORON = const(0x13)  # Partial off (Normal)

    CMD_INVOFF = const(0x20)  # Display inversion off
    CMD_INVON = const(0x21)  # Display inversion on
    CMD_DISPOFF = const(0x28)  # Display off
    CMD_DISPON = const(0x29)  # Display on
    CMD_CASET = const(0x2A)  # Column address set
    CMD_RASET = const(0x2B)  # Row address set
    CMD_RAMWR = const(0x2C)  # Memory write
    CMD_RAMRD = const(0x2E)  # Memory read

    CMD_PTLAR = const(0x30)  # Partial start/end address set
    CMD_COLMOD = const(0x3A)  # Interface pixel format
    CMD_MADCTL = const(0x36)  # Memory data access control

    CMD_RDID1 = const(0xDA)  # Read ID1
    CMD_RDID2 = const(0xDB)  # Read ID2
    CMD_RDID3 = const(0xDC)  # Read ID3
    CMD_RDID4 = const(0xDD)  # Read ID4

    # panel function commands
    CMD_FRMCTR1 = const(0xB1)  # In normal mode (Full colors)
    CMD_FRMCTR2 = const(0xB2)  # In Idle mode (8-colors)
    CMD_FRMCTR3 = const(0xB3)  # In partial mode + Full colors
    CMD_INVCTR = const(0xB4)  # Display inversion control

    CMD_PWCTR1 = const(0xC0)  # Power control settings
    CMD_PWCTR2 = const(0xC1)  # Power control settings
    CMD_PWCTR3 = const(0xC2)  # In normal mode (Full colors)
    CMD_PWCTR4 = const(0xC3)  # In Idle mode (8-colors)
    CMD_PWCTR5 = const(0xC4)  # In partial mode + Full colors
    CMD_VMCTR1 = const(0xC5)  # VCOM control

    CMD_GMCTRP1 = const(0xE0)
    CMD_GMCTRN1 = const(0xE1)

    # colors
    COLOR_BLACK = const(0x0000)
    COLOR_BLUE = const(0x001F)
    COLOR_RED = const(0xF800)
    COLOR_GREEN = const(0x07E0)
    COLOR_CYAN = const(0x07FF)
    COLOR_MAGENTA = const(0xF81F)
    COLOR_YELLOW = const(0xFFE0)
    COLOR_WHITE = const(0xFFFF)


    def __init__(self):
        self.baudrate = 27000000
        self.cs = Pin(2, Pin.OUT, value=1)
        self.dc = Pin(5, Pin.OUT, value=1)
        self.rst = Pin(4, Pin.OUT, value=1)
        self.spi = SPI(
                1, baudrate=self.baudrate,
                polarity=0, phase=0, bits=8, firstbit=SPI.MSB,
                sck=Pin(18), mosi=Pin(23), miso=Pin(19))
        self.rst.value(1)
        time.sleep_ms(5)
        self.rst.value(0)
        time.sleep_ms(20)
        self.rst.value(1)
        time.sleep_ms(150)

        self.width = 160
        self.height = 80
        self.buffer = bytearray(self.width * self.height * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

    def init_display(self):

        # Controls lcd screen orientation, read ST7735 documentation on MADCTL configuration
        madctl_params = 0b10100000
        #madctl_params = 0b01100000

        for cmd, data, delay in [
            (self.CMD_SWRESET, None, 150),
            (self.CMD_SLPOUT, None, 500),
            (self.CMD_FRMCTR1, b'\x01\x2c\x2d', None),
            (self.CMD_FRMCTR2, b'\x01\x2c\x2d', None),
            (self.CMD_FRMCTR3, b'\x01\x2c\x2d\x01\x2c\x2d', None),
            (self.CMD_INVCTR, b'\x07', None),
            (self.CMD_PWCTR1, b'\xa2\x02\x84', None),
            (self.CMD_PWCTR2, b'\xc5', None),
            (self.CMD_PWCTR3, b'\x0a\x00', None),
            (self.CMD_PWCTR4, b'\x8a\x2a', None),
            (self.CMD_PWCTR5, b'\x8a\xee', None),
            (self.CMD_VMCTR1, b'\x0e', None),
            (self.CMD_INVOFF, None, None),
            (self.CMD_MADCTL, b'\x60', None),
            (self.CMD_COLMOD, b'\x05', None),
            (self.CMD_INVON, None, None),
            (self.CMD_GMCTRP1, b'\x02\x1c\x07\x12\x37\x32\x29\x2d\x29\x25\x2b\x39\x00\x01\x03\x10', None),
            (self.CMD_GMCTRN1, b'\x03\x1d\x07\x06\x2e\x2c\x29\x2d\x2e\x2e\x37\x3f\x00\x00\x02\x10', None),
            (self.CMD_NORON, None, 10),
            (self.CMD_DISPON, None, 100),
            (self.CMD_MADCTL, madctl_params.to_bytes(1, 'big'), 10),
        ]:
            self.write_cmd(cmd)
            if data:
                self.write_data(data)
            if delay:
                time.sleep_ms(delay)
        self.fill(0)
        self.show()

    def turn_off(self):
        self.write_cmd(self.CMD_SLPIN)


    def turn_on(self):
        self.write_cmd(self.CMD_SLPOUT)

    def show(self):
        self.write_cmd(self.CMD_CASET)
        self.write_data(b'\x00\x01\x00\xA0')
        self.write_cmd(self.CMD_RASET)
        # Not sure why RASET start position is x1a...
        self.write_data(b'\x00\x1a\x00\x69')
        self.write_cmd(self.CMD_RAMWR)
        self.write_data(self.buffer)

    def write_cmd(self, cmd):
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(bytes([cmd]))
        self.cs.value(1)

    def write_data(self, buf):
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(buf)
        self.cs.value(1)
