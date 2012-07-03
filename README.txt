Cequence
========

event sequencing: mostly for sounds and audio

### Why ?
little library for sequencing events.
Here: sounds are given as examples (actually, this is the initial goal: to make a sound sequencer in python).
However, any instance that has a .run() method can be sequenced.

### Installation:
copy the 'Cequence' repository into your current python site-packages repository.
Currently, 'Sound' class within Cequence.py only supports Windows system: 
I will have anyway to find something better than this dummy API for playing audio.

### Testing:
simply import test() from Cequence, and run it.
E.g. :
    >>> from Cequence.Cequence import *
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
    >>>

### Building a sequence:
1) configure the sequencer:
    >>> from Cequence.Cequence import *
    >>> s = Sequencer()
as soon as you create a Sequencer() instance (or even before, cause it's mostly class attribute),
you can modify the following attributes:
.BPM : beat per minute, the higher the faster
    >>> Sequencer.BPM = 250; test(4)
.BEAT_NUM : number of beats per sequence
.BEAT_DIV : number of sub-steps between 2 beats (this is like the resoution of the sequence)
    >>> Sequencer.BPM = 100; Sequencer.BEAT_DIV = 2; test(2)

2) create an EVENT_GRID: 
>>> s.EVENT_GRID = my_sound_grid
the EVENT_GRID is a dictionnary, where each key is an event which needs to have a .run() method.
For each event, you provide a list a beat offset, for when the event will be run()ed.
E.g. for the test() function, we have defined:
        {
        Sound('sounds/tamtam_1.wav') : [0, 2, 4, 6], 
        Sound('sounds/percviet_6.wav') : [1, 3, 5.25, 5.5, 7],
        Sound('sounds/guiro_4.wav') : [2.5, 6.5],
        }

3) start the sequencer:
    >>> s.start()
The sequence will start in background, 
and you will be able to modify all parameters live while the sequence is playing.

3_bis) update the sequencer live:
e.g. the EVENT_GRID:
    >>> s.EVENT_GRID[Sound('sounds/djembe_2.wav')] = [0.3, 6.7]
    >>> s.EVENT_GRID[Sound('sounds/maracas_6.wav')] = [ 0.98, 3.5, 7.5]
    >>> s.EVENT_GRID[Sound('sounds/guiro_4.wav')] = [2.8, 4.8]
and the BPM:
    >>> s.BPM = 90

4) stop the sequencer:
    >>> s.stop()

### Interested in it ?
email me:
michau [do] benoit [a] gmail [do] com

