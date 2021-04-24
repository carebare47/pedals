#!/usr/bin/python
import sys
import serial
from serial.serialutil import SerialException
import time
import rtmidi_python as rtmidi


midi_out = rtmidi.MidiOut()
midi_out.open_port(1)



for i in range(0, 4):
	try:
		arduino = serial.Serial('/dev/ttyUSB' + str(i), 57600, timeout=.1)
		break
	except SerialException as e:
		print e


i=0
deadband=30
def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


while True:
	message = arduino.readline()[:-2]
	i = i + 1
	if message:
		left = message.split("b")[1]
	        right = message.split("b")[0]
		print "left: " + str(left) + "\tright: " + str(right)
		if left > deadband:
			midi_out.send_message([0xB0, 7, _map(left, 0, 1024, 0, 127)]) # volume
