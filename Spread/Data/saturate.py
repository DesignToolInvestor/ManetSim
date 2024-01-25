#
# s a t u r a t e . p y
#

# This script will increase the number of streams passed the point of saturating aggregate flow.

# system packages
import argparse
from datetime import datetime, timedelta
import math
import random

# local libraries
import LocMath
import LocUtil
import Log
import MakeNet
import MaxFlow
import NetPath


###########################################################
def Info2Line(nNode,r,netSeed, numStream,streamSeed,flowFrac,agFlow, time):
    netInfo = f'[{nNode}, {r} ,{netSeed}]'
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

    # core parse
    args = parser.parse_args()
    
    # check and fix network size parameters
    n,r,rho = MakeNet.ParseParams(args.n, args.r, args.rho)
    if (n < 10):
        raise Exception('Network size is small enough to likely be an error')

    # convert duration argument
    asDate = datetime.strptime(args.delta, "%H:%M:%S")
    asDelta = (timedelta(hours=asDate.hour, minutes=asDate.minute, seconds=asDate.second))
    asSec = asDelta.total_seconds()

    # return result
    return [args.fileName, asSec, n, r, rho]

###########################################################
if __name__ == '__main__':
    # constants
    escPerNet = 1
    
    logDelay = 60
    numSeedDig = 3

    # parse args
    fileName,duration, netSize,r,rho = ParseArgs()
    maxNumStream = round(math.sqrt(netSize))

    # creat log
    log = Log.Log(fileName, logDelay)

    # main loop
    progStartTime = datetime.now()
    
    numNet = 0;
    while ((datetime.now() - progStartTime).total_seconds() < duration):
        # make network
        netSeed = LocUtil.SetSeed()
        net = MakeNet.RandNetCirc(netSize, r, dir=True)

        # extract the dominant subnet as a network
        subNet = NetPath.DomCompSubNet(net)
        nodeLoc,link = subNet
        nSubNet = len(nodeLoc)

        # do the escalations on this network
        for escalation in range(escPerNet):
            streamSeed = LocUtil.SetSeed()

            stream = [random.sample(range(nSubNet), 2) for _ in range(maxNumStream)]
            endLoc = LocUtil.Index(nodeLoc, stream)
            streamDist = list(map(lambda vec: LocMath.Dist(vec[0],vec[1]), endLoc))

            # escalate the number of streams
            for numStream in range(1, maxNumStream + 1):
                startTime = datetime.now()
                try:
                    maxFlow = MaxFlow.MaxFlowRate(subNet, stream[:numStream])
                except:
                    print(f"{numNet}, {escalation}, {numStream}: Couldn't Solve")
                    break

                endTime = datetime.now()
                solveTime = (endTime - startTime).total_seconds()

                maxFlowFrac = LocMath.RealToFrac(maxFlow)
                agFlow = maxFlow * sum(streamDist[:numStream])

                line = Info2Line(
                    netSize,r,netSeed, numStream,streamSeed,maxFlowFrac,agFlow, solveTime)
                log.Log(line)

                print(f'{numNet}, {escalation}, {numStream}, {solveTime}, '
                      f' {datetime.now() - progStartTime}')

        numNet += 1

    # Need to explicitly delete the log, because automatic deletion sometimes takes down the file
    # system before calling the delete method on Log.  Because the deletion flushes the buffer
    # this can cause a crash.
    del Log
