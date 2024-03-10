#
# I n t e r f e r e . p y
#

from matplotlib import pyplot as plot
from math import cos, pi, sin

from LocUtil import Grid1, Sub, UnZip
from LocMath import Add, Diff, Dist, Perp, Scale


###############################
# This function returns the interference distance for a link.  That is the distance that another 
# transmitter must be from the receiver in order NOT to interfere.
def InterDist(linkDist, gamma, snir):
    return linkDist * (snir / (1 - linkDist ** gamma)) ** (1 / gamma)


# TODO:  make this a class so that code reuse is less messy
def TableBi(recLoc,transLoc, excludeR):
    nHops = len(recLoc)
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

    return tuple(linkLink)


def TableDir(recLoc, transLoc, excludeR):
    nHops = len(recLoc)
    linkLink = []

    for link0 in range(nHops):
        for link1 in range(nHops):
            if link0 != link1:
                interDist = Dist(recLoc[link0], transLoc[link1])
                if (interDist < excludeR[link0]):
                    linkLink.append((link0, link1))

    return linkLink


def PathSelfInter(net, path, gamma, snir, dir=False):
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
    if dir:
        linkLink = TableDir(recLoc,transLoc, excludeR)
    else:
        linkLink = TableBi(recLoc,transLoc, excludeR)

    return linkLink


##############################
def PlotInerCirc(ax, nodeLoc, path, gamma, snir, netCirc=None):
    # constants
    # TODO:  make this a function of 'figsize'
    offSet = 0.25
    pointPerLine = 30

    # parse args
    nHop = len(path) - 1

    pathLoc = Sub(nodeLoc, path)
    recLoc = pathLoc[1:]
    transLoc = pathLoc[:nHop]

    linkDir = [Diff(*pathLoc[i: i + 2]) for i in range(nHop)]
    perpDir = [Perp(lD) for lD in linkDir]

    hopLen = [Dist(pathLoc[k], pathLoc[k + 1]) for k in range(nHop)]
    excluR = [InterDist(l, gamma, snir) for l in hopLen]

    # do each hop
    for i in range(nHop):
        # label receiver
        x = recLoc[i][0] + offSet * perpDir[i][0]
        y = recLoc[i][1] + offSet * perpDir[i][1]
        plot.text(
            x, y, f'R{i}', color="black", ha="center", va="center", zorder=0)

        # label transmitters
        x = transLoc[i][0] - offSet * perpDir[i][0]
        y = transLoc[i][1] - offSet * perpDir[i][1]
        plot.text(
            x, y, f'T{i}', color="black", ha="center", va="center", zorder=3)

        # do circle at receiver
        # circ = (recLoc[i], excluR[i])
        # arc = CircClipCirc(circ, netCirc)
        # if arc is not None:
        #   cent,angRange = arc
        #   theta = Grid1(*angRange, pointPerLine)
        #   x,y = UnZip([(cent[0] * excluR[i] * cos(t), cent[0] * excluR[i] * sin(t)) for t in theta])
        #   plot.plot(x,y, ':', color='limegreen')

        cent = recLoc[i]
        theta = Grid1(0, 2 * pi, pointPerLine)
        r = excluR[i]
        x, y = UnZip([(cent[0] + r * cos(t), cent[1] + r * sin(t)) for t in theta])
        plot.plot(x, y, ':', color='limegreen', zorder=-2)

        # Do circle diameters perpendicular to link
        a = Add(recLoc[i], Scale(excluR[i], perpDir[i]))
        b = Add(recLoc[i], Scale(-excluR[i], perpDir[i]))

        # TODO:  clip with the network boundary
        plot.plot([a[0], b[0]], [a[1], b[1]], ':', color='limegreen', zorder=-3)
