#
# t e s t _ B e s t P a t h . p y
#

from matplotlib import pyplot as plot
import random
from unittest import TestCase

from BestPath import BestPath
from Dijkstra import DijkstraBack, DijkstraFor
import Cost
from LocUtil import SetSeed
from MakeNet import RandNetCirc
import MakeNet
from Visual import GraphBiNet

class Test(TestCase):
    def test_best_path(self):
        # constants
        nNode = 30
        rho = 2

        numNet = 3
        numDest = 6

        seed = None
        numSeedDig = 3

        SetSeed(None)
        seedL = [random.randint(0, 10**numSeedDig - 1) for _ in range(numNet)]

        # loop over the networks
        for netNum in range(numNet):
            # make network
            r = MakeNet.R(nNode,rho)

            seed = SetSeed(seedL[netNum])

            net = RandNetCirc(nNode, r)
            nodeLoc,linkL = net

            source = random.randint(0, len(nodeLoc) - 1)

            # visualize net
            fig, ax = plot.subplots(figsize=(6.5, 6.5))
            print(f'seed: {seed}')
            GraphBiNet(ax, net, True, True, nodeNum=[k for k in range(nNode)])
            plot.title(f'N = {nNode}; Seed = {seed}')

            fileName = f'BestPath/best_path_{nNode}_{seed}_cost'
            plot.savefig(fileName, dpi=200)
            plot.show()

            # build ground truth
            linkCost = [Cost.R(nodeLoc[n0], nodeLoc[n1]) for (n0, n1) in linkL]
            cost,back = DijkstraFor(net, source, linkCost)

            # Do tests
            posDest = [k for k in range(nNode)]
            posDest.pop(source)
            destL = random.sample(posDest, k=numDest)
            print(f'srouce = {source}, dest = {destL}')

            for dest in destL:
                turePath = DijkstraBack(back, source,dest)
                compPath = BestPath(net, source,dest, linkCost)
                self.assertEqual(turePath,compPath)
