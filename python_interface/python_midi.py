#!/usr/bin/python


import midi
from midi import MidiConnector
from midi import ControlChange, Message
from serial.serialutil import SerialException
import time

read = True

'''
for i in range(0, 10):
	try:
		print "trying :" + "/dev/midi" + str(i)
		midi_connection = MidiConnector('/dev/midi' + str(i))
	except SerialException as e:
		print e
		pass
	except:
		print e
	else:
		print "found midi device at /dev/midi" + str(i)
		break
	time.sleep(1)
'''

try:
	midi_connection = MidiConnector('/dev/snd/midiC1D0')
except SerialException as e:
	print e
	exit()

if not read:
	control_change = ControlChange(100, 127)
	msg = Message(control_change, channel=1)
else:
	msg2 = midi_connection.read()  # blocks
	for whatever in msg2:
		print whatever

	print
	print
	print
