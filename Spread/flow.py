#
# f l o w . p y
#
# This program solves the capacity problem for a fixed number of flows on a given network.
#
# The formulation is to randomly pick end-point for the specified number of flows and then setup the optimization
# problem to be solved via a separate program.
#
# Call this as
#   SingleStrand <net_file> -n=<num_flow>

import cvxpy
import random
import sys


import Net
import LocUtil
import LocMath

def LinkCost(net):
    nodeL,linkL = net
    result = []

    for link in linkL:
        dist = LocMath.Dist(nodeL[link[0]], nodeL[link[1]])
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

# TODO: consider rather this is a general representation that should be moved to the Net library
def Net2FanLink(net):
    nodes,links= net
    nNodes = len(nodes)
    
    # initialize linkFan
    linkFan = []
    for k in range(nNodes):
        linkFan.append([])
    
    # walk the links filling in linkFan
    for k in range(links):
        n0,n1 = nodes[k]
        linkFan[n0].append(k)
        linkFan[n1].append(k)
    
    # return results
    return linkFan
    
    
if __name__ == '__main__':
    ###########################
    # read network
    fileName = sys.argv[1]
    nFlow = int(sys.argv[2])

    net,direct = Net.ReadNet(fileName)
    if ~direct:
        raise Exception("The network must be directional.")

    nodes,links = net
    nNode = len(nodes)
    nLink = len(links)

    # compute link cost
    linkCost = LinkCost(net)

    # pick random end points
    random.seed(0)
    flowEnds = RandEnds(nNode, nFlow)
    print(flowEnds)

    # convert to fanout style network
    node2LinkOut = []
    node2LinkIn = []
    for nodeNum in range(nNode):
        node2LinkOut.append([])
        node2LinkIn.append([])

    for linkNum in range(nLink):
        (nodeStart,nodeStop) = links[linkNum]
        node2LinkOut[nodeStart].append(linkNum)
        node2LinkIn[nodeStop].append(linkNum)

    print(node2LinkOut)
    print(node2LinkIn)

    ###########################
    # Setup the problem
    linkVar = []
    for k in range(nLink):
        linkVar.append(cvxpy.Variable())

    flowRate = cvxpy.Pareto(nonneg=True)

    constraints = []
    # Do flow constraints
    for k in range(nFlow):
        source,sink = flowEnds[k]
        linkVars = Index(linkVar, node2LinkOut[source])
        constraints.append(sum(linkVars) == flowRate)
        # net sum of in flows

