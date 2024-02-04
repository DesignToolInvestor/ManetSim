#
# t e s t _ D i j k s t r a . p y
#

import random
from matplotlib import pyplot as plot

from Dijkstra import DijkstraBack, DijkstraFor
from LocUtil import SetSeed
from MakeNet import RandNetCirc
import MakeNet
from Visual import GraphBiNet

if __name__ == "__main__":
        # constants
        nNode = 30
        rho = 3

        seed = None
        numSeedDig = 2

        # make network
        r = MakeNet.R(nNode,rho)

        seed = SetSeed(seed, numSeedDig)
        print(f'Seed: {seed}')

        net = RandNetCirc(nNode, r)
        nodeLoc,linkL = net

        # build ground truth
        linkCost = [1 for (n0, n1) in linkL]
        source = random.randint(0, len(nodeLoc) - 1)
        cost,back = DijkstraFor(net, source, linkCost)

        # print graph
        fig,ax = plot.subplots(figsize=(6.5,6.5))
        GraphBiNet(ax, net, True, True, nodeNum=cost)
        plot.title(f'N = {nNode}; Seed = {seed}')

        # save figure
        fileName = f'Dijkstra/dijkstra_{nNode}_{seed}_cost'
        plot.savefig(fileName, dpi=200)
        plot.show()

        ########################################
        # Code for debugging
        #
        # fig,ax = plot.subplots(figsize=(6.5,6.5))
        # GraphBiNet(ax, net, True, True, nodeNum=[k for k in range(nNode)])
        # plot.title(f'N = {nNode}; Seed = {seed}')
        #
        # # save figure
        # fileName = f'Dijkstra/dijkstra_{nNode}_{seed}_num'
        # plot.savefig(fileName, dpi=200)
        # plot.show()
