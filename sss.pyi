#
# s s s . p y
#   Single Strand Setup
#
# This program sets up the optimization problem for determining the maximum capacity for a single strand flow.
#
# The formulation is to randomly pick end-point for the specified number of flows and then setup the optimization
# problem to be solved via a separate program.
#
# Call this as
#   SingleStrand <net_file> -n=<num_flow>

import random
import scanf
import sys
import matplotlib.pyplot as plot

def LinkCost(net):
    nodeL,linkL = net
    result = []

    for link in linkL:
        dist = Dist(nodeL[link[0]], nodeL[link[1]])
        result.append(dist)

    return result


def RandEnds(nNode, nPair):
    result = []
    for k in range(nPair):
        pair = [random.randint(0, nNode), random.randint(0, nNode)]
        while (pair[0] == pair[1]):
            pair = [random.randint(0, nNode), random.randint(0, nNode)]
        result.append(pair)

    return result


if __name__ == '__main__':
    random.seed(0)

    fileName = sys.argv[1]
    nFlow = int(sys.argv[2])

    net = ReadNet(fileName)
    nNode = len(net[1])
    linkCost = LinkCost(net)

    flowEnds = RandEnd(nNode, nFlow)

    print(flowEnds)