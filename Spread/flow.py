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
    # parse command line
    # TODO:  Switch to using argparse
    fileName = sys.argv[1]
    nFlow = int(sys.argv[2])

    # read network
    net,direct = Net.ReadNet(fileName)
    if not direct:
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

    ###########################################################
    # Setup the problem

    ###########################
    # define the variables and the parameter
    # TODO:  This should be a vector rather than a list
    linkFlow = []
    for k in range(nLink):
        linkFlow.append(cvxpy.Variable())

    flowRate = cvxpy.Parameter(nonneg=True)

    ###########################
    # Do constraints
    constraints = []

    # constraints at the ends of the flows
    for flowNum in range(nFlow):
        source,sink = flowEnds[flowNum]

        outLinks = LocUtil.Index(linkFlow, node2LinkOut[source])
        constraints.append(sum(outLinks) == flowRate)

        inLinks = LocUtil.Index(linkFlow, node2LinkIn[sink])
        constraints.append(sum(inLinks) == flowRate)

    # constraints for conservation of flow (except at ends of the flows)
    for nodeNum in range(nNode):
        if nodeNum not in flowEnds:
            outLinks = LocUtil.Index(linkFlow, node2LinkOut[nodeNum])
            inLinks = LocUtil.Index(linkFlow, node2LinkIn[nodeNum])
            constraints.append(sum(inLinks) == sum(inLinks))

    # constraints for not overloading the nodes -- non-sink or source nodes
    for nodeNum in range(nNode):
        if nodeNum not in flowEnds:
            outLinks = LocUtil.Index(linkFlow, node2LinkOut[nodeNum])
            constraints.append(sum(outLinks) <= 1)

    # constraints for not overloading the nodes -- sink and source nodes
    for flowNum in range(nFlow):
        source,sink = flowEnds[flowNum]

        outLinks = LocUtil.Index(linkFlow, node2LinkOut[source])
        inLinks = LocUtil.Index(linkFlow, node2LinkIn[source])
        constraints.append(sum(outLinks) + sum(inLinks) <= 1)

        outLinks = LocUtil.Index(linkFlow, node2LinkOut[sink])
        inLinks = LocUtil.Index(linkFlow, node2LinkIn[sink])
        constraints.append(sum(outLinks) + sum(inLinks) <= 1)

    # constraints for not overloading links
    for link in linkFlow:
        constraints.append(0 <= link)
        constraints.append(link <= 1)

    ###########################
    # set up the problem
    factors = []
    for linkNum in range(nLink):
        factors.append(linkCost[linkNum] * linkFlow[linkNum])
    goal = cvxpy.Minimize(sum(factors))

    prob = cvxpy.Problem(goal, constraints)

    ###################################
    # solve the problem
    flowRate.value = 1/4
    prob.solve()
    print(f'Solution = {prob.status}')

    ###################################
    # print the solution
    psudoEps = 1e-10;
    for linkNum in range(nLink):
        rate = linkFlow[linkNum].value
        if rate > psudoEps:
            print(f'{linkNum}: {rate}')