import os
import glob
import time
import serial
import RPi.GPIO as GPIO
from bluetooth import *

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
base_dir = '/sys/bus/w1/devices/'
device_folder = '/sys/bus/w1/devices/'
device_file = device_folder + '/w1_slave'

start = 0xAA
BlockAddressLSB = 0x00
BlockAddressMSB = 0x00
COMMAND = 0x01

RegAddressLSB = 0x00
RegAddressMSB = 0x00

Stop = 0x55

ser.write(serial.to_bytes([start,BlockAddressLSB,BlockAddressMSB,COMMAND,RegAddressLSB,RegAddressMSB,0x43,0x44,0x00,0x00,0x00,0x00,Stop]))
ser_bytes = ser.readline(8)

print ser_bytes.encode("hex")

#decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
#print(decoded_bytes)
GPIO.cleanup()
