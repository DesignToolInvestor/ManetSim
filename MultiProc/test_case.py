#
# t e s t _ c a s e . p y
#

from multiprocessing import Queue, Process
from math import sqrt, floor
import sys

import TaskFarm

#####################################
# TODO:  Move to LocUtil ... must share between projects
def DebugMode():
    has_trace = hasattr(sys, 'gettrace') and sys.gettrace() is not None
    has_breakpoint = sys.breakpointhook.__module__ != "sys"

    return has_trace or has_breakpoint


#####################################
def nthPrime(nPrime):
    primeL = [2]
    nextNum = 3

    while len(primeL) < nPrime:
        mightBePrime = True
        i = 0

        maxMinFact = floor(sqrt(nextNum))
        while (primeL[i] <= maxMinFact) and mightBePrime:
            if (nextNum % primeL[i]) == 0:
                mightBePrime = False
            i += 1

        if mightBePrime:
            primeL.append(nextNum)

        nextNum += 1

    return primeL[nPrime - 1]


#####################################
if __name__ == '__main__':
    # constants
    numProc = 3
    numCycle = 4

    if DebugMode():
        baseNum = [20_000, 30_000, 50_000]
    else:
        baseNum = [100_000, 200_000, 300_000]

    # setup
    taskFarm = TaskFarm.TaskFarm(nthPrime, numProc)

    # start tasks
    result = [None for _ in range(numCycle * numProc)]
    for cycle in range(numCycle):
        for job in range(numProc):
            taskId = [cycle, job]
            taskResult = taskFarm.StartTask(taskId, [baseNum[job]])
            print(f'{taskId} started')

            if taskResult != None:
                res, oldTaskId = taskResult
                [oldCycle, oldJob] = oldTaskId
                resIndex = oldCycle * numProc + oldJob
                result[resIndex] = res

                print(f'{oldTaskId} is done')
                print(f'result[{resIndex}] = {res}')

    # collect results from running tasks
    taskResult = taskFarm.DrainTask()
    while taskResult != None:
        taskResult = taskFarm.DrainTask()
        if taskResult != None:
            res,taskId = taskResult
            [oldCycle, oldJob] = taskId
            resIndex = oldCycle * numProc + oldJob
            result[resIndex] = res

            print(f'{taskId} is done')
            print(f'result[{resIndex}] = {res}')

    # "check" result
    print(result)