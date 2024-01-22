#
# L o g . p y
#

# This is an object for writing log information to a file.

from datetime import datetime
from logging import info


class Log(object):
    def __init__(self, fileName, delay, trace=False):
        self.fileName = fileName
        self.delay = delay
        self.trace = trace

        self.lastDump = datetime.now()
        self.buff = []

    def Log(self, line):
        self.buff.append(line)
        if (datetime.now() - self.lastDump).total_seconds() > self.delay:
            with open(self.fileName, 'a') as file:
                for line in self.buff:
                    file.write(f'{line}\n')
                if self.trace:
                    file.write(f'--------------\n')

            self.buff.clear()
            self.lastDump = datetime.now()

    def __del__(self):
        with open(self.fileName, 'a') as file:
            for line in self.buff:
                file.write(f'{line}\n')
            if self.trace:
                file.write(f'--------------\n')