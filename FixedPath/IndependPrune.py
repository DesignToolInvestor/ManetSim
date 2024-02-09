#
# I n d e p e n d P r u n e . p y
#

# indSubSet is indexed by the numer of links in the subset.  Each element is a list of
# independent subsets of the links with that many links in the subset.

from LocUtil import Flatten, ListMinus

def IndSubSet(graph):
    # parse arguments
    nNode, linkL = graph

    # do case for subset size == 1
    indSubSet = [[[id] for id in range(nNode)]]

    # do case for subset size == 2
    level2 = []
    for n0 in range(nNode - 1):
        for n1 in range(n0 + 1, nNode):
            # operation is important for speed
            if ((n0,n1) not in linkL) and ((n1,n0) not in linkL):
                level2.append([n0,n1])

    indSubSet.append(level2)

    # do cases for larger subset sizes
    subSetSize = 2
    while 0 < len(indSubSet[subSetSize - 1]):
        level = []
        for leaf in indSubSet[subSetSize - 1]:
            for extendNode in range(max(leaf) + 1, nNode):
                i = 0
                noConflict = True

                while noConflict and (i < subSetSize):
                    testCase = leaf.copy()
                    testCase[i] = extendNode

                    # TODO: compair the speed of assembling it in order with sorting
                    testCase.sort()

                    # TODO: compare the speed of binary search, dict, and list
                    # this operation will dominate speed
                    noConflict = (testCase in indSubSet[subSetSize - 1])
                    i += 1

                if noConflict:
                    # TODO: compair the timing of assembling it in order with sorting
                    nextSet = leaf.copy()
                    nextSet.append(extendNode)
                    level.append(sorted(nextSet))

        indSubSet.append(level)
        subSetSize += 1

    # return all the different sizes
    return Flatten(indSubSet,1)
