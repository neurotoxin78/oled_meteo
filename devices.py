import machine, bme280

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))

class UI(object):
    """
    docstring
    """
    def __init__(self):
        """
        docstring
        """
        pass

    def text(self, text, x, y):
        pass

class SENSOR(object):
    """
    docstring
    """
    def __init__(self):
        """
        docstring
        """
        self.bme = bme280.BME280(i2c=i2c)
    def __get_temp(self):
        return self.bme.values[0]
    def __get_humi(self):
        return self.bme.values[2]
    def __get_pres(self):
        return self.bme.values[1]
    temperature = property(__get_temp)
    humidity = property(__get_humi)
    pressure = property(__get_pres)
