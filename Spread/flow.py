#
# f l o w . p y
#
# This program solves the capacity problem for a fixed number of flows on a given network.
#
# The formulation is to randomly pick end-point for the specified number of flows and then set up the
# optimization problem to be solved via a separate program.
#
# Call this as
#   SingleStrand <net_file> -n=<num_flow>

# system packages

import argparse
import cvxpy
from datetime import datetime
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


###############################################################################
# trace functionality
# TODO:  Make this an object that encapsulates it's state

TRACE_ON = True

def Trace(format, stream=None, link0=None, link1=None):
    if TRACE_ON:
        if stream is None:
            print(format)
        else:
            assert(link0 is not None)

            if type(stream) != list:
                stream = [stream]
            if type(link0) != list:
                link0 = [link0]

            streamChar = list(map(lambda num: chr(num + 65), stream))

            name0 = ["{}{}".format(linkNum,let) for linkNum in link0 for let in streamChar]
            nameStr0 = LocUtil.List2Str(name0)

            if link1 is None:
                print(format.format(nameStr0))
            else:
                if (link1 != None) and (type(stream) != list):
                    link1 = [link1]

                name1 = ["{}{}".format(linkNum, let) for linkNum in link1 for let in streamChar]
                nameStr1 = LocUtil.List2Str(name1)
                print(format.format(nameStr0,nameStr1))


###############################################################################
def OptFlow(net, stream):
    startTime = datetime.now()

    # parse parameters
    node,link = net
    nNode = len(node)
    nLink = len(link)

    nStream = len(stream)

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

    ###########################
    # define the variables and the parameter
    # TODO:  This should be a vector rather than a list
    linkRate = list([cvxpy.Variable() for j in range(nLink)] for k in range(nStream))

    flowRate = cvxpy.Parameter(nonneg=True)

    ###########################
    # Do constraints
    constraints = []

    # constraints at the ends of the streams
    Trace("Constraints for sources and sinks")
    for streamId in range(nStream):
        source, sink = stream[streamId]

        # source end of stream
        outLink = node2LinkOut[source]
        Trace('{} = flowRate', streamId, outLink)
        constraints.append(sum(LocUtil.Index(linkRate[streamId], outLink)) == flowRate)

        inLink = node2LinkIn[source]
        Trace('{} = 0', streamId, inLink)
        constraints.append(sum(LocUtil.Index(linkRate[streamId], inLink)) == 0)

        # sink end of stream
        inLink = node2LinkIn[sink]
        Trace('{} = flowRate', streamId, inLink)
        constraints.append(sum(LocUtil.Index(linkRate[streamId], inLink)) == flowRate)

        outLink = node2LinkOut[sink]
        Trace('{} = 0', streamId, outLink)
        constraints.append(sum(LocUtil.Index(linkRate[streamId], outLink)) == 0)

    # constraints for conservation of stream (except at ends of the flows)
    Trace("Constraints for conservation at non-source and non-sink nodes")

    endNode = LocUtil.FlattenAll(stream)
    nonEndNode = LocUtil.ListMinus([nodeId for nodeId in range(nNode)], endNode)

    for streamId in range(nStream):
        streamVarL = linkRate[streamId]
        for nodeNum in range(nNode):
            if nodeNum not in stream[streamId]:
                outLink = node2LinkOut[nodeNum]
                inLink = node2LinkIn[nodeNum]
                Trace('{} = {}', streamId, outLink, inLink)
                constraints.append(
                    sum(LocUtil.Index(streamVarL, outLink)) == sum(LocUtil.Index(streamVarL, inLink)))

    # constraints for not overloading the nodes -- sink and source nodes
    Trace("Constraints for node linits at source and sink nodes")
    for nodeNum in endNode:
        outLink = node2LinkOut[nodeNum]
        inLink = node2LinkIn[nodeNum]
        Trace('{} <= 1', list(range(nStream)), outLink + inLink)

        outVar = list(linkRate[s][l] for l in outLink for s in range(nStream))
        inVar = list(linkRate[s][l] for l in inLink for s in range(nStream))
        constraints.append(sum(outVar) + sum(inVar) <= 1)

    # constraints for avoiding overloading the nodes -- for non-end nodes
    Trace("Constraints for node linits at non-source and non-sink nodes")
    for nodeNum in nonEndNode:
        outLink = node2LinkOut[nodeNum]
        inLink = node2LinkIn[nodeNum]
        Trace('{} <= 1', list(range(nStream)), outLink + inLink)

        outVar = list(linkRate[s][l] for l in outLink for s in range(nStream))
        inVar = list(linkRate[s][l] for l in inLink for s in range(nStream))
        constraints.append(sum(outVar) + sum(inVar) <= 1)

    # no negative flows
    Trace("Constraints against negative flows")
    for linkId in range(nLink):
        for streamId in range(nStream):
            Trace('0 <= {}', streamId, linkId)
            constraints.append(0 <= linkRate[streamId][linkId])

    # constraints for not overloading links
    Trace("Constraints for link limits")
    for linkId in range(nLink):
        Trace('{} <= 1', list(range(nStream)), linkId)

        var = list(linkRate[s][linkId] for s in range(nStream))
        constraints.append(sum(var) <= 1)

    ###########################
    # set up the problem
    factors = []
    for streamId in range(nStream):
        for linkNum in range(nLink):
            factors.append(linkCost[linkNum] * linkRate[streamId][linkNum])
    goal = cvxpy.Minimize(sum(factors))

    prob = cvxpy.Problem(goal, constraints)

    ###################################
    # solve the problem
    flowRate.value = 3/4

    endTime = datetime.now()
    elapsed = endTime - startTime
    print(f'Setup time {elapsed}')

    startTime = datetime.now()
    prob.solve()

    endTime = datetime.now()
    elapsed = endTime - startTime
    print(f'Solve time {elapsed}')

    print(f'Solution = {prob.status}')

    ###################################
    # print the solution
    PSUDO_EPS = 1e-8;
    N_COLUMN = 5;
    
    for streamId in range(nStream):
        print(f'Stream {chr(streamId + 65)}:')
        nActive = 0
        for linkNum in range(nLink):
            rate = linkRate[streamId][linkNum].value
            if abs(rate) > PSUDO_EPS:
                if (nActive % N_COLUMN) != 0:
                    print(", ", end="")
                nActive += 1
                print(f'({linkNum}: {round(rate*24)})', end="")
                if (nActive % N_COLUMN) == 0:
                    print()
        if (nActive % N_COLUMN) != 0:
            print()


###############################################################################
def ParseArgs():
    parser = argparse.ArgumentParser(
        prog='stream',
        description='This program will compute the path of the optimal stream'
    )

    parser.add_argument('fileName', type=str)
    parser.add_argument('-n', type=int)
    parser.add_argument('-stream', type=str)
    parser.add_argument('-seed', type=int)

    args = parser.parse_args()
    if (args.n == None) and (args.stream == None):
        raise Exception('Must either specify the number of flows (to be picked randomly) or the flows')
    elif (args.n != None) and (args.stream != None):
        raise Exception("Can't specify both the number of random flows and the flows")

    return [args.fileName, args.n, args.stream, args.seed]


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
        stream = []
        for k in range(n):
            source = random.randint(0, nNode - 1)
            sink = random.randint(0, nNode - 1)
            stream[k].append([source, sink])

    else:
        assert(flowStr != None)

        flowStrList = flowStr.split("),")
        stream = list(map(lambda str: scanf.scanf("(%d,%d", str), flowStrList))

    OptFlow(net, stream)