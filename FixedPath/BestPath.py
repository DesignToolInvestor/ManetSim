#
# B e s t P a t h . p y
#
from collections import deque

from Net import Net2FanLink
from PathHeap import PathHeap

def BestPath(net, source,sink, linkCost):
    # parse arguments
    nodeLoc,linkL = net
    nNode = len(nodeLoc)

    # set up
    neighborTab = Net2FanLink(net)

    # Do walk
    visited = [False for _ in range(nNode)]
    cost = [float("inf") for _ in range(nNode)]
    parent = [None for _ in range(nNode)]

    pathHeap = PathHeap(nNode)
    pathHeap.Push(source,0, -1)

    visited[source] = True

    done = False
    while not done:
        # when popped, node is done
        nodeId,nodeCost,parentId = pathHeap.Pop()
        cost[nodeId] = nodeCost
        parent[nodeId] = parentId

        done = (nodeId == sink)
        if not done:
            neighborL = neighborTab[nodeId]

            for neighborId,linkId in neighborL:
                newCost = nodeCost + linkCost[linkId]

                if not visited[neighborId]:  # first time to reach it
                    pathHeap.Push(neighborId, newCost, nodeId)
                    visited[neighborId] = True

                elif pathHeap.Peak(neighborId) != None:  # still active (not retired)
                    _, currCost, _ = pathHeap.Peak(neighborId)
                    if newCost < currCost:
                        pathHeap.ChangeCost(neighborId, newCost, nodeId)

                else:  # this node is retired
                    pass    # just for debugging

    result = deque([sink])
    node = sink
    
    while node != source:
        node = parent[node]
        result.appendleft(node)
    
    return list(result)
