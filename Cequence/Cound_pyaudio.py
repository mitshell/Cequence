#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# slight wrapper to pyaudio: http://people.csail.mit.edu/hubert/pyaudio/
# based on the cross-platform audio lib PortAudio
import pyaudio
#
# use python wave module to read wave,
# before streaming it to pyaudio output
import wave
WAVE_DIR = './sounds/'

class Streamer(object):
    #
    dbg = 0
    #
    # this is the configuration for the samples in the 'sounds' directory
    _samplerate = 44100 # 44100 Hz
    _samplefmt = 8 # int16 -signed-
    _channels = 1 # mono
    
    def __init__(self):
        # start and configure PortAudio
        self.pa = pyaudio.PyAudio()
        self._samplerate = Streamer._samplerate
        self._samplefmt = Streamer._samplefmt
        self._channels = Streamer._channels
        # yet, not streaming
        self._streaming = False
    
    def start(self):
        self._streaming = True
        self.stream = self.pa.open(
                format   = self._samplefmt,
                channels = self._channels,
                rate     = self._samplerate,
                output   = True)
        if self.dbg:
            print('Streamer() started')
        return self.stream
        
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self._streaming = False
        if self.dbg:
            print('Streamer() stopped')
    
    
# Sound object:
# grab a wave file
# and read it to pyaudio output each time .run() is called
class Sound(object):
    
    # pyaudio Mixer as class attribute
    # no need to instantiate it for each Sound()
    MIX = Streamer()
    #
    # wave chunk size to be streamed
    CHK_SIZE = 1024
    
    def __init__(self, wave_file='djembe_2.wav'):
        self.wave_path = '%s%s' % (WAVE_DIR, wave_file)
        try:
            # try to open the wave file
            self.wave = wave.open(self.wave_path, 'rb')
        except IOError:
            print('file %s not found: this Sound() will actually not play' \
                   % self.wave_path)
        else:
            # get wave file parameters
            if self.wave.getparams()[0:3] != ( \
                            self.MIX._channels,
                            self.MIX.pa.get_sample_size(Streamer._samplefmt),
                            self.MIX._samplerate):
                print('sound file has not the correct settings')
                raise(Exception)
    
    def run(self):
        # if wave file had been found
        if hasattr(self, 'wave'):
            # rewind the wave
            self.wave.rewind()
            # if Streamer() already streaming, stop it
            if self.MIX._streaming:
                self.MIX.stop()
            # initialize wave and PA stream
            data = self.wave.readframes(self.CHK_SIZE)
            s = self.MIX.start()
            # send wave stream to PA
            while data:
                s.write(data)
                data = self.wave.readframes(self.CHK_SIZE)
#

