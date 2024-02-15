#
# C l i c k P r u n e . p y
#

# This library contains functions that compute all the clicks in a graph.
#
# The method used search the tree that generates the entire power set of the nodes, while pruning
# branches of the tree.  The resulting search space is alpha^N where alpha depends on the
# structure of the graph, but is much smaller than 2, when the chromatic number is small.
#
# Caution:
#   The links must be in order.  That is the link (n0,n1) must be represented so that n0 < n1.
#
# The algorithm represents all clicks in order.  It leverages this to:  1) more quickly find
# smaller clicks in the previous result and 2) avoid creating duplicate outputs.
#
# The implementation uses sets of tuples because:  1) the *in* statement is dramatically faster
# for sets than for lists and 2) tuples leverage their immutability to reduce overhead and are
# thus noticeably faster than lists.


from LocUtil import Flatten

def Click(graph):
    # parse arguments
    nNode, linkL = graph

    #############################
    # click size == 1 and 2
    clickBySize = [{(id,) for id in range(nNode)}, {tuple(l) for l in linkL}]

    #############################
    # click size > 2
    clickSize = 3
    while 0 < len(clickBySize[clickSize - 2]):
        level = []
        for leaf in clickBySize[clickSize - 2]:
            # because the subsets are in order only need to consider extension beyond mas
            for extendNode in range(max(leaf) + 1, nNode):
                dropIndex = 0
                noMissLink = True

                while noMissLink and (dropIndex < clickSize - 1):
                    # care to keep the subset sorted
                    temp = \
                        tuple(leaf[i] for i in range(dropIndex)) + \
                        tuple(leaf[i] for i in range(dropIndex + 1, clickSize - 1))
                    mustHave = (*temp, extendNode)

                    noMissLink = (mustHave in clickBySize[clickSize - 2])
                    dropIndex += 1

                if noMissLink:
                    # care to keep the subset sorted
                    newSub = (*leaf, extendNode)
                    level.append(newSub)

        clickBySize.append({*level})
        clickSize += 1

    # return all the different sizes
    result = Flatten(clickBySize,1)

    return tuple(result)