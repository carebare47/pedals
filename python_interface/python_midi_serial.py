#!/usr/bin/python
import sys
import serial
from serial.serialutil import SerialException
import time
import rtmidi


midi_out = rtmidi.MidiOut()
midi_out.open_port(1)

'''
0: Sysex (13 bytes)
    F0 41 10 00 00 72 12 00 00 00 08 78 F7 
1: Sysex (13 bytes)
    F0 41 10 00 00 72 12 00 00 00 08 78 F7 
2: Sysex (13 bytes)
    F0 41 10 00 00 72 12 00 00 00 08 78 F7 
3: Sysex (13 bytes)
    F0 41 10 00 00 72 12 00 00 00 08 78 F7 
4: Sysex (13 bytes)
    F0 41 10 00 00 72 12 00 00 00 08 78 F7 
'''


arduino = serial.Serial('/COM4', 57600, timeout=.1)


i=0
deadband=30
def _map(x, in_min, in_max, out_min, out_max):
	return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
tflag = False
last_reading = 0
last_l = 0
last_r = 0
# time_limit_ms = 
while True:
	message = arduino.readline()[:-2]
	i = i + 1
	if message:
		left = int(message.split(b'b')[1])
		right = int(message.split(b'b')[0])
		if left < 0:
			left = 0
		if left > 1024:
			left = 1024
		if right < 0:
			right = 0
		if right > 1024:
			right = 1024
		if right > 20 and right == last_r:
                        right = right - 1
		if left > 20 and left == last_l:
                        left = left - 1
		print("left: " + str(left) + "\tright: " + str(right))
		midi_out.send_message([0xB0, 44, _map(int(left), 0, 1024, 0, 120)]) # volume
		midi_out.send_message([0xB0, 43, _map(int(right), 0, 1024, 35, 105)])
		last_l = left
		last_r = right
		if not time.localtime(time.time())[5] % 10 and not tflag:
			print(time.asctime(time.localtime(time.time())))
			tflag = True
