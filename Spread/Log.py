#
# L o g . p y
#

# This is an object for writing log information to a file.

from datetime import datetime


# TODO:  originally flushed on deletion, but sometimes the file system was "unloaded"
class Log(object):
    def __init__(self, fileName, epicLen, trace=False):
        self.fileName = fileName
        self.epicLen = epicLen
        self.trace = trace

        self.startTime = datetime.now()
        self.flushEpic = 0
        self.buff = []

    def Log(self, line):
        self.buff.append(line)

        epic = (datetime.now() - self.startTime).total_seconds() / self.epicLen
        assert(self.flushEpic <= epic)

        if (self.flushEpic < epic):
            with open(self.fileName, mode='a') as file:
                Log.Flush(self)
            self.flushEpic = epic

    def Flush(self):
        with open(self.fileName, mode='a') as file:
            for line in self.buff:
                file.write(f'{line}\n')
            if self.trace:
                file.write(f'--------------\n')

        self.buff.clear()
        self.lastFlush = datetime.now()
 
