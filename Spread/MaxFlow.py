#
# M a x F l o w . p y
#

import cvxpy
from datetime import datetime

import LocMath
import LocUtil

def DefaultLinkCost(a, b):
    return LocMath.DistSqr(a, b)


def LinkCostHelper(net, Metric):
    nodeL, linkL = net
    result = []

    for link in linkL:
        dist = Metric(NodeLoc[link[0]], NodeLoc[link[1]])
        result.append(dist)

    return result

##############################################################################
# trace functionality
# TODO:  Make this an object that encapsulates it's state
# TODO:  Make this a submodule of LocUtil

TRACE_ON = False

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


###############################################################
# TODO:  Should use vectors rather than lists
def FlowConstraints(nLink, nodeOutLink, nodeInLink, stream):
    # parse arguments
    nNode = len(nodeOutLink)
    assert(nNode == len(nodeInLink))

    nStream = len(stream)
    
    # define the variables for the solver
    linkRate = list([cvxpy.Variable() for j in range(nLink)] for k in range(nStream))
    flowRate = cvxpy.Variable()

    # constraints at the ends of the streams
    constraints = []

    Trace("Constraints for sources and sinks")
    for streamId in range(nStream):
        source, sink = stream[streamId]

        # source end of stream
        outLink = nodeOutLink[source]
        Trace('{} = flowRate', streamId, outLink)
        constraints.append(sum(LocUtil.Index(linkRate[streamId], outLink)) == flowRate)

        inLink = nodeInLink[source]
        Trace('{} = 0', streamId, inLink)
        constraints.append(sum(LocUtil.Index(linkRate[streamId], inLink)) == 0)

        # sink end of stream
        inLink = nodeInLink[sink]
        Trace('{} = flowRate', streamId, inLink)
        constraints.append(sum(LocUtil.Index(linkRate[streamId], inLink)) == flowRate)

        outLink = nodeOutLink[sink]
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
                outLink = nodeOutLink[nodeNum]
                inLink = nodeInLink[nodeNum]
                Trace('{} = {}', streamId, outLink, inLink)
                constraints.append(
                    sum(LocUtil.Index(streamVarL, outLink)) == sum(
                        LocUtil.Index(streamVarL, inLink)))

    # constraints for not overloading the nodes -- sink and source nodes
    Trace("Constraints for node linits at source and sink nodes")
    for nodeNum in endNode:
        outLink = nodeOutLink[nodeNum]
        inLink = nodeInLink[nodeNum]
        Trace('{} <= 1', list(range(nStream)), outLink + inLink)

        outVar = list(linkRate[s][l] for l in outLink for s in range(nStream))
        inVar = list(linkRate[s][l] for l in inLink for s in range(nStream))
        constraints.append(sum(outVar) + sum(inVar) <= 1)

    # constraints for avoiding overloading the nodes -- for non-end nodes
    Trace("Constraints for node linits at non-source and non-sink nodes")
    for nodeNum in nonEndNode:
        outLink = nodeOutLink[nodeNum]
        inLink = nodeInLink[nodeNum]
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

    # constraints for not overloading linkL
    Trace("Constraints for link limits")
    for linkId in range(nLink):
        Trace('{} <= 1', list(range(nStream)), linkId)

        var = list(linkRate[s][linkId] for s in range(nStream))
        constraints.append(sum(var) <= 1)

    return (constraints, linkRate, flowRate)


###############################################################################
def MaxFlowRate(net, stream):
    startTime = datetime.now()

    # parse parameters
    node, linkL = net
    nNode = len(node)
    nLink = len(linkL)

    # convert to fanout style network
    nodeOutLink = []
    nodeInLink = []
    for nodeNum in range(nNode):
        nodeOutLink.append([])
        nodeInLink.append([])

    for linkNum in range(nLink):
        start, stop = linkL[linkNum]
        nodeOutLink[start].append(linkNum)
        nodeInLink[stop].append(linkNum)

    ###########################
    # setup constraints
    constraints, linkRate, flowRate = FlowConstraints(nLink, nodeOutLink, nodeInLink, stream)

    goal = cvxpy.Maximize(flowRate)
    prob = cvxpy.Problem(goal, constraints)

    prob.solve()

    if (prob.status != cvxpy.OPTIMAL):
        raise Exception("solver failure", prob.status)
    return flowRate.value
