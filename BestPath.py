#
# B e s t P a t h . p y
#

# This file contains a function for finding the best path in a network

from collections import deque

from Net import Net2FanLink
from PathHeap import PathHeap


# TODO: change source,sink to a tuple called pathEnd
def BestPath(net, endNode, linkCost):
    # parse arguments
    nodeLoc,linkL = net
    nNode = len(nodeLoc)

    source,sink = endNode

    # set up
    neighborTab = Net2FanLink(net)

    # set up
    visited = [False for _ in range(nNode)]
    cost = [float("inf") for _ in range(nNode)]
    parent = [None for _ in range(nNode)]

    pathHeap = PathHeap(nNode)
    pathHeap.Push(source,0, -1)

    visited[source] = True

    # walk until done or can't walk anymore
    done = False
    while (not done) and (0 < pathHeap.NumActive()):
        nodeId,nodeCost,parentId = pathHeap.Pop()
        cost[nodeId] = nodeCost
        parent[nodeId] = parentId

        # node is only popped when there are no lower cost paths to it
        done = (nodeId == sink)
        if not done:
            neighborL = neighborTab[nodeId]

            for neighborId,linkId in neighborL:
                newCost = nodeCost + linkCost[linkId]

                if not visited[neighborId]:  # first time to reach this node
                    pathHeap.Push(neighborId, newCost, nodeId)
                    visited[neighborId] = True

                elif pathHeap.Peak(neighborId) != None:  # node is still active (not retired)
                    _, currCost, _ = pathHeap.Peak(neighborId)
                    if newCost < currCost:
                        pathHeap.ChangeCost(neighborId, newCost, nodeId)

    # return result
    if not done:
        return None

    else:
        result = deque([sink])
        node = sink

        while node != source:
            node = parent[node]
            result.appendleft(node)

        return list(result)
