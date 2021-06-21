#!/usr/bin/python
import sys
import serial
from serial.serialutil import SerialException
import time
import numpy as np
import rtmidi_python as rtmidi
import math


'''
def callback(message, time_stamp):
    print message, time_stamp

midi_in = rtmidi.MidiIn()
midi_in.callback = callback
midi_in.open_port(0)

# do something else here (but don't quit)
Note that the signature of the callback differs from the original RtMidi API: message is now the first parameter, like in the tuple returned by get_message().

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
		#self.midi_in = rtmidi.MidiIn()
		#self.midi_in.callback = self.callback
		#self.midi_in.open_port(0)
		self.samples = []
		self.beat_dict = {j:None for j in range(0, 16)}
                #while True:
                #        self.loop()

	def callback(self, message, time_stamp):
                for element in message:
			print "callback: {} @ {}".format(element, time_stamp)
		if self.beat_dict[self.sub_beat] == None:
			self.beat_dict[self.sub_beat] = (message, time_stamp)

	def play(self, msg):
		message = msg[0]
		time_stamp = msg[1]
		for sub_msg in message:		
			print "playing {}".format(sub_msg)


        def loop(self):
                now = time.time()
                loop_end_time = now + 8.0
		j = 0
                while (j < 16):
			self.sub_beat = j
			if self.beat_dict[self.sub_beat] is not None:
				self.play(self.beat_dict[self.sub_beat])
			if j%4 == 0:
				print "beat {} ".format(j),
                        self.record_2(loop_end_time, now, j)
			j = j + 1
                print("NEW BAH j: {j}".format(j=j))
		for key in sorted(self.beat_dict):
			print key, self.beat_dict[key]
		#for s in self.samples:
		#	print s

	def record_2(self, loop_end_time, now, sub_beat):
                beat_end_time = time.time() + (loop_end_time - time.time()) % self.beat_time_s
                print "loop_end_time, now, sub_beat, beat_end_time: {} {} {} {}".format(loop_end_time, now, sub_beat, beat_end_time)
		self.get_samples(beat_end_time, sub_beat)

	def get_samples(self, end_time, sub_beat):
		while time.time() < end_time:
			pass
		return


        def record(self, t_time):
                current_beat = math.ceil((self.bar_length_seconds - t_time) / self.bps)
                remainder = math.floor((self.bar_length_seconds - t_time) % self.bps)
                if remainder != self.last_remainder:
                        print(current_beat, remainder, self.last_remainder)
                        self.last_remainder = remainder


loop = PyLooper()
while True:
	loop.loop()
