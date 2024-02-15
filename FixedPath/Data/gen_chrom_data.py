#
# g e n _ c h r o m _ d a t a .p y
#

# system packages
import argparse
from datetime import datetime, timedelta
from matplotlib import pyplot as plot
from random import sample

# local library files
from BestPath import BestPath
from Cost import MetricArg
from FracChromNum import FracChromNum
from LocUtil import DebugMode, SetSeed, Sub
from LocMath import Dist, RealToFrac
from Log import Log
import MakeNet
from MakeNet import RandNetCirc
from Interfere import PathSelfInter
from StopWatch import StopWatch
from Visual import GraphBiNet

# special packages
from IndependPrune import IndSubSet
# from IndependSlow import IndSubSet

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
    parser.add_argument('-flow', type=str)
    parser.add_argument('-gamma', type=float, default=2.0)
    parser.add_argument('-snirDb', type=float, default=0)

    # parse args
    args = parser.parse_args()

    # deal with metric
    costF,metric = MetricArg(args.metric, args.gamma, args.snirDb)

    # deal with flow
    flow = eval(args.flow) if args.flow is not None else None

    # return results
    return [args.fileName, costF, metric, args.n, args.rho, flow, args.gamma, args.snirDb]


#######################################################
if __name__ == "__main__":
    # constants
    timeLim = "0:05:00"
    masterSeed = None
    logDelay = 60

    maxPathLen = 23

    # parse arguments
    fileName,costF,metric,nNode,rho,flow,gamma,snirDb = ParseArgs()
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

        # select all the flows at once
        if flow is None:
            flow = [sample(range(nNode), 2) for _ in range(flowPerNet)]

        dist = [Dist(*Sub(nodeLoc, f)) for f in flow]

        # for debugging only
        # fig,ax = plot.subplots(figsize=(6.5, 6.5))
        # GraphBiNet(ax,net)
        # plot.show()
        # plot.close()

        # compute link costs
        linkCost = [costF(nodeLoc[n0], nodeLoc[n1]) for (n0, n1) in link]

        # log string
        netInfoStr = f'[{nNode}, {rho}, {seed}]'
        
        # do each flow
        flowNum = 0
        while (flowNum < len(flow)) and (totalTime.Seconds() < limInSec):
            path = BestPath(net, *flow[flowNum], linkCost)
            nHop = len(path) - 1 if (path != None) else 0

            flowInfoStr = f'[{nHop}, {flow[flowNum]}, {dist[flowNum]}]'

            if 0 < nHop:
                if maxPathLen < nHop:
                    resultInfoStr = 'None'
                    print(f'{totalTime.Delta()}:  {netNum}, {flowNum}, {nHop}, ** skipped **')

                else:
                    print(f'{totalTime.Delta()}:  {netNum}, {flowNum}, {nHop}', end='')

                    snir = 10 ** (snirDb / 20)
                    graph = (nHop, PathSelfInter(net, path, gamma, snir))

                    timer = StopWatch(running=True)
                    indSubSet = IndSubSet(graph)
                    setUpTime = timer.Stop()

                    nSubSetStr = f'{len(indSubSet):,}'.replace(',', '_')
                    print(f', {nSubSetStr}', end='')

                    rank = max(map(len, indSubSet))
                    print(f', rank={rank}', end='')

                    # might crash on solve ... save previous results
                    if logDelay < setUpTime:
                        log.Flush()
                        print(f'nHops = {nHop}  ==>>  {len(indSubSet)} @ {setUpTime}')

                    timer.Reset().Start()
                    try:
                        result = FracChromNum(nHop, indSubSet)
                    except:
                        resultInfoStr = 'None'
                        print(f', ** failed **')
                    else:
                        solveTime = timer.Stop()

                        chromNum = RealToFrac(sum(result))
                        # chromNum = sum(result)

                        # report results
                        print(f',  {chromNum}')
                        resultInfoStr = f'[{chromNum}, {nSubSetStr}, {setUpTime}, {solveTime}]'

                if not DebugMode():
                    logLine = f'[{netInfoStr}, {flowInfoStr}, {resultInfoStr}]'
                    log.Log(logLine)

            flowNum += 1
        netNum += 1

    log.Flush()