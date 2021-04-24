#!/usr/bin/python


import midi
from midi import MidiConnector
from midi import ControlChange, Message

read = True
midi_connection = MidiConnector('/dev/midi3')

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
