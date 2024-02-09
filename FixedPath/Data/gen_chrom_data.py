#
# g e n _ c h r o m _ d a t a .p y
#

# system packages
import argparse
from datetime import datetime, timedelta
from random import sample

# local library files
from BestPath import BestPath
import Cost
from FracChromNum import FracChromNum
from LocUtil import DebugMode, SetSeed, Sub
from LocMath import Dist, RealToFrac
from Log import Log
import MakeNet
from MakeNet import RandNetCirc
from IndependPrune import IndSubSet
from Interfere import PathSelfInter
from StopWatch import StopWatch 


#######################################
def ParseArgs():
    parser = argparse.ArgumentParser(
        prog='gen_chrom_data',
        description='This program will generate chromatic number data for best paths'
    )

    parser.add_argument('fileName', type=str)
    parser.add_argument('metric', type=str)

    parser.add_argument('-n', type=int, default=300)
    parser.add_argument('-rho', type=float, default=2.0)
    parser.add_argument('-gamma', type=float, default=2.0)
    parser.add_argument('-snirDb', type=float, default=0)

    # parse args
    args = parser.parse_args()

    # deal with metric
    if args.metric == "sp":
        costF = Cost.R
    elif args.metric == "xr":
        snir = 10 ** (args.snirDb / 20)
        costF = lambda p0,p1: Cost.ExcluR(p0,p1,snir,gamma)
    elif args.metric == "xa":
        snir = 10 ** (args.snirDb / 20)
        costF = lambda p0, p1: Cost.ExcluArea(p0, p1, snir, gamma)
    else:
        raise Exception("Must specify metric.  Either 'sp', 'xr', or 'xa'")

    # return results
    return [args.fileName, costF, args.n, args.rho, args.gamma, args.snirDb]


#######################################################
if __name__ == "__main__":
    # constants
    timeLim = "0:05:00"
    masterSeed = None
    logDelay = 60

    maxPathLen = 24

    # parse arguments
    fileName,costF,nNode,rho,gamma,snirDb = ParseArgs()
    flowPerNet = nNode // 10

    # start the clock
    totalTime = StopWatch(running=True)
    
    # deal with stopping criteria
    if timeLim is not None:
        limAsDate = datetime.strptime(timeLim, "%H:%M:%S")
        limAsDelta = \
            (timedelta(hours=limAsDate.hour, minutes=limAsDate.minute, seconds=limAsDate.second))
        limInSec = limAsDelta.total_seconds()
        
    if masterSeed is not None:
        nNet = len(masterSeed)
    
    # setup log
    log = Log(fileName, logDelay)
    
    # do loop
    netNum = 0
    while ((timeLim == None) or (totalTime.Seconds() < limInSec)) and \
           ((masterSeed == None) or (netNum < nNet)):

        # deal with seed
        if masterSeed is not None:
            seed = SetSeed(masterSeed[netNum])
        else:
            seed = SetSeed()

        # create network and pick flows (before random sequence is lost)
        r = MakeNet.R(nNode, rho)
        net = RandNetCirc(nNode, r)
        nodeLoc,link = net
        nNode = len(nodeLoc)

        flow = [sample(range(nNode), 2) for _ in range(flowPerNet)]
        dist = [Dist(*Sub(nodeLoc, f)) for f in flow]

        # compute link costs
        linkCost = [costF(nodeLoc[n0], nodeLoc[n1]) for (n0, n1) in link]

        # log string
        netInfoStr = f'[{nNode}, {rho}, {seed}]'
        
        # do each flow
        flowNum = 0
        while (flowNum < flowPerNet) and (totalTime.Seconds() < limInSec):
            path = BestPath(net, *flow[flowNum], linkCost)
            nHop = len(path) - 1 if (path != None) else 0

            flowInfoStr = f'[{nHop}, {flow[flowNum]}, {dist[flowNum]}]'

            if 0 < nHop:
                if maxPathLen < nHop:
                    resultInfoStr = 'None'
                    print(f'{totalTime.Delta()}:  {netNum}, {flowNum}, {nHop}, ** skipped **')

                else:
                    snir = 10 ** (snirDb / 20)
                    graph = (nHop, PathSelfInter(net, path, gamma, snir))

                    timer = StopWatch(running=True)
                    indSubSet = IndSubSet(graph)
                    setUpTime = timer.Stop()

                    # might crash on solve ... save previous results
                    if logDelay < setUpTime:
                        log.Flush()
                        print(f'nHops = {nHop}  ==>>  {len(indSubSet)} @ {setUpTime}')

                    timer.Reset().Start()
                    result = FracChromNum(nHop, indSubSet)
                    solveTime = timer.Stop()

                    chromNum = RealToFrac(sum(result))
                    # chromNum = sum(result)

                    # report results
                    print(f'{totalTime.Delta()}:  {netNum}, {flowNum}, {nHop}, {len(indSubSet)},'
                          f' {chromNum}')
                    resultInfoStr = f'[{chromNum}, {setUpTime}, {solveTime}]'

                if not DebugMode():
                    logLine = f'[{netInfoStr}, {flowInfoStr}, {resultInfoStr}]'
                    log.Log(logLine)

            flowNum += 1
        netNum += 1

    log.Flush()