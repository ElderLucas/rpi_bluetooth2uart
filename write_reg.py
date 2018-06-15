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
BlockAddressLSB = 0x01
BlockAddressMSB = 0x00
COMMAND = 0x00

RegAddressLSB = 0x00
RegAddressMSB = 0x00

DataLSB = 0x00
DataMSB = 0x00

Stop = 0x55

while True:

    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)
    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service( server_sock, "raspberrypi",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ])

    print("Waiting for connection on RFCOMM channel %d" % (port))

    client_sock, client_info = server_sock.accept()
    print "Accepted connection from ", client_info

    try:
        data = client_sock.recv(1024)

        if len(data) == 0:
            print 'no data iacit!'
            break
        print "received [%s]" % data

        if data == 'temp':
            ser.write(serial.to_bytes([start,BlockAddressLSB,BlockAddressMSB,COMMAND,RegAddressLSB,RegAddressMSB,0x01,0x01,0x00,0x00,0x00,0x00,Stop]))
            client_sock.close()
            server_sock.close()
            print "temp"


    	elif data == 'lightOn':
            ser.write(serial.to_bytes([start,BlockAddressLSB,BlockAddressMSB,COMMAND,RegAddressLSB,RegAddressMSB,0xFF,0xFF,0x00,0x00,0x00,0x00,Stop]))
            client_sock.close()
            server_sock.close()
            print "lightOn"


    	elif data == 'lightOff':
            ser.write(serial.to_bytes([start,BlockAddressLSB,BlockAddressMSB,COMMAND,RegAddressLSB,RegAddressMSB,0x00,0x00,0x00,0x00,0x00,0x00,Stop]))
            client_sock.close()
            server_sock.close()
            print "lightOff"

        #client_sock.send(data)
        #print "sending [%s]" % data
        #client_sock.close()
        #server_sock.close()
        #GPIO.cleanup()
        #print "all done"
        #break

        else:
            data = 'WTF!'
            client_sock.send(data)
            print "sending [%s]" % data
            client_sock.close()
            server_sock.close()


    except IOError:
        pass

    except KeyboardInterrupt:
        print "disconnected"

        client_sock.close()
        server_sock.close()
        GPIO.cleanup()
        print "all done"

        break


#ser.write(serial.to_bytes([start,BlockAddressLSB,BlockAddressMSB,COMMAND,RegAddressLSB,RegAddressMSB,DataMSB,DataLSB,0x00,0x00,0x00,0x00,Stop]))
#ser_bytes = ser.readline(8)
#resp = ser_bytes.encode("hex")
#
#print resp

#decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
#print(decoded_bytes)
#GPIO.cleanup()

def sendMessageTo(targetBluetoothMacAddress):
  port = 1
  sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  sock.connect((targetBluetoothMacAddress, port))
  sock.send("hello!!")
  sock.close()
