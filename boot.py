# This file is executed on every boot (including wake-boot from deepsleep)
import sys
sys.path[1] = '/flash/lib'
import gc
gc.collect()
import network

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan()                             # Scan for available access points
sta_if.connect("Neurotoxin2", "Mxbb2Col")  # Connect to an AP
sta_if.isconnected()
sta_if.ifconfig()
