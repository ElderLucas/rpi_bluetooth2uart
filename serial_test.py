import os
import glob
import time
import serial
import RPi.GPIO as GPIO
from bluetooth import *

#configura a serial
ser = serial.Serial("/dev/ttyS0")
ser.baudrate = 115200

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
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)
    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service( server_sock, "raspberrypi",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ])
#                  protocols = [ OBEX_UUID ])

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
            # data = str(read_temp())+'!'
            data = 'IACIT'
            #ser.write(serial.to_bytes([0x4C,0x12,0x01,0x00,0x03,0x40,0xFB,0x02,0x7a]))
            ser.write(serial.to_bytes([0xAA,
                                       0x00,  #BYTE 1 - BLOCK ADDRESS LSW
                                       0x00,  #BYTE 2 - BLOCK ADDRESS MSW

                                       0x00,  #BYTE 3 - COMMAND - CRUD

                                       0x00,  #BYTE 4 - REGISTER ADDRESS MSB
                                       0x00,  #BYTE 5-  REGISTER ADDRESS LSB

                                       0x00,  #BYTE 6 - DATA MSB
                                       0x00,  #BYTE 7 - DATA LSB

                                       0x00,  #BYTE 8 - RESERVADO
                                       0x00,  #BYTE 9 - RESERVADO
                                       0x00,  #BYTE 10 - RESERVADO
                                       0x00,  #BYTE 11 - RESERVADO

                                       0x55]))#STOP WORD

            client_sock.send(data)
            print "sending [%s]" % data
            client_sock.close()
            server_sock.close()
            print "all done"
            break
            #ser.write()

    	#elif data == 'lightOn':
    	#	GPIO.output(17,False)
    	#	data = 'TESTE 1'
        #    ser.write("2")

        #elif data == 'lightOff':
        #    GPIO.output(17,True)
    	#	data = 'Read ADC 0'
    	#	ser.write("#")
    	#	ser.write("A")
    	#	ser.write("$")
    	#	data_rx = ser.read(10)
    	#	print "sending [%s]" % data_rx



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
    	print "all done"

        break
