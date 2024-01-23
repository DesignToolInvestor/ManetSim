#
# t i m e _ i n d e x _ p o o l . p y
#

# system imports
from datetime import datetime
import enum
import math
import random

# local imports
import IndexPool
from LocMath import Sqr, RandLog
import Log
import LocUtil


OpT = enum.Enum('OpT', ('ADD', 'DROP'))

def BuildTest(indexSize, fracMaxActive):
    addL = [k for k in range(indexSize)]
    random.shuffle(addL)

    H = fracMaxActive
    DropTime = lambda y: (4*H - 1 + math.sqrt(Sqr(4*H - 1) + 16*H*y)) / (8*H)
    dropTime = [indexSize * DropTime((k + 0.5) / indexSize) for k in range(indexSize)]

    indexPool = IndexPool.IndexPool(indexSize)
    nextDropIndex = 0

    result = []
    for i in range(indexSize):
        indexPool.Push(addL[i])
        result.append([OpT.ADD, addL[i]])

        while (nextDropIndex < indexSize) and (dropTime[nextDropIndex] < (i + 1)):
            dropIndex = indexPool.pool[random.randint(0, indexPool.Len() - 1)]
            indexPool.Drop(dropIndex)
            nextDropIndex += 1
            result.append([OpT.DROP, dropIndex])

    assert(indexPool.Len() == 0)

    return result


def DoTest(indexSize, opL):
    indexPool = IndexPool.IndexPool(indexSize)

    # do test
    startTime = datetime.now()
    for i in range(len(opL)):
        op, index = opL[i]
        # print(f'op: {op}, index: {index}')

        if op == OpT.ADD:
            indexPool.Push(index)
        else:
            indexPool.Drop(index)
    endTime = datetime.now()

    return endTime - startTime


if __name__ == '__main__':
    # constants
    MIN_SIZE = 1_000
    MAX_SIZE = 1_000_000
    NUM_SAMP = 300

    FILE_NAME = "index_pool.log"

    # random index sizes
    seed = LocUtil.SetSeed()
    indexSize = [round(RandLog(MIN_SIZE,MAX_SIZE)) for _ in range(NUM_SAMP)]

    # build test
    log = Log.Log(FILE_NAME, 10)
    for n in indexSize:
        opL = BuildTest(n, 1/4)
        delta = DoTest(n, opL)

        info = [n, delta.total_seconds()]
        log.Log(str(info))