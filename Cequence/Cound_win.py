#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# using python windows sound API
from winsound import PlaySound, SND_FILENAME, SND_NODEFAULT, SND_NOWAIT, \
                     SND_NOSTOP, SND_ASYNC
#
WAVE_DIR = './sounds/'

###
# The following is just given as example under windows
# This is going to be updated to a better and cross-ptf python sound library
class Sound(object):
    
    def __init__(self, sound_path='djembe_2.wav'):
        self._path = '%s%s' % (WAVE_DIR, sound_path)
    
    def run(self):
        flags = SND_FILENAME | SND_NODEFAULT | SND_ASYNC
        threadit(PlaySound, (self._path, flags))


