############
# Cequence #
############

### Why ?
little library for sequencing events.
Here: sounds are given as examples (actually, this is the initial goal: to make a sound sequencer in python).
However, any instance that has a .run() method can be sequenced.


### Installation:
1) Copy the 'Cequence' repository into your current python site-packages repository, or anywhere in your $PYTHONPATH
I am using python2.7, not sure it will work with previous versions of python.
And for sure, it is not going to work with python3.
2) 'Sound' class is now running thanks to pygame: www.pygame.org/docs/ref/mixer.html, so install pygame on your system.
You can still fallback on the windows API  (embedded into python 2.7) by importing 'Sound' from Cound_win.py in the Cequence.py header.
You can also try the API based on PortAudio and its python binding pyaudio (see http://people.csail.mit.edu/hubert/pyaudio/), 
however, it makes my ALSA segfaulting a lot (I surely did wrong somewhere).


### Testing:
simply import test() from Cequence, and run it.
    >>> from Cequence.Cequence import *
    >>> Sequencer.dbg = 1 # this is to have those nice print()
    >>> s = test()
    [+] sequencer started
    [+] playing sequence 0
    [+] playing sequence 1
    [+] playing sequence 2
    [+] playing sequence 3
    [+] playing sequence 4
    [+] sequencer stopped
    >>> s
    <Cequence.Cequence.Sequencer object at 0x02B9AB50>
    >>> s.start() # this will re-run the loop (infinitely, if you don't stop it)
    >>> s.stop()


### Building a sequence:
1) configure the sequencer:
    >>> from Cequence.Cequence import *
    >>> s = Sequencer()
as soon as you create a Sequencer() instance (or even before, cause it's mostly class attribute),
you can modify the following attributes:
.BPM : beat per minute, the higher the faster
    >>> Sequencer.BPM = 250; test()
.BEAT_NUM : number of beats per sequence
.BEAT_DIV : number of sub-steps between 2 beats (this is like the resoution of the sequence)
    >>> Sequencer.BPM = 100; Sequencer.BEAT_DIV = 3; test()
    >>> Sequencer.BEAT_DIV = 16 # comes back to something more conventional...

2) create an EVENT_GRID:
e.g. : s.EVENT_GRID = {Sound('some_wavefile') : [offset1, offset2, ...], ...}
the EVENT_GRID is a python dictionnary, where each key is an event which needs to have a .run() method.
For each event, you provide a list a beat offset, for when the event will be run()ed.
E.g. for the test() function, we have defined:
    >>> s.EVENT_GRID = { \
        Sound('tamtam_1.wav') : [0, 2, 4, 6], 
        Sound('percviet_6.wav') : [1, 3, 5.25, 5.5, 7],
        Sound('guiro_4.wav') : [2.5, 6.5],
        Sound('djembe_2.wav') : [0.75, 2.75, 4.5, 6.5, 7.25] }

3) start the sequencer:
    >>> s.start()
The sequence will start in background, 
and you will be able to modify all parameters live while the sequence is playing.

3_bis) update the sequencer live:
e.g. the EVENT_GRID:
    >>> s.EVENT_GRID[Sound('maracas_7.wav')] = [0.3, 6.7]
    >>> s.EVENT_GRID[Sound('maracas_6.wav')] = [ 0.98, 3.5, 7.5]
    >>> s.EVENT_GRID[Sound('guiro_4.wav')] = [2.8, 4.8]
and the BPM:
    >>> s.BPM = 90
and strange beat division
    >>> s.BEAT_DIV = 5
and go for some d&b
    >>> s.BPM = 180

4) stop the sequencer:
    >>> s.stop()

