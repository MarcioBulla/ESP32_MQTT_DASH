import sys
sys.path.reverse()
from lib.umqtt.simple import MQTTClient
import machine
import esp
import time
import network
from machine import WDT
import ubinascii
import gc
from machine import Pin 

machine.freq(240000000)

esp.osdebug(None)
gc.collect()

ssid = "Marcio Bulla"
password = "senha"
mqtt_server = "IP_mqtt_server"
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = "entrada"
topic_pub = "saida"
led = Pin(2, Pin.OUT)
button = Pin(4, Pin.IN, Pin.PULL_UP)

