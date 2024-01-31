#
# s a t u r a t e _ v a r y _ n . p y
#

# This script will increase the number of streams passed the point of saturating aggregate flow.

# system packages
import argparse
from datetime import datetime, timedelta
import random
import time

# local libraries
import LocMath
import LocUtil
import Log
import MakeNet
import MaxFlow
import NetPath
import TaskFarm

# global variable
progStartTime = datetime.now()


###########################################################
def ParseArgs():
    parser = argparse.ArgumentParser(
        prog='saturate_vary_n',
        description='This program will generate a random network over a circular area.'
    )

    # setup
    parser.add_argument('fileName', type=str)
    parser.add_argument('nRange', type=str)
    parser.add_argument('rho', type=float)
    parser.add_argument('delta', type=str)

    parser.add_argument('-nProc', type=int, default=None)

    # core parse
    args = parser.parse_args()

    # nRange
    nRange = eval(args.nRange)

    # convert duration argument
    asDate = datetime.strptime(args.delta, "%H:%M:%S")
    asDelta = (timedelta(hours=asDate.hour, minutes=asDate.minute, seconds=asDate.second))
    asSec = asDelta.total_seconds()

    # return result
    return [args.fileName, nRange, args.rho, asSec, args.nProc]


###########################################################
# This function returns a task-result if successful and the list [solver-status, time] if the
# solver failed.
def Task(netInfo, streamIndo):
    [netSize, rho, netSeed] = netInfo
    [nStream, streamSeed] = streamIndo

    # make network
    LocUtil.SetSeed(netSeed)
    r = MakeNet.R(netSize, rho)
    net = MakeNet.RandNetCirc(netSize, r, dir=True)

    # extract the dominant subnet as a network
    subNet = NetPath.DomCompSubNet(net)
    nodeLoc, link = subNet
    nSubNet = len(nodeLoc)

    # select streams
    LocUtil.SetSeed(streamSeed)
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
        maxFlowFrac = LocMath.RealToFrac(float(maxFlow))

        endLoc = LocUtil.Index(nodeLoc, stream)
        cumDist = sum(map(lambda vec: LocMath.Dist(vec[0], vec[1]), endLoc))

        return [[netSize, rho, netSeed], [nStream, streamSeed], [maxFlowFrac, cumDist, timeSec]]


###########################################################
def Info2Line(netSize, rho, netSeed, nStream, streamSeed, flowFrac, cumDist, time):
    netInfo = f'[{netSize}, {rho}, {netSeed}]'
    streamInfo = \
        f'[{nStream}, {streamSeed}, {flowFrac.numerator}/{flowFrac.denominator}, {cumDist}]'
    result = f'[{netInfo}, {streamInfo}, {time}]'

    return result


###############################
def IsFailTyep(obj):
    return \
        (isinstance(obj, list) and (len(obj) == 2) and
         (isinstance(obj[0], str) and isinstance(obj[1], float)))


###############################
def ProcessResults(taskResult, log):
    if IsFailTyep(taskResult):
        print(f'{datetime.now() - progStartTime}: fail')

    elif taskResult is not None:
        taskInfo, taskId = taskResult
        [netSize,rho,netSeed], [nStream,streamSeed], [maxFlowFrac,cumDist,timeSec] = taskInfo

        line = Info2Line(netSize, rho, netSeed, nStream, streamSeed, maxFlowFrac, cumDist, timeSec)
        log.Log(line)


###########################################################
if __name__ == '__main__':
    # constants
    escPerNet = 1

    minNumStream = 1
    maxNumStream = 16

    logDelay = 60

    masterSeed = None
    numSeedDig = 5

    # parse args
    fileName,nRange,rho,duration,nProc = ParseArgs()

    # create log
    log = Log.Log(fileName, logDelay)

    # set up
    masterSeed = LocUtil.SetSeed(masterSeed, digits=numSeedDig)
    print(f'master masterSeed = {masterSeed}')

    taskFarm = TaskFarm.TaskFarm(Task, nProc)

    # main loop
    netNum = 0
    done = False

    while not done:
        netSize = round(LocMath.RandLog(*nRange))

        netSeed = random.randint(0, 10 ** numSeedDig - 1)
        netTask = [netSize, rho, netSeed]

        escNum = 0
        while (escNum < escPerNet) and not done:
            streamSeed = random.randint(0, 10 ** numSeedDig - 1)

            nStream = minNumStream
            while (nStream <= maxNumStream) and not done:
                taskId = [netNum, escNum, nStream]
                taskArgs = [netTask, [nStream, streamSeed]]
                taskResult = taskFarm.StartTask(taskId, taskArgs)

                ProcessResults(taskResult, log)
                done = ((datetime.now() - progStartTime).total_seconds() > duration)

                nStream += 1

            escNum += 1
        netNum += 1

    # wait for all the processes to finish
    taskResult = taskFarm.DrainTask()
    while taskResult != None:
        ProcessResults(taskResult, log)
        taskResult = taskFarm.DrainTask()

    log.Flush()
