#
# I n t e r f e r e . p y
#

from LocUtil import Sub
from LocMath import Dist

###############################
# This function returns the interference distance for a link.  That is the distance that another 
# transmitter must be from the receiver in order NOT to interfere.
def InterDist(linkDist, gamma, snir):
    return linkDist * (snir / (1 - linkDist ** gamma)) ** (1 / gamma)


def PathSelfInter(net, path, gamma, snir):
    # parse arguments
    assert(path is not None)
    nHops = len(path) - 1
    
    nodeLoc,linkL = net

    # compute tables for exclusion range of each link in path
    recLoc = Sub(nodeLoc, path[1:])
    transLoc = Sub(nodeLoc, path[:nHops])
    
    linkLen = [Dist(nodeLoc[path[k]], nodeLoc[path[k + 1]]) for k in range(nHops)]
    excludeR = [InterDist(l, gamma, snir) for l in linkLen]

    # make edge table
    linkLink = []
    for link0 in range(0, nHops - 1):
        for link1 in range(link0 + 1, nHops):
            interDist = Dist(recLoc[link0], transLoc[link1])
            if (interDist < excludeR[link0]):
                linkLink.append((link0, link1))
            else:
                interDist = Dist(recLoc[link1], transLoc[link0])
                if (interDist < excludeR[link1]):
                    linkLink.append((link0, link1))

    return linkLink