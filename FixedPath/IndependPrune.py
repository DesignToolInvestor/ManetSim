#
# I n d e p e n d P r u n e . p y
#

# Each element in subBySize contains all the independent subsets of a fixed size (i.e.,
# of size index plus one).

from LocUtil import Flatten


def IndSubSet(graph):
    # parse arguments
    nNode, linkL = graph

    # do case for subset size == 1
    subBySize = [{id for id in range(nNode)}]

    # do case for subset size == 2
    level2 = []
    for n0 in range(nNode - 1):
        for n1 in range(n0 + 1, nNode):
            # operation is important for speed
            if ((n0,n1) not in linkL) and ((n1,n0) not in linkL):
                level2.append((n0,n1))

    subBySize.append({*level2})

    # do cases for larger subset sizes
    subSetSize = 3
    while 0 < len(subBySize[subSetSize - 2]):
        level = []
        for leaf in subBySize[subSetSize - 2]:
            # because the subsets are in order only need to consider extension beyond mas
            for extendNode in range(max(leaf) + 1, nNode):
                dropIndex = 0
                noConflict = True

                while noConflict and (dropIndex < subSetSize - 1):
                    # care to keep the subset sorted
                    temp = \
                        tuple(leaf[i] for i in range(dropIndex)) + \
                        tuple(leaf[i] for i in range(dropIndex + 1, subSetSize - 1))
                    mustHave = (*temp, extendNode)

                    noConflict = (mustHave in subBySize[subSetSize - 2])
                    dropIndex += 1

                if noConflict:
                    # care to keep the subset sorted
                    newSub = (*leaf, extendNode)
                    level.append(newSub)

        subBySize.append({*level})
        subSetSize += 1

    # return all the different sizes
    result = Flatten(subBySize,1)
    result = [[*s] if type(s) == tuple else [s] for s in result]

    return result
