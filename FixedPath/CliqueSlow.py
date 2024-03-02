#
# C l i q u e S l o w . p y
#

# This library contains functions that compute all the cliques in a graph, using exhaustive search.
# It's primarily purpose is to test the correctness of less slow methods.

# This function is leveraging (and enforcing) the assumption that all the sets are
# represented with ordered tuples.  It expects the graph to be of the form *(nNode, link)*,
# where link is of type of *list of list*.

# TODO:  Change graph to use a *tuple of tuples* for *link*

from LocMath import PowerSetTup


def Clique(graph):
    # parse arguments
    nNode, linkL = graph

    # setup
    result = []
    powerSet = PowerSetTup(nNode)

    # test all the subsets
    for set in powerSet:
        if (0 < len(set)):
            setLen = len(set)

            i0 = 0
            done = False
            while (i0 < setLen) and not done:
                i1 = i0 + 1

                while (i1 < setLen) and not done:
                    n0 = set[i0]
                    n1 = set[i1]

                    if (n0, n1) not in linkL:
                        done = True
                    i1 += 1

                i0 += 1

            if not done:
                result.append(set)

    return result