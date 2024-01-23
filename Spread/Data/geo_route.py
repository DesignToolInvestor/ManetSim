#
# g e o _ r o u t e . p y
#

import math
import random

from LocMath import RandLog, Dist
from LocUtil import SetSeed, MinIndex
import Log
import MakeNet
from MakeNet import RandNetCirc


# TODO:  extract this code to a library
# TODO:  make it work for directed and undirected graphs equally well
def GeoMakeIt(net, source,sink):
    # parse arguments
    nodeLoc,linkL = net
    nNode = len(nodeLoc)

    # construct fanout table
    nodeToNode = [[] for _ in range(nNode)]
    for link in linkL:
        n0,n1 = link
        nodeToNode[n0].append(n1)
        nodeToNode[n1].append(n0)

    # do the route
    sinkLoc = nodeLoc[sink]
    curNode = source
    currDist = Dist(nodeLoc[curNode], sinkLoc)

    while curNode != sink:
        neighborId = nodeToNode[curNode]
        if len(neighborId) == 0:
            break

        distToSink = list(
            map(lambda loc: Dist(loc,sinkLoc),
                map(lambda id: nodeLoc[id], neighborId)))

        # TODO: consider case where we take the best neighbor even if it's worse (live lock)
        best = MinIndex(distToSink)
        if distToSink[best] > currDist:
            break
        else:
            curNode = neighborId[best]
            currDist = distToSink[best]

    return (curNode == sink)


if __name__ == "__main__":
    # constants
    NUM_NET = 300

    MIN_NET_SIZE = 30
    MAX_NET_SIZE = 1_000

    DENSITY = [2]

    FILE_NAME = 'geo_route.log'
    DELAY = 3

    # open log
    log = Log.Log(FILE_NAME, DELAY)

    # do something
    for density in DENSITY:
        seed = SetSeed()
        netSize = [round(RandLog(MIN_NET_SIZE, MAX_NET_SIZE)) for _ in range(NUM_NET)]

        for k in range(NUM_NET):
            # build network
            n = netSize[k]
            r = MakeNet.R(n,density)
            seed = SetSeed()
            net = RandNetCirc(n,r)

            # pick random streams
            nStream = round(math.sqrt(n))
            temp = random.choices(range(n), k=2*nStream)
            streamL = [[temp[2*k],temp[2*k+1]] for k in range(nStream)]

            numGood = 0
            for stream in streamL:
                source,sink = stream
                if GeoMakeIt(net,source,sink):
                    numGood += 1

            info = [[n,r,seed], [nStream, numGood]]
            log.Log(info)

            print(f'{k} of {NUM_NET}:  n = {n}')

    # shouldn't be necessary, but didn't work without
    del log
