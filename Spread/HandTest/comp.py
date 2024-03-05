#
# c o m p . p y
#

# This program tests the partitioning of networks into components.  It creates a list of the
# network components represented as a list of node numbers.  The components are sorted in order
# of decreasing size.  That is, the dominant component is the first one.

# TODO:  Does it actually test anything or just go through the motions

import colorsys
import math
from matplotlib import pyplot as plot

import LocUtil
import Component
import MakeNet
import Visual

if __name__ == '__main__':
    # set constants
    N = 600
    RHO = 2
    R = math.sqrt(N / RHO / math.pi)

    SEED = None

    # generate network
    seed = LocUtil.SetSeed(SEED, 3)
    print(f'Seed = {seed}')

    net = MakeNet.RandNetCirc(N,R)
    node,link = net

    # plot network
    fig,ax = plot.subplots(figsize=(6.5,6.5))
    ax = Visual.GraphBiNet(ax, net, showNode=False)

    # break into components
    comp = NetPath.Component(net)
    nComp = len(comp)

    compSize = [len(comp[k]) for k in range(nComp)]
    print(compSize)

    hue = [2/3 * k/(nComp - 1) for k in range(nComp)]
    colorL = [colorsys.hsv_to_rgb(hue[k],1,0.8) for k in range(nComp)]

    # show components
    for k in range(nComp):
        x,y = LocUtil.UnZip(LocUtil.Index(node, comp[k]))
        ax.scatter(x,y, color=colorL[k], s=3)

    # add annotation
    baseLine = R / (2*6.5)
    ax.text(-R, R, str(f'{compSize}'), va="top", ha="left")
    ax.text(-R, R - baseLine, str(f'Seed = {seed}'), va="top", ha="left")
    ax.text(-R, R - 2*baseLine, str(f'N = {N}'), va="top", ha="left")

    # save figure
    fileName = f'comp_{N}_{seed}.png'
    plot.savefig(fileName, dpi=200)