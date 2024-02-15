#
# s e t _ l i k e . p y
#

# This script times various fundamental operations that can be used to build a set-like ADT
# (Abstract Data Type).  The core need is to be able to check that an element is in a set.

from math import sqrt
from random import randint

from StopWatch import StopWatch
from LocUtil import BinIn, DebugMode, SetSeed
from LocMath import RandLog
from Log import Log


#########################################################################
def ListTest(setSize, numLim, nSearch):
    testSet = [(randint(0, numLim), randint(0, numLim)) for _ in range(setSize)]
    searchCases = [(randint(0, numLim), randint(0, numLim)) for _ in range(nSearch)]

    timer = StopWatch(running=True)
    hit = 0
    for test in searchCases:
        if test in testSet:
            hit += 1
    timer.Stop()

    return (timer.Seconds(),hit)

def SetTest(setSize, numLim, nSearch):
    testSet = {(randint(0, numLim), randint(0, numLim)) for _ in range(setSize)}
    searchCases = [(randint(0, numLim), randint(0, numLim)) for _ in range(nSearch)]

    timer = StopWatch(running=True)
    hit = 0
    for test in searchCases:
        if test in testSet:
            hit += 1
    timer.Stop()

    return (timer.Seconds(), hit)


def SortTest(setSize, numLim, nSearch):
    testSet = sorted([(randint(0, numLim), randint(0, numLim)) for _ in range(setSize)])
    searchCases = [(randint(0, numLim), randint(0, numLim)) for _ in range(nSearch)]

    timer = StopWatch(running=True)
    hit = 0
    for test in searchCases:
        if BinIn(testSet,test):
            hit += 1
    timer.Stop()

    return (timer.Seconds(), hit)


####################################
if __name__ == "__main__":
    # constants
    setSizeRange = (10, 10_000)
    nSet = 500

    # TODO:  create a command line argument that determines which test is run
    nSearch = 10_000  # for list
    # nSearch = 30_000  # for sorted
    # nSearch = 100_000  # for set

    masterSeed = None
    locDelay = 60

    # pick set sizes
    setSizeL = [round(RandLog(*setSizeRange)) for _ in range(nSet)]

    # loop setup
    log = Log('set_list.log', locDelay)

    # do loop
    for setNum in range(nSet):
        seed = SetSeed()
        setSize = setSizeL[setNum]

        numLim = 2 * round(sqrt(setSize))
        timeSec,hit = ListTest(setSize, numLim, nSearch)
        # timeSec,hit = SetTest(setSize, numLim, nSearch)
        # timeSec,hit = SortTest(setSize, numLim, nSearch)

        timeEach = timeSec/nSearch
        hitRatio = hit/nSearch

        if (setNum % 10) == 9:
            print(f'{setNum}:  SetSize = {setSize}, Time = {timeEach:.2e}, Ratio = {hitRatio:.2f}')

        if not DebugMode():
            setInfo = f'[{setSize}, {seed}]'
            resultInfo = f"['FTD', {hitRatio}, {timeEach}]"
            sampInfo = f'[{setInfo}, {resultInfo}]'

            log.Log(sampInfo)

    log.Flush()
