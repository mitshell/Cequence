#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# slight wrapper to pygame mixer: http://www.pygame.org/docs/ref/mixer.html
from pygame import mixer
#
# use python wave module to read wave,
# before streaming it to pyaudio output
import wave
WAVE_DIR = './sounds/'


# this is the audio buffer size for pygame.mixer
AUDIO_BUFSZ = 2048 
# this is the configuration for the samples in the 'sounds' directory
_samplerate = 44100 # 44100 Hz
_samplefmt = -16 # int16 -signed-
_channels = 1 # mono

# init pygame mixer
mixer.init(frequency   = _samplerate,
           size        = _samplefmt,
           channels    = _channels,
           buffer      = AUDIO_BUFSZ)

    
    
# Sound object:
# grab a wave file
# and play it with pygame.mixer each time .run() is called
class Sound(object):
    
    def __init__(self, wave_file='djembe_2.wav'):
        self.wave_path = '%s%s' % (WAVE_DIR, wave_file)
        try:
            # try to open the wave file through pygame.mixer.Sound
            self.wave = wave.open(self.wave_path, 'rb')
            #self.wave = mixer.Sound(self.wave_path)
        except IOError:
            print('file %s not found: this Sound() will actually not play' \
                   % self.wave_path)
        else:
            # get wave file parameters
            red = -8 if _samplefmt < 0 else 8
            if self.wave.getparams()[0:3] != (_channels,
                                              _samplefmt/red,
                                              _samplerate):
                print('sound file has not the correct settings')
                raise(Exception)
            # read the wave into memory
        #
        if hasattr(self, 'wave'):
            # get a channel from pygame.mixer
            self._chan = mixer.find_channel()
            if self._chan is None:
                print('could not get a channel from pygame.mixer')
            #
            #self._buf = self.wave.readframes(self.wave.getnframes())
            #self._snd = mixer.Sound(self._buf)
            self._snd = mixer.Sound(self.wave_path)
    
    def run(self):
        # if wave file had been found
        if hasattr(self, '_chan') and self._chan is not None:
            self._chan.play(self._snd)
#

