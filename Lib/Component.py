#
# C o m p o n e n t . p y
#

# This file contains functions for computing the components of a network.

# The function *Component* will group all the nodes in a network into components and sort them
# according to the number of nodes in the component.  The node numbering will be the same as in
# the original network.

# The function *DomCompSubNet* will return a new network consisting only of the nodes in the
# dominant component.  This is convenient for functions that take a network rather than a subset
# of network.  The nodes are renumbered and the links are updated to match this new numbering.


import IndexPool
import LocUtil

def Component(net, direct=False):  # problem specifying list(list[int,ing]) as output type
    # parse arguments
    nodeL,link = net
    nNode = len(nodeL)

    # make neighbor table
    neighborTab = [[] for i in range(nNode)]
    for (n0,n1) in link:
        neighborTab[n0].append(n1)
        neighborTab[n1].append(n0)

    # pre-loop setup
    unVisited = IndexPool.IndexPool(nNode, initFull=True)
    edge = []

    comp = []
    numComp = 0;

    # component external loop
    while unVisited.Len() > 0:
        node = unVisited.Pop()
        comp.append([node])
        numComp += 1

        # component internal loop
        while node != None:
            neighbor = neighborTab[node]
            for node in neighbor:
                if unVisited.Active(node):
                    edge.append(node)
                    comp[numComp - 1].append(node)
                    unVisited.Drop(node)

            node = edge.pop() if edge != [] else None

    return sorted(comp, key=len, reverse=True)


def DomCompSubNet(net, direct=False) -> [list([float,float]), list([int,int])]:
    # parse arguments
    nodeLoc,link = net
    nNode = len(nodeLoc)

    comp = Component(net)

    newToOld = comp[0]
    oldToNew = LocUtil.MapInverse(newToOld, nNode)

    newLink = LocUtil.Sub(oldToNew, link)
    newNode = LocUtil.Sub(nodeLoc, newToOld)

    return [newNode,newLink]