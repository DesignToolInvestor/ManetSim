#
# S t o p W a t c h . p y
#

from datetime import datetime, timedelta

# TODO:  create unit tests
class StopWatch(object):
    def __init__(self, running=False):
        self.running = running
        self.cumSec = 0

        if running:
            self.start = datetime.now()

    def Start(self):
        if not self.running:
            self.start = datetime.now()
            self.running = True

    def Stop(self):
        if self.running:
            stop = datetime.now()
            self.cumSec += (stop - self.start).total_seconds()

        return self.cumSec

    def Seconds(self):
        if self.running:
            now = datetime.now()
            return (now - self.start).total_seconds()
        else:
            return self.cumSec

    def Delta(self):
        if self.running:
            now = datetime.now()
            return (now - self.start)
        else:
            return timedelta(seconds=self.cumSec)

    def Reset(self):
        if self.running:
            self.start = datetime.now()
        self.cumSec = 0

        return self