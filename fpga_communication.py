#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

# Inicio do Protocolo de Comunicacao com a FPGA
start = 0xAA

# Endereco dos blocos que se quer acessar para escrita ou leitura
# ---- 0x00 -Master
# ---- 0x01 -GPIO Access Write
BlockAddressLSB = 0x01
BlockAddressMSB = 0x00

# Operacao que se deseja executar
# ----- 0x00 Operação de escrita nos REGISTROS
# ----- 0x01 Operação de Leitura nos REGISTROS
COMMAND = 0x00

# Endereço do Registro do Bloco que se acessou
RegAddressLSB = 0x00
RegAddressMSB = 0x00

# Dados para Escrita no Registro do Bloco selecionado
DataLSB = 0x00
DataMSB = 0x00

# Fim do Protocolo.
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

	#print "Waiting for connection on RFCOMM channel %d" % port

	client_sock, client_info = server_sock.accept()
	#print "Accepted connection from ", client_info

    by = serial.to_bytes([start,BlockAddressLSB,BlockAddressMSB,COMMAND,RegAddressLSB,RegAddressMSB,DataMSB,DataLSB,0x00,0x00,0x00,0x00,Stop])

    ser.write(by)

    ser_bytes = ser.readline(8)
    resp = ser_bytes.encode("hex")

    print resp

    #decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    #print(decoded_bytes)
    GPIO.cleanup()




try:
    print "ok"
except IOError:
    pass
except KeyboardInterrupt:
    print "dosconct"
