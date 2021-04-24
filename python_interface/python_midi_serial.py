#!/usr/bin/python
import sys
import serial
import midi
from midi import MidiConnector
from midi import ControlChange, Message
from serial.serialutil import SerialException
import time


print "hello"
print "python " + str(sys.version) + " " + str(sys.version_info)
try:
	midi_connection = MidiConnector('/dev/snd/midiC1D0')
except SerialException as e:
	print e
	exit()

arduino = serial.Serial('/dev/ttyUSB1', 57600, timeout=.1)
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
			control_change = ControlChange(7, _map(left, 0, 1024, 0, 127))
			msg = Message(control_change, channel=1)
			midi_connection.write(msg)
