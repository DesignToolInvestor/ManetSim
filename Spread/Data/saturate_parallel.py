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

# local libraries
import LocMath
import LocUtil
import Log
import MakeNet
import MaxFlow
import NetPath

# constants
sleepTime = 0.1

###########################################################
def Info2Line(nNode, rho, netSeed, numStream, streamSeed, flowFrac, agFlow, time):
    netInfo = f'[{nNode}, {rho} ,{netSeed}]'
    streamInfo = \
        f'[{numStream}, {streamSeed}, {flowFrac.numerator}/{flowFrac.denominator}, {agFlow}]'
    result = f'[{netInfo}, {streamInfo}, {time}]'

    return result


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
def MaxFlowTask(net,stream,taskInfo):
    maxFlow = MaxFlow.MaxFlowRate(net,stream)
    return [maxFlow, taskInfo]


def StartTask(subNet, stream, proc, taskInfo):
    # wait for free proc
    # TODO:  replace busy wait with IPC about which process is finishing
    procId = 0
    while (procId < len(proc)) and ((proc[procId] is None) or (not proc[procId].done())):
        procId += 1

    while procId is len(proc):
        time.sleep(sleepTime)

        procId = 0
        while (procId < len(proc)) and ((proc[procId] is None) or (not proc[procId].done())):
            procId += 1

    # get results
    if proc[procId] is not None:
        taskResult = proc[procId].result()
    else:
        taskResult = None

    # start next task
    proc[procId] = pool.submit(MaxFlowTask, subNet, stream, taskInfo)
    print(f'Start task {taskInfo} on proc {procId}')

    return taskResult


###########################################################
if __name__ == '__main__':
    # constants
    escPerNet = 1

    logDelay = 60
    numSeedDig = 3

    # parse args
    fileName,duration, netSize,r,rho, nProc = ParseArgs()
    maxNumStream = round(math.sqrt(netSize))

    # creat log
    log = Log.Log(fileName, logDelay)

    # main loop
    # TODO:  This is very poorly structured code
    progStartTime = datetime.now()

    proc = [None for _ in range(nProc)]
    with (futures.ProcessPoolExecutor(max_workers=nProc) as pool):
        numNet = 0
        while ((datetime.now() - progStartTime).total_seconds() < duration):
            # make network
            netSeed = LocUtil.SetSeed()
            net = MakeNet.RandNetCirc(netSize, r, dir=True)

            # extract the dominant subnet as a network
            subNet = NetPath.DomCompSubNet(net)
            nodeLoc, link = subNet
            nSubNet = len(nodeLoc)

            # do the escalations on this network
            for escalation in range(escPerNet):
                streamSeed = LocUtil.SetSeed()

                stream = [random.sample(range(nSubNet), 2) for _ in range(maxNumStream)]
                endLoc = LocUtil.Index(nodeLoc, stream)
                streamDist = list(map(lambda vec: LocMath.Dist(vec[0], vec[1]), endLoc))

                # escalate the number of streams
                for numStream in range(1, maxNumStream + 1):
                    startTime = datetime.now()
                    try:
                        taskStream = stream[:numStream]
                        taskInfo = [[netSize,rho,netSeed], [taskStream,streamSeed]]
                        [maxFlow,solveTime],taskInfo = StartTask(subNet, str, proc, taskInfo)
                    except:
                        print(f"{numNet}, {escalation}, {numStream}: Couldn't Solve")
                        break

                    # stuff extracted from taskInfo
                    maxFlowFrac = LocMath.RealToFrac(maxFlow)

                    # all for lost tasks
                    [netSize,rho,netSeed], [taskStream,streamSeed] = taskInfo
                    nStream = len(taskStream)
                    agFlow = maxFlow * sum(LocUtil.Index(streamDist, taskStream))

                    line = Info2Line(
                        netSize, rho, netSeed, nStream, streamSeed, maxFlowFrac, agFlow,
                        solveTime)
                    log.Log(line)

                    print(f'{numNet}, {escalation}, {numStream}, {solveTime}, '
                          f' {datetime.now() - progStartTime}')

        numNet += 1

    # wait for all the processes to finish
    done = all(((p is None) or p.done()) for p in proc)
    while not done:
        for k in range(nProc):
            if (proc[k] is not None) and proc[k].done():
                [maxFlow,solveTime],taskInfo = proc[k].result()

                maxFlowFrac = LocMath.RealToFrac(maxFlow)

                # all for lost tasks
                [netSize, rho, netSeed], [taskStream, streamSeed] = taskInfo
                nStream = len(taskStream)
                agFlow = maxFlow * sum(LocUtil.Index(streamDist, taskStream))

                line = Info2Line(
                    netSize, rho, netSeed, nStream, streamSeed, maxFlowFrac, agFlow,
                    solveTime)
                log.Log(line)

                print(f'{numNet}, {escalation}, {numStream}, {solveTime}, '
                      f' {datetime.now() - progStartTime}')

        time.sleep(sleepTime)

    # Need to explicitly delete the log, because automatic deletion sometimes takes down the file
    # system before calling the delete method on Log.  Because the deletion flushes the buffer
    # this can cause a crash.
    del Log
