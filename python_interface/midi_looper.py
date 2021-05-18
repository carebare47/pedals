#!/usr/bin/python
import sys
import serial
from serial.serialutil import SerialException
import time
import numpy as np
# import rtmidi
import math

#midi_out = rtmidi.MidiOut()
#midi_out.open_port(1)

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

bpm = 120
bps = bpm/60

class MidiData():
	def __init__(self, name):
		self.name = name
		self.data = {}

	

class PyLooper():
        def __init__(self, bpm=120, time_sig=4):
                self.bpm = bpm
                self.bps = bpm/60.0
                self._valid_time_sigs = [2, 3, 4]
                if time_sig not in self._valid_time_sigs:
                        print("uh oh time sig not valid")
                        raise
                self.time_sig = time_sig
                self.current_time = time.time()
                self.bar_length_seconds = self.bps * time_sig
                self.last_remainder = 0
		self.data = MidiData("test")
                self.beat_time_s = self.bar_length_seconds / 20
		self.timer2 = time.time()
                self.buffer = {(self.beat_time_s*x):None for x in range(0, 100)}



		self.samples = []
                #while True:
                #        self.loop()

        def loop(self):
                now = time.time()
                loop_end_time = now + 8.0
		j = 0
                while (time.time() < loop_end_time):
			if j%4 == 0:
				print "beat {} ".format(j),
                        self.record_2(loop_end_time, now, j)
			j = j + 1
                print("NEW BAH j: {j}".format(j=j))
		for key, value in self.buffer.iteritems():
			print key, value
		#for s in self.samples:
		#	print s

	def record_2(self, loop_end_time, now, sub_beat):
                beat_end_time = time.time() + (loop_end_time - time.time()) % self.beat_time_s
		self.samples.append("{e}".format(e=beat_end_time))
		# print "time:{time} beat_end_time:{sample}".format(time=(loop_end_time - time.time()), sample=(loop_end_time - beat_end_time))
		timestamp, sample = self.get_samples(beat_end_time)
		print timestamp, sample
		key = '{a}_{b}'.format(a=str(sub_beat), b=str(timestamp))
		print key
		self.buffer[key] = sample

	def get_samples(self, end_time):
		i=0
		while time.time() < end_time:
			#print "new_sample"
			#things = []
			#midi_thing = self.get_midi_stuff()
			timestamp, sample = self.get_midi_stuff(end_time)
			self.data.data[timestamp] = sample
			#things.append(midi_thing)
			i = i + 1
			#print ".",
		print "s: {i}".format(i=i)
		return timestamp, sample

	def get_midi_stuff(self, end_time):
		self.timer2 = time.time()
		while not self.midi_ready():
			pass
		sample = None
		timestamp = round(end_time - time.time(), 2)
		return timestamp, sample

	def midi_ready(self): 
		if (self.timer2 + 0.05 < time.time()):
			return 1
		else:
			return 0

        def record(self, t_time):
                current_beat = math.ceil((self.bar_length_seconds - t_time) / self.bps)
                remainder = math.floor((self.bar_length_seconds - t_time) % self.bps)
                if remainder != self.last_remainder:
                        print(current_beat, remainder, self.last_remainder)
                        self.last_remainder = remainder


loop = PyLooper()
exit()
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
