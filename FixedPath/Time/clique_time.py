#
# c l i c k _ t i m e . p y
#

# This program is to test the speed at which all the cliques can be constructed from a link
# graph.

# system files
from random import randint, sample
import argparse

# open source packages
from engineering_notation import EngNumber as EngNum

# local files
from BestPath import BestPath
from Cost import MetricCostF
from Interfere import PathSelfInter
from LocUtil import SetSeed
from Log import Log
from MakeNet import RandNetCirc, NetR
from StopWatch import StopWatch

# special import
from CliquePrune import Clique
from CliqueSlow import Clique

#######################################
def ParseArgs():
    parser = argparse.ArgumentParser(
        prog='clique_time',
        description='This script will measure the time it takes to construct all the cliques.'
    )

    parser.add_argument('fileName', type=str)
    parser.add_argument('metric', type=str)

    parser.add_argument('-nNet', type=int, default=100)
    parser.add_argument('-nNode', type=int, default=500)

    parser.add_argument('-rho', type=int, default=2.0)
    parser.add_argument('-gamma', type=float, default=2.0)
    parser.add_argument('-snirDb', type=float, default=0.0)

    # parse args
    args = parser.parse_args()

    # deal with metric
    costF, metric = MetricCostF(args.metric, args.gamma, args.snirDb)

    return [args.fileName, costF, metric, args.nNet, args.nNode, args.rho, args.gamma, args.snirDb]


########################################
if __name__ == "__main__":
    # constants
    nSeedDig = 5
    maxNHops = 50

    # parse arguments
    fileName,costF,metric, nNet, nNode,rho, gamma,snirDb = ParseArgs()
    snir = 10 ** (snirDb/20)

    # set up
    SetSeed()
    seedL = [randint(0, 10**nSeedDig - 1) for _ in range(nNet)]

    # do for each file
    log = Log(fileName, 60)
    for netNum in range(len(seedL)):
        seed = SetSeed(seedL[netNum])
        netR = NetR(nNode, rho)

        net = RandNetCirc(nNode, netR)
        nodeLoc,link = net

        pathEnd = sample(range(nNode), k=2)

        # get path
        linkCost = [costF(nodeLoc[n0], nodeLoc[n1]) for (n0,n1) in link]
        path = BestPath(net, *pathEnd, linkCost)

        if path is not None:
            # make interference graph
            nHops = len(path)
            if maxNHops < nHops:
                print(f'Will skip (n = {nHops})')
            else:
                if 30 < nHops:
                    print(f'Big One (n = {nHops})')

                interfearGraph = (nHops, PathSelfInter(net,path,gamma,snir))

                # compute independent subsets
                subSetTimer = StopWatch(running=True)
                clique = Clique(interfearGraph)
                subSetTime = subSetTimer.Stop()

                # log the results
                nClique = len(clique)
                cliqueNum = max(len(c) for c in clique)
                print(f'{netNum}:  {nHops}, {EngNum(nClique)}, {cliqueNum}, {EngNum(subSetTime)}s')

                line = (
                    f'[[{nNode}, {rho}, {seed}], [{nHops}, {nClique}, {subSetTime}]]'
                )
                log.Log(line)

    log.Flush()
