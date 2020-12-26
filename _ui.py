from st7735s import ST7735
import label

class UserInterface(object):
    """docstring for ."""

    def __init__(self):
        self.lcd = ST7735()
        self.main_screen()

    def main_screen(self):
        self.__free_mem_label()
        self.__temperature_value()
        self.__humidity_value()
        self.__pressure_value()

    def __free_mem_label(self):
        self.free_mem_label = label.Label(60, 70, 30, 10, self.lcd)

    def __temperature_value(self):
        self.temp_value = label.Label(60, 10, 30, 10, self.lcd)

    def __humidity_value(self):
        self.humi_value = label.Label(60, 25, 30, 10, self.lcd)

    def __pressure_value(self):
        self.press_value = label.Label(60, 40, 30, 10, self.lcd)

    def set_free_mem_text(self, text, color):
        self.free_mem_label.set_text('RAM: ' + str(text) + ' bytes', color=color)

    def set_temp_value(self, text, color):
        self.temp_value.set_text(str(text), color=color)

    def set_humidity_value(self, text, color):
        self.humi_value.set_text(str(text), color=color)

    def set_pressure_value(self, text, color):
        self.press_value.set_text(str(text), color=color)
