#
# m a k e _ i n t e r f e r e . p y
#
import os
# This scrip will generate interference graphs from network graphs and store them in files for
# analysis by other programs

import random
from matplotlib import pyplot as plot

from BestPath import BestPath
import Cost
from Interfere import PathSelfInter
from LocUtil import SetSeed, Sub, UnZip
import MakeNet
from MakeNet import RandNetCirc
from Visual import GraphBiNet


def Order(n0, n1):
    if n0 < n1:
        return [n0, n1]
    else:
        return [n1, n0]


# TODO:  move to LocUtil and add unit test
def Cent(seg):
    (x0, y0), (x1, y1) = seg
    return ((x0 + x1) / 2, (y0 + y1) / 2)


# TODO:  Break this up into smaller functions
def DoNet(seed, rhoStr):
    # make net
    seed = SetSeed(seed, digits=numSeedDig)
    print(f'seed = {seed}')

    r = MakeNet.R(nNode, rho)
    net = RandNetCirc(nNode, r)
    nodeLoc, linkL = net

    flow = random.sample([k for k in range(nNode)], k=2)

    # find best flow
    linkCost = [Cost.Dist(nodeLoc[n0], nodeLoc[n1]) for (n0, n1) in linkL]
    path = BestPath(net, *flow, linkCost)

    if path is None:
        nHops = 0
    else:
        nHops = len(path) - 1
    print(f'{nHops} hops')

    ###########################
    # make graph
    fig, ax = plot.subplots(figsize=(6.5,6.5))
    GraphBiNet(ax, net)

    # mark end points
    endColor = (0.3,1,0.3)

    x,y = nodeLoc[flow[0]]
    plot.plot(x,y, 's', color=endColor, markersize=7, zorder=-1)

    x,y = nodeLoc[flow[1]]
    plot.plot(x,y, 'o', color=endColor, markersize=7, zorder=-1)

    # mark selected path
    pathColor = (1,1,0.5)

    if 0 < nHops:
        x,y = UnZip(Sub(nodeLoc, path))
        plot.plot(x,y, color=pathColor, linewidth=4, zorder=-2)

        # change color on nodes along route
        plot.plot(x, y, 'bo', markersize=3, zorder=2)

    # annotation
    plot.title(f'{nHops} hops @ rho = {rho} (n = {nNode}, seed = {seed})')

    # save figure
    fileName = f'Cases 500/shortest_{nNode}_{rhoStr}_{seed}_{nHops}.png'
    plot.savefig(fileName, dpi=200)
    # plot.show()   # takes a long time to display in PyCharm
    plot.close()

    ###########################
    # build link interference graph

    # find links in path
    if 0 < nHops:
        # linkLink is the links between the links, links are renumbers to the links in the path
        snir = 10 ** (snirDb / 20)
        linkLink = PathSelfInter(net, path, gamma, snir)

        # save link net
        fileName = f'Cases 500/shortest_{nNode}_{rhoStr}_{seed}_{nHops}.graph'
        with open(fileName, 'w') as file:
            file.write(f'{nHops}\n')
            file.write(f'{dist}\n')
            for link in linkLink:
                file.write(f'{link[0]}, {link[1]}\n')


if __name__ == "__main__":
    # constants
    nNode = 500
    numNet = 50

    # TODO: one file per network is too fine grained.
    rho = 2.0
    rhoStr = "2.0"

    seed = None
    numSeedDig = 5

    snirDb = 0
    gamma = 2

    nPointCirc = None

    # do all the networks
    for _ in range(numNet):
        DoNet(seed, rhoStr)
