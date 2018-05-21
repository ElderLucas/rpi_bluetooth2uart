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
#	print(read_temp())	
#	time.sleep(1)


	server_sock=BluetoothSocket( RFCOMM )
	server_sock.bind(("",PORT_ANY))
	server_sock.listen(1)

	port = server_sock.getsockname()[1]

	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

	advertise_service( server_sock, "raspberrypi",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
#  while True:          
	print "Waiting for connection on RFCOMM channel %d" % port

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
			ser.write("1")


		elif data == 'lightOn':
			GPIO.output(17,False)
			data = 'light on!'
                        ser.write("2")
   

		elif data == 'lightOff':
			GPIO.output(17,True)
			data = 'Read ADC 0'
			ser.write("#")
			ser.write("A")
			ser.write("$")
			data_rx = ser.read(10)
			print "sending [%s]" % data_rx
                        


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
