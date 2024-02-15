#
# S t o p W a t c h . p y
#

from time import perf_counter
from datetime import timedelta

# TODO:  create unit tests
class StopWatch(object):
    def __init__(self, running=False):
        self.running = running
        self.cumSec = 0

        if running:
            self.start = perf_counter()

    def Start(self, reset=False):
        if not self.running:
            self.start = perf_counter()
            self.running = True

        if reset:
            self.cumSec = 0

    def Stop(self):
        if self.running:
            stop = perf_counter()
            self.cumSec += stop - self.start

        self.running = False
            
        return self.cumSec

    def Seconds(self):
        if self.running:
            now = perf_counter()
            return now - self.start
        else:
            return self.cumSec

    def Delta(self):
        if self.running:
            now = perf_counter()
            return timedelta(seconds=(now - self.start))
        else:
            return timedelta(seconds=self.cumSec)

    def Reset(self):
        if self.running:
            self.start = perf_counter()
        self.cumSec = 0

        return self