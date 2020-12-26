from time import sleep
from gc import collect, mem_free
from devices import SENSOR
from ui import UserInterface
from rgb565color import *

collect()

ui = UserInterface()
sensor = SENSOR()

while KeyboardInterrupt:
    ui.mem_free_label(mem_free(), CORAL)
    ui.temp_label(sensor.temperature, CRIMSON)
    ui.humi_label(sensor.humidity, FIREBRICK)
    #ui.set_temp_value(sensor.temperature, AZURE)
    #ui.set_humidity_value(sensor.humidity, DODGERBLUE)
    #ui.set_pressure_value(sensor.pressure, GAINSBORO)
    collect()
    sleep(0.1)
