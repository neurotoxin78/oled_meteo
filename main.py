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
    ui.temp_label(sensor.temperature, MAGENTA)
    ui.humi_label(sensor.humidity, LIME)
    ui.pres_label(sensor.pressure, GAINSBORO)
    collect()
    sleep(0.5)
