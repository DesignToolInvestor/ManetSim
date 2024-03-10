#
# I n d e p e n d N a i v e . p y
#

from LocMath import PowerSet


##########################################################################
def IndSubSet(graph):
    # parse arguments
    nNode, linkL = graph

    # setup
    result = []
    powerSet = PowerSet(nNode)

    # test all the subsets
    for subSet in powerSet:
      if (0 < len(subSet)):
        setLen = len(subSet)

        i0 = 0
        done = False
        while (i0 < setLen) and not done:
          i1 = i0 + 1

          while (i1 < setLen) and not done:
            n0, n1 = [subSet[i0], subSet[i1]]
            if ((n0, n1) in linkL) or ((n1, n0) in linkL):
              done = True
            i1 += 1

          i0 += 1

        if not done:
          result.append(subSet)

    return result