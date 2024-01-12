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

# system packages
import argparse
import cvxpy
import random
import scanf

# local packages
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
    

###############################################################################
def OptFlow(net, flow):
    # parse parameters
    node,link = net
    nNode = len(node)
    nLink = len(link)

    nFlow = len(flow)

    # compute link cost
    linkCost = LinkCost(net)

    # convert to fanout style network
    node2LinkOut = []
    node2LinkIn = []
    for nodeNum in range(nNode):
        node2LinkOut.append([])
        node2LinkIn.append([])

    for linkNum in range(nLink):
        start, stop = links[linkNum]
        node2LinkOut[start].append(linkNum)
        node2LinkIn[stop].append(linkNum)

    ###########################################################
    # Setup the problem

    ###########################
    # define the variables and the parameter
    # TODO:  This should be a vector rather than a list
    linkRate = []
    for k in range(nLink):
        linkRate.append(cvxpy.Variable())

    flowRate = cvxpy.Parameter(nonneg=True)

    ###########################
    # Do constraints
    constraints = []

    # constraints at the ends of the flows
    for flowId in range(nFlow):
        source, sink = flow[flowId]

        outLink = LocUtil.Index(linkRate, node2LinkOut[source])
        print(f'{node2LinkOut[source]} = {flowRate}')
        constraints.append(sum(outLink) == flowRate)

        inLink = LocUtil.Index(linkRate, node2LinkIn[sink])
        print(f'{node2LinkIn[sink]} = {flowRate}')
        constraints.append(sum(inLink) == flowRate)

    # constraints for conservation of flow (except at ends of the flows)
    flowEnds = LocUtil.FlattenAll(flow)
    for nodeNum in range(nNode):
        if nodeNum not in flowEnds:
            outLink = LocUtil.Index(linkRate, node2LinkOut[nodeNum])
            inLink = LocUtil.Index(linkRate, node2LinkIn[nodeNum])
            print(f'{node2LinkOut[nodeNum]} = {node2LinkIn[nodeNum]}')
            constraints.append(sum(inLink) == sum(outLink))

    # constraints for avoiding overloading the nodes -- neither sink nor source nodes
    for nodeNum in range(nNode):
        if nodeNum not in flowEnds:
            outLink = LocUtil.Index(linkRate, node2LinkOut[nodeNum])
            inLink = LocUtil.Index(linkRate, node2LinkIn[nodeNum])

            temp = node2LinkOut[nodeNum] + node2LinkIn[nodeNum]
            print(f'{temp} <= 1')
            constraints.append(sum(outLink) + sum(inLink) <= 1)

    # constraints for not overloading the nodes -- sink and source nodes
    for flowId in range(nFlow):
        source,sink = flow[flowId]

        outLink = LocUtil.Index(linkRate, node2LinkOut[source])
        inLink = LocUtil.Index(linkRate, node2LinkIn[source])

        temp = node2LinkOut[source] + node2LinkIn[source]
        print(f'{temp} <= 1')

        constraints.append(sum(outLink) + sum(inLink) <= 1)

        outLink = LocUtil.Index(linkRate, node2LinkOut[sink])
        inLink = LocUtil.Index(linkRate, node2LinkIn[sink])
        constraints.append(sum(outLink) + sum(inLink) <= 1)

    # constraints for not overloading links
    for link in linkRate:
        constraints.append(0 <= link)
        constraints.append(link <= 1)

    ###########################
    # set up the problem
    factors = []
    for linkNum in range(nLink):
        factors.append(linkCost[linkNum] * linkRate[linkNum])
    goal = cvxpy.Minimize(sum(factors))

    prob = cvxpy.Problem(goal, constraints)

    ###################################
    # solve the problem
    flowRate.value = 1
    prob.solve()
    print(f'Solution = {prob.status}')

    ###################################
    # print the solution
    psudoEps = 1e-10;
    for linkNum in range(nLink):
        rate = linkRate[linkNum].value
        if rate > psudoEps:
            print(f'{linkNum}: {rate}')



###############################################################################
def ParseArgs():
    parser = argparse.ArgumentParser(
        prog='flow',
        description='This program will compute the path of the optimal flow'
    )

    parser.add_argument('fileName', type=str)
    parser.add_argument('-n', type=int)
    parser.add_argument('-flow', type=str)
    parser.add_argument('-seed', type=int)

    args = parser.parse_args()
    if (args.n == None) and (args.flow == None):
        raise Exception('Must either specify the number of flows (to be picked randomly) or the flows')
    elif (args.n != None) and (args.flow != None):
        raise Exception("Can't specify both the number of random flows and the flows")

    return [args.fileName, args.n, args.flow, args.seed]


if __name__ == '__main__':
    # parse command line
    fileName,n,flowStr,seed = ParseArgs()

    # read network
    net,direct = Net.ReadNet(fileName)
    if not direct:
        raise Exception("The network must be directional.")
    nodes,links = net
    nNode = len(nodes)

    # deal with flows
    if n != None:
        assert(flowStr == None)
        seed = SetSeed(seed)

        # TODO:  Do choose without replacement
        flow = []
        for k in range(n):
            source = random.randint(0, nNode - 1)
            sink = random.randint(0, nNode - 1)
            flow[k].append([source, sink])

    else:
        assert(flowStr != None)

        flowStrList = flowStr.split("),")
        flow = list(map(lambda str: scanf.scanf("(%d,%d", str), flowStrList))

    OptFlow(net, flow)