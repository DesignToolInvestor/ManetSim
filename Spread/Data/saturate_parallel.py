#
# s a t u r a t e _ p a r a l l e l . p y
#

# This script will increase the number of streams passed the point of saturating aggregate flow.

# system packages
import argparse
from concurrent import futures
from datetime import datetime, timedelta
import math
import os
import random
import time
from multiprocessing import pool

# local libraries
import LocMath
import LocUtil
import Log
import MakeNet
import MaxFlow
import NetPath

# global variable
progStartTime = datetime.now()

###########################################################
def ParseArgs():
    parser = argparse.ArgumentParser(
        prog='RandNetCirc',
        description='This program will generate a random network over a circular area.'
    )

    # setup
    parser.add_argument('fileName', type=str)
    parser.add_argument('delta', type=str)

    parser.add_argument('-n', type=int)
    parser.add_argument('-r', type=float)
    parser.add_argument('-rho', type=float)
    parser.add_argument('-nProc', type=int)

    # core parse
    args = parser.parse_args()

    # check and fix network size parameters
    n, r, rho = MakeNet.ParseParams(args.n, args.r, args.rho)
    if (n < 10):
        raise Exception('Network size is small enough to likely be an error')

    # convert duration argument
    asDate = datetime.strptime(args.delta, "%H:%M:%S")
    asDelta = (timedelta(hours=asDate.hour, minutes=asDate.minute, seconds=asDate.second))
    asSec = asDelta.total_seconds()

    # fix number of processes
    if args.nProc is None:
        nProc = os.cpu_count() - 1
    else:
        nProc = args.nProc

    # return result
    return [args.fileName,asSec, n,r,rho, nProc]


###########################################################
def Info2Line(netSize, rho, netSeed, nStream, strSeed, flowFrac, cumDist, time):
    netInfo = f'[{netSize}, {rho}, {netSeed}]'
    streamInfo = \
        f'[{nStream}, {strSeed}, {flowFrac.numerator}/{flowFrac.denominator}, {cumDist}]'
    result = f'[{netInfo}, {streamInfo}, {time}]'

    return result


###########################################################
# This function returns a task-result if successful and the list [solver-status, time] if the
# solver failed.
def Task(taskInfo):
    [netSize, rho, netSeed], [nStream, strSeed] = taskInfo
    
    # make network
    LocUtil.SetSeed(netSeed)
    r = MakeNet.R(netSize, rho)
    net = MakeNet.RandNetCirc(netSize, r, dir=True)

    # extract the dominant subnet as a network
    subNet = NetPath.DomCompSubNet(net)
    nodeLoc, link = subNet
    nSubNet = len(nodeLoc)

    # select streams
    LocUtil.SetSeed(strSeed)
    stream = [random.sample(range(nSubNet), 2) for _ in range(nStream)]

    # call MaxFlowRate and catch solver error
    startTime = datetime.now()
    try:
        maxFlow = MaxFlow.MaxFlowRate(subNet, stream)
        timeSec = (datetime.now() - startTime).total_seconds()
        
    except Exception as exception:
        if exception.args[0] == 'solver failure':
            timeSec = (datetime.now() - startTime).total_seconds()
            return [exception.args[1], timeSec]
        else:
            raise Exception("solver failure") from exception
        
    else:
        maxFlowFrac = LocMath.RealToFrac(maxFlow)

        endLoc = LocUtil.Index(nodeLoc, stream)
        cumDist = sum(map(lambda vec: LocMath.Dist(vec[0], vec[1]), endLoc))

        return [[netSize,rho,netSeed], [nStream,strSeed], [maxFlowFrac,cumDist, timeSec]]


###########################################################
def IsFailTyep(obj):
    return \
        (isinstance(obj, list) and (len(obj) == 2) and
         (isinstance(obj[0], str) and isinstance(obj[1], float)))

###########################################################
# TODO:  replace busy wait with IPC about which process is finishing
def StartTask(taskInfo, proc):
    # constants
    sleepTime = 0.1
    
    # wait for free proc
    procId = LocUtil.IndexOfFirst(lambda info: (info is None) or info.done(), proc)
    while procId is None:
        time.sleep(sleepTime)
        procId = LocUtil.IndexOfFirst(lambda info: (info is None) or info.done(), proc)

    # get results
    if proc[procId] is None:
        taskResult = None
    else:
        taskResult = proc[procId].result()

        if IsFailTyep(taskResult):
            taskResult = None
        else:
            netSeed = taskResult[0][2]
            nStream = taskResult[1][0]
            timeSec = taskResult[2][2]
            totalTime = datetime.now() - progStartTime
            print(f'{totalTime}:  Completed task ({netSeed}, {nStream}) on proc {procId} '
                  f'in {timeSec} seconds')

    # start new task
    proc[procId] = pool.submit(Task, taskInfo)

    netSeed = taskInfo[0][2]
    nStream = taskInfo[1][0]
    print(f'Start task ({netSeed}. {nStream}) on proc {procId}')

    return taskResult


###########################################################
def DrainTask(proc):
    # constants
    sleepTime = 0.1

    # look for done tasks
    procId = LocUtil.IndexOfFirst(lambda info: (info is not None) and info.done(), proc)
    while procId is None:
        time.sleep(sleepTime)
        procId = LocUtil.IndexOfFirst(lambda info: (info is not None) and info.done(), proc)

    # get results
    # TODO:  fix code reuse issue
    taskResult = proc[procId].result()
    netSeed = taskResult[0][2]
    nStream = taskResult[1][0]
    timeSec = taskResult[2][2]

    totalTime = datetime.now() - progStartTime
    print(f'{totalTime}:  Completed task ({netSeed}, {nStream}) on proc {procId} '
          f'in {timeSec} seconds')
    
    # remove entry from process table
    proc[procId] = None

    return taskResult


###############################
def ProcessResults(taskResult, log):
    if IsFailTyep(taskResult):
        print(f'{datetime.now() - progStartTime}: fail')

    elif taskResult is not None:
        [netSize, rho, netSeed], [nStream, strSeed], [maxFlowFrac, cumDist, timeSec] = taskResult

        line = Info2Line(netSize, rho, netSeed, nStream, strSeed, maxFlowFrac, cumDist, timeSec)
        log.Log(line)

    
###########################################################
if __name__ == '__main__':
    # constants
    escPerNet = 2

    logDelay = 60
    numSeedDig = 5

    masterSeed = None
    # masterSeed = 26

    # parse args
    fileName,duration, netSize,r,rho, nProc = ParseArgs()
    # maxNumStream = round(math.sqrt(netSize))
    minNumStream = 13
    maxNumStream = 16

    # create log
    log = Log.Log(fileName, logDelay)

    # main loop
    masterSeed = LocUtil.SetSeed(masterSeed, digits=numSeedDig)
    print(f'master masterSeed = {masterSeed}')

    proc = [None for _ in range(nProc)]

    with futures.ProcessPoolExecutor(max_workers=nProc) as pool:
        netNum = 0
        done = False

        while not done:
            netSeed = random.randint(0, 10**numSeedDig - 1)
            netTask = [netSize,rho,netSeed]
            
            escNum = 0
            while (escNum < escPerNet) and not done:
                strSeed = random.randint(0, 10**numSeedDig - 1)
                
                nStream = minNumStream
                while (nStream <= maxNumStream) and not done:
                    taskInfo = [netTask, [nStream, strSeed]]
                    taskResult = StartTask(taskInfo, proc)
                    
                    ProcessResults(taskResult, log)
                    done = ((datetime.now() - progStartTime).total_seconds() > duration)

                    nStream += 1
                escNum += 1
            netNum += 1

    # wait for all the processes to finish
    done = all((p is None) for p in proc)
    while not done:
        taskResult = DrainTask(proc)
        ProcessResults(taskResult, log)

        done = all((p is None) for p in proc)

    log.Flush()
