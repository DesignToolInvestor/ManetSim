#
# g e n _ c l i q u e .p y
#

# system packages
import argparse
from datetime import timedelta
from random import sample

# open source packages
from engineering_notation import EngNumber as EngrNum

# local library files
from BestPath import BestPath
from Cost import MetricCostF
from CliquePrune import Clique
from LocUtil import DebugMode, SetSeed, Sub
from LocMath import Dist, RealToFrac
from Log import Log
from MakeNet import RandNetCirc, NetR
from Interfere import PathSelfInter
from StopWatch import StopWatch


#######################################
def ParseArgs():
    parser = argparse.ArgumentParser(
        prog='gen_clique',
        description='This program will generate maximum clique size interference best paths'
    )

    parser.add_argument('metric', type=str)

    parser.add_argument('-folder', type=str, default="")
    parser.add_argument('-nSamp', type=int, default=100)

    parser.add_argument('-n', type=int, default=300)
    parser.add_argument('-rho', type=float, default=2.0)

    parser.add_argument('-gamma', type=float, default=2.0)
    parser.add_argument('-snirDb', type=float, default=0)

    # parse args
    args = parser.parse_args()

    # deal with metric
    costF,metric = MetricCostF(args.metric, args.gamma, args.snirDb)

    # return results
    return [metric, args.folder, args.nSamp, args.n, args.rho, args.gamma, args.snirDb, costF]


#######################################################
if __name__ == "__main__":
    # constants
    logDelay = 60

    maxNumHop = 80
    maxSysSize = 50e3

    fileNameMask = '%s_%d_%d.log'

    # parse arguments
    metric,folder, numSamp,nNode, rho,gamma,snirDb, costF = ParseArgs()
    flowPerNet = round(nNode/10)

    # start the clock
    totalTime = StopWatch(running=True)
    
    # setup log
    fileName = f'{folder}/{fileNameMask%(metric[0],nNode,rho)}'
    log = Log(fileName, logDelay)
    
    # do loop
    sampNum = 0
    while sampNum < numSamp:
        # deal with seed
        seed = SetSeed()

        # create network and pick flows (before random sequence is lost)
        r = NetR(nNode, rho)
        net = RandNetCirc(nNode, r)
        nodeLoc,link = net
        nNode = len(nodeLoc)

        # compute link costs
        linkCost = [costF(nodeLoc[n0], nodeLoc[n1]) for (n0, n1) in link]

        # network info for logging
        netInfoStr = f'[{nNode}, {rho}, {seed}]'

        # do each flow
        # TODO:  error handling is out of control ... think about what to do about it
        flowNum = 0
        while (flowNum < flowPerNet) and (sampNum < numSamp):
            # pick a flow
            flow = sample(range(nNode), 2)
            dist = Dist(*Sub(nodeLoc, flow))

            # find the best path
            path = BestPath(net, *flow, linkCost)
            nHop = len(path) - 1 if (path != None) else 0

            print(f'{sampNum}:  {nHop}', end='')

            # do flow infor for logging
            flowInfoStr = f'[{nHop}, {flow}, {dist:.5e}]'

            # if path found generate rest of log
            if nHop == 0:
                print()

            else:
                if maxNumHop < nHop:
                    print(f', ** skiped **')
                    resultInfoStr = f'None'

                else:
                    # TODO:  refactor code so that this isn't computed twice (robustness)
                    snir = 10 ** (snirDb / 20)
                    graph = (nHop, PathSelfInter(net, path, gamma, snir))

                    timer = StopWatch(running=True)
                    clique = Clique(graph)
                    setUpTime = timer.Stop()

                    nClique = len(clique)
                    print(f', {EngrNum(nClique)}', end='')

                    maxClique = max(map(len, clique))

                    # report results
                    print(f', {maxClique}, {timedelta(seconds=setUpTime)}')
                    resultInfoStr = \
                        f'[{nClique}, {maxClique}, {setUpTime:.5e}]'

                    sampNum += 1

                if not DebugMode():
                    logLine = f'[{netInfoStr}, {flowInfoStr}, {resultInfoStr}]'
                    log.Log(logLine)

            flowNum += 1

    log.Flush()