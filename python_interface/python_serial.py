#!/usr/bin/python
import sys
import serial

print "hello"
print "python " + str(sys.version) + " " + str(sys.version_info)

arduino = serial.Serial('/dev/ttyUSB1', 57600, timeout=.1)
i=0
while True:
	message = arduino.readline()[:-2]
	i = i + 1
	if message:
		left = message.split("b")[1]
	        right = message.split("b")[0]
		print "left: " + str(left) + "\tright: " + str(right)

