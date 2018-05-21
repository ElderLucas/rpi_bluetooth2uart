import serial

ser = serial.Serial("/dev/ttyS0")
ser.baudrate = 115200
ser.write("ABCD")
ser.close()

