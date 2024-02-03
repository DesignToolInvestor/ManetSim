#
# B e s t P a t h . p y
#
from collections import deque

from Net import Net2FanLink
from LocUtil import Index
from PathHeap import PathHeap

def BestPath(source,sink, net, costF):
    # parse arguments
    nodeLoc,linkL = net
    nNode = len(nodeLoc)

    # set up
    node2Node = Net2FanLink(net)
    linkCost = [costF(Index(nodeLoc, link)) for link in linkL]

    # Do walk
    pathHeap = PathHeap
    pathHeap.Push((source,0,None))

    visited = [False for _ in range(nNode)]
    cost = [float("inf") for _ in range(nNode)]
    parent = [None for _ in range(nNode)]
    
    done = False
    while not done:
        # when popped, node is done
        nodeId,nodeCost,parentId = pathHeap.Pop()
        cost[nodeId] = nodeCost
        parent[nodeId] = parentId

        done = (nodeId == sink)
        if not done:
            neighborL = node2Node[nodeId]

            for neighborId,linkId in neighborL:
                if not visited[neighborId]:
                    neighborCost = nodeCost + linkCost[linkId]
                    pathHeap.Push((neighborId, neighborCost))
                    visited[neighborId] = True

                elif pathHeap.Peak(neighborId) != None:
                    currCost, _ = pathHeap.Peak(neighborId)
                    newCost = nodeCost + linkCost[neighborId]
                    if newCost < currCost:
                        pathHeap.ChangeCost(nodeId, newCost)

                else:
                    pass    # just for debugging

    result = deque([sink])
    node = sink
    
    while node != source:
        node = parent[node]
        result.appendleft(node)
    
    result = list(result)
