#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# Python library for sequencing events
# mostly for sounds (e.g. making a beatbox)

from time import time, sleep
from thread import start_new_thread as threadit
# TODO: find an effective audio API including a mixer !!!
#from Cound_win import Sound
#from Cound_pyaudio import Sound
# actually pygame looks like the winner:
from Cound_pygame import Sound

class Sequencer(object):
    # print debug info
    dbg = 0
    #
    # this is the time resolution (its a bit optimistic, even more on windows)
    _TIME_RES = 0.001
    # sequencer speed: beats per minute
    BPM = 120
    # number of beats in the sequence
    BEAT_NUM = 4
    # number of sub-steps into a single beat
    BEAT_DIV = 64
    
    def __init__(self):
        # sequence basic beat / time parameters
        self.BPM = Sequencer.BPM
        self.BEAT_NUM = int(Sequencer.BEAT_NUM)
        self.BEAT_DIV = int(Sequencer.BEAT_DIV)
        # EVENT_GRID is a dict of
        # objects (that have a .play() method) : list of beat (when object needs to be played)
        # e.g. {Sound('test1.wav'):[0, 1.5, 2.5], {Sound('test2.wav'):[1, 3.05]}
        self.EVENT_GRID = {}
        self.update_internals()
        # ensure sequencer is stopped... who knows !
        self._running = False
        self._seq_cnt = 0
        
    def _build_step_grid(self):
        # revert the EVENT_GRID to a STEP_GRID
        # init with an empty EVENT_GRID
        STEP_GRID = {}
        for s in range(self.BEAT_NUM * self.BEAT_DIV):
            STEP_GRID[s] = []
        # fill in with events from the EVENT_GRID
        for evt in self.EVENT_GRID.keys():
            for beat in self.EVENT_GRID[evt]:
                step = int(beat * self.BEAT_DIV)
                if STEP_GRID.__contains__(step):
                    STEP_GRID[step].append( evt )
        return STEP_GRID
    
    def update_internals(self):
        self.SEQ_DUR = int(self.BEAT_NUM) * float(60.0 / self.BPM)
        self.STEP_DUR = float(60.0 / (self.BPM * self.BEAT_DIV))
        self.STEP_GRID = self._build_step_grid()
        
    def start(self):
        # start the sequencer, backgrounding ._run()
        self._running = True
        threadit(self._run, ())
    
    def stop(self):
        # stop the running loop in ._run()
        self._running = False
    
    def is_running(self):
        return bool(self._running)
    
    def _run(self):
        # this is the backgrounded loop
        # do not call it directly
        print('[+] sequencer started')
        while self._running:
            self.play_sequence()
        print('[+] sequencer stopped')
    
    def play_sequence(self):
        if self.dbg > 0:
            print('[+] playing sequence %i' % self._seq_cnt)
        # recompute sequence and step durations, and STEP_GRID
        self.update_internals()
        # initialize the list of played steps
        self._step_played = [0]
        # ensure we respect sequence duration
        T0 = time()
        # launch step 0, and loop over all subsequent steps
        threadit(self.play_step, (0,))
        while time() - T0 < self.SEQ_DUR:
            # go over the STEP_GRID step by step, on time
            # 1) check in which step we are
            step = int((time()-T0) / self.STEP_DUR)
            # 2) play all steps that are not yet played
            for s in range(self._step_played[-1]+1, step+1):
                threadit(self.play_step, (s,))
                self._step_played.append(s)
            # 3) sleep to wait until next step
            sleep(self._TIME_RES)
        # reinit internal attribute
        self._step_played = []
        # update sequence counter
        self._seq_cnt += 1
    
    def play_step(self, step=0):
        if self.dbg > 1:
            print('time %f :: step %i' % (time(), step))
        # go over all event from the STEP_GRID
        for evt in self.STEP_GRID[step]:
            if hasattr(evt, 'run'):
                evt.run()


# testing program non-interactively
def test(num=4):
    s = Sequencer()
    s.BEAT_NUM = 8
    s.EVENT_GRID = {
        Sound('tamtam_1.wav') : [0, 2, 4, 6], 
        Sound('percviet_6.wav') : [1, 3, 5.25, 5.5, 7],
        Sound('guiro_4.wav') : [2.5, 6.5],
        Sound('djembe_2.wav') : [0.75, 2.75, 4.5, 6.5, 7.25]
        }
    s.start()
    sleep(0.1)
    try:
        sleep(s.SEQ_DUR * num)
    except KeyboardInterrupt:
        s.stop()
    s.stop()
    sleep(0.1)
    return s

