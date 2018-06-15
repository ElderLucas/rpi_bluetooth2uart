import os
import glob
import time
import serial
import RPi.GPIO as GPIO
from bluetooth import *

#configura a serial
#ser = serial.Serial("/dev/ttyS0")
#ser.baudrate = 115200

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


#Configura o BT
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

base_dir = '/sys/bus/w1/devices/'

# device_folder = glob.glob(base_dir + '28*')[0]
device_folder = '/sys/bus/w1/devices/'
device_file = device_folder + '/w1_slave'

#http://blog.davidvassallo.me/2014/05/11/android-linux-raspberry-pi-bluetooth-communication/


while True:

    ser.write(serial.to_bytes([0xAA,    # START WORD

                               0x00,    # BYTE 1 - BLOCK ADDRESS LSW
                               0x00,    # BYTE 2 - BLOCK ADDRESS MSW

                               0x01,    # BYTE 3 - COMMAND - CRUD
                                        # 0x00 Write
                                        # 0x01 Read

                               0x00,    # BYTE 4 - REGISTER ADDRESS MSB
                               0x00,    # BYTE 5-  REGISTER ADDRESS LSB

                               0x31,    # BYTE 6 - DATA MSB
                               0x34,    # BYTE 7 - DATA LSB

                               0x11,    # BYTE 8 - RESERVADO
                               0x33,    # BYTE 9 - RESERVADO
                               0x77,    # BYTE 10 - RESERVADO
                               0x99,    # BYTE 11 - RESERVADO

                               0x55]))  # STOP WORD

    ser_bytes = ser.readline(6)
    decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    print(decoded_bytes)


    #x = ser.read()          # read one byte

    #print x

    #print hex(x)

    #while 1:
    #    x=ser.readline()
    #    print x

    print "ok"

    #print data_rx

    print 'END SERIAL'

    # when your code ends, the last line before the program exits would be...
    GPIO.cleanup()


    break
