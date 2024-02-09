#
# m a k e _ p a t h_ g r a p h . p y
#

from math import cos, pi, sin
from matplotlib import pyplot as plot, pyplot as plt
import random

from BestPath import BestPath
import Cost
from Interfere import InterDist
from LocMath import Dist
from LocUtil import SetSeed, Sub, UnZip
from MakeNet import RandNetCirc
import MakeNet


def Order(n0,n1):
    if n0 < n1:
        return [n0,n1]
    else:
        return [n1,n0]


# TODO:  move to LocUtil and add unit test
def Cent(seg):
    (x0,y0),(x1,y1) = seg
    return ((x0 + x1)/2, (y0 + y1)/2)


if __name__ == "__main__":
    # constants
    nNode = 50

    rho = 2.0
    rhoStr = "2"

    seed = 404
    numSeedDig = 3

    snirDb = 0
    gamma = 2

    nPointCirc = 30

    # make net
    seed = SetSeed(seed, digits=numSeedDig)

    r = MakeNet.R(nNode,rho)
    net = RandNetCirc(nNode,r)
    nodeLoc,linkL = net

    flow = random.sample([k for k in range(nNode)], k=2)

    # find best flow
    linkCost = [Cost.Dist(nodeLoc[n0], nodeLoc[n1]) for (n0,n1) in linkL]
    path = BestPath(net, *flow, linkCost)
    if path is None:
        raise Exception("No path found")

    ###########################
    # make graph
    # fig, ax = plot.subplots(figsize=(6.5,6.5))
    # GraphBiNet(ax, net)
    #
    # # mark end points
    # endColor = (0.3,1,0.3)
    #
    # x,y = nodeLoc[flow[0]]
    # plot.plot(x,y, 's', color=endColor, markersize=7, zorder=-1)
    #
    # x,y = nodeLoc[flow[1]]
    # plot.plot(x,y, 'o', color=endColor, markersize=7, zorder=-1)
    #
    # # mark selected path
    # pathColor = (1,1,0.5)
    #
    # x,y = UnZip(Sub(nodeLoc, path))
    # plot.plot(x,y, color=pathColor, linewidth=4, zorder=-2)
    #
    # # change color on nodes along route
    # plot.plot(x, y, 'bo', markersize=3, zorder=2)
    #
    # # annotation
    # plot.title(f'n = {nNode}, rho = {rho}, seed = {seed}, hops = {len(path) - 1}')
    #
    # # save figure
    # fileName = f'Figures/shortest_{nNode}_{rhoStr}_{seed}.png'
    # plot.savefig(fileName, dpi=200)
    # # plot.show()   # takes a long time to display in PyCharm

    ###########################
    # save link network
    # find links in path
    nPathLink = len(path) - 1

    pathLink = [[path[k], path[k+1]] for k in range(nPathLink)]
    linkSet = [{*l} for l in linkL]
    linkId = [linkSet.index({*l}) for l in pathLink]

    # compute tables for edge computation
    sinkLoc = Sub(nodeLoc, path[1:])
    linkLen = [Dist(nodeLoc[path[k]], nodeLoc[path[k+1]]) for k in range(nPathLink)]
    print(f'linkLen: {linkLen}')
    
    snir = 10 ** (snirDb / 20)
    excludeR = [InterDist(l, 2, snir) for l in linkLen]
    
    # make edge table
    linkLink = []
    for l0 in range(0, nPathLink - 1):
        for l1 in range(l0 + 1, nPathLink):
            interDist = Dist(sinkLoc[l0], sinkLoc[l1])
            if (interDist < excludeR[l0]) or (interDist <= excludeR[l1]):
                linkLink.append((l0,l1))

    # save link net
    fileName = 'interfere_a.graph'
    with open(fileName, 'w') as file:
        file.write(f'{nPathLink}\n')
        for link in linkLink:
            file.write(f'{link[0]}, {link[1]}\n')