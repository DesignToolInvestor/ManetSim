#
# D i j k s t r a . p y
#

from collections import deque

from Net import Net2FanLink

def DijkstraFor(net, sourceId, linkCost):
    # set up
    nodeLoc,linkL = net
    nNodes = len(nodeLoc)

    neighborTab = Net2FanLink(net)

    nodeCost = [float("inf") for _ in range(nNodes)]
    back = [-1 for _ in range(nNodes)]

    visited = [False for _ in range(nNodes)]
    toDo = []

    # source node
    nodeCost[sourceId] = 0
    visited[sourceId] = True
    toDo = [sourceId]
    back[sourceId] = -1

    # do loop
    while 0 < len(toDo):
        currId = toDo.pop()
        currCost = nodeCost[currId]
        neighbor = neighborTab[currId]

        for nodeId,linkId in neighbor:
            newCost = currCost + linkCost[linkId]
            if newCost < nodeCost[nodeId]:
                nodeCost[nodeId] = newCost
                back[nodeId] = currId

                if not nodeId in toDo:
                    toDo.append(nodeId)

    return nodeCost, back


def DijkstraBack(back,source, dest):
    node = dest
    path = deque()

    while 0 <= back[node]:
        path.appendleft(node)
        node = back[node]

    if node != source:
        return None
    else:
        path.appendleft(node)
        return list(path)