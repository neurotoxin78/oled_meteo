import machine, display, time
from micropython import const

tft_rst = machine.Pin(4, machine.Pin.OUT, 1)

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

#------------------
def tft_init(disp):
    # Reset
    tft_rst.value(0)
    time.sleep_ms(120)
    tft_rst.value(1)
    madctl_params = 0b10100000
    for cmd, data, delay in [
        (CMD_SWRESET, None, 150),
        (CMD_SLPOUT, None, 500),
        #(CMD_FRMCTR1, b"\x01\x2c\x2d", None),
        #(CMD_FRMCTR2, b"\x01\x2c\x2d", None),
        #(CMD_FRMCTR3, b"\x01\x2c\x2d\x01\x2c\x2d", None),
        #(CMD_INVCTR, b"\x07", None),
        (CMD_PWCTR1, b"\xa2\x02\x84", None),
        (CMD_PWCTR2, b"\xc5", None),
        (CMD_PWCTR3, b"\x0a\x00", None),
        (CMD_PWCTR4, b"\x8a\x2a", None),
        (CMD_PWCTR5, b"\x8a\xee", None),
        (CMD_VMCTR1, b"\x0e", None),
        (CMD_INVOFF, None, None),
        (CMD_MADCTL, b"\x60", None),
        #(CMD_COLMOD, b"\x05", None),
        (CMD_INVON, None, None),
        (CMD_GMCTRP1, b"\x02\x1c\x07\x12\x37\x32\x29\x2d\x29\x25\x2b\x39\x00\x01\x03\x10", None),
        (CMD_GMCTRN1, b"\x03\x1d\x07\x06\x2e\x2c\x29\x2d\x2e\x2e\x37\x3f\x00\x00\x02\x10", None),
        (CMD_NORON, None, 10),
        (CMD_DISPON, None, 100),
        (CMD_MADCTL, madctl_params.to_bytes(1, 'big'), 10),
        ]:
        if data:
            #print(hex(cmd), str(data))
            disp.tft_writecmddata(cmd, data)
        else:
            #print(hex(cmd))
            disp.tft_writecmd(cmd)
        if delay:
            #print(delay)
            time.sleep_ms(delay)
    disp.tft_writecmd(CMD_SLPOUT)
    time.sleep_ms(120)
    disp.tft_writecmd(CMD_DISPON)


tft = display.TFT()
# Init display with GENERIC type, the display will not be initialized
# This, for example, works for M5Stack display
tft.init(tft.GENERIC, width=160, height=120, miso=19, mosi=23, clk=18, cs=2, dc=5, bgr=False)
# Initialize the display
tft_init(tft)
miny = 10
# fonts used in this demo
fontnames = (
    tft.FONT_Default,
    tft.FONT_7seg,
    tft.FONT_Ubuntu,
    tft.FONT_Comic,
    tft.FONT_Tooney,
    tft.FONT_Minya
)
maxx, maxy = tft.screensize()
tft.clearwin()
tft.clear()
tft.resetwin()
tft.setwin(0, 25, maxx + 3, maxy)
tft.rect(0, 0, maxx, maxy, tft.OLIVE, tft.BLACK)# print display header
tft.font(tft.FONT_Comic, rotate=0)
tft.text(tft.CENTER, 5, "Hello World", tft.ORANGE, transparent=True)
print(tft.winsize())
#tft.resetwin()
