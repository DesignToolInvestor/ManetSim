#
# I n d e p e n d S l o w . p y
#

# This library contains a function to construct the set of independent subsets of the nodes,
# where independence is defined as the absences of direct links between any of the nodes in the
# subset.  This is the central step in computing the fractional cover of the graph, which in turn
# is used to compute the chromatic number of the graph.

from LocMath import PowerSet


def IndSubSet(graph):
    # parse arguments
    nNode, linkL = graph
    
    # setup
    result = []
    powerSet = PowerSet(nNode)

    # test all the subsets
    for set in powerSet:
        if (0 < len(set)):
            setLen = len(set)

            i0 = 0
            done = False
            while (i0 < setLen) and not done:
                i1 = i0 + 1

                while (i1 < setLen) and not done:
                    n0,n1 = (set[i0], set[i1])
                    if ((n0,n1) in linkL) or ((n1,n0) in linkL):
                        done = True
                    i1 += 1

                i0 += 1

            if not done:
                result.append(set)

    return result
