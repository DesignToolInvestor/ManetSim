#
# i n d e p e n d _ t i m e . p y
#

# This program is to test the speed at which independent subset can be constructed from a link
# graph.

# system files
from random import randint, sample
import argparse

# open source packages
from engineering_notation import EngNumber as EngNum

# local files
from BestPath import BestPath
import Cost
from IndependPrune import IndSubSet
from Interfere import PathSelfInter
from LocUtil import SetSeed
from Log import Log
from StopWatch import StopWatch
from MakeNet import RandNetCirc, NetR


#######################################
def ParseArgs():
    parser = argparse.ArgumentParser(
        prog='independ_time',
        description='This script will read the files in a directory and time the setup and solver'
    )

    parser.add_argument('fileName', type=str)

    parser.add_argument('-nNode', type=int, default=500)
    parser.add_argument('-nNet', type=int, default=100)

    parser.add_argument('-rho', type=int, default=2.0)
    parser.add_argument('-gamma', type=float, default=2.0)
    parser.add_argument('-snirDb', type=float, default=0.0)

    # parse args
    args = parser.parse_args()

    return [args.fileName, args.nNode, args.nNet, args.rho, args.gamma, args.snirDb]


########################################
if __name__ == "__main__":
    # constants
    nSeedDig = 5
    maxNHops = 40

    # parse arguments
    fileName,nNode,nNet,rho,gamma,snirDb = ParseArgs()
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
        # linkCost = [Cost.LinkR(nodeLoc[n0], nodeLoc[n1]) for (n0,n1) in link]
        linkCost = [Cost.ExcluR(nodeLoc[n0], nodeLoc[n1], gamma,snir) for (n0,n1) in link]
        # linkCost = [Cost.ExcluArea(nodeLoc[n0], nodeLoc[n1], gamma,snir) for (n0,n1) in link]

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
                subSet = IndSubSet(interfearGraph)
                subSetTime = subSetTimer.Stop()

                # log the results
                nSubSet = len(subSet)
                print(f'{netNum}:  {nHops}, {EngNum(nSubSet)}, {EngNum(subSetTime)}s')

                line = (
                    f'[[{nNode}, {rho}, {seed}], [{nHops}, {nSubSet}, {subSetTime}]]'
                )
                log.Log(line)

    log.Flush()
