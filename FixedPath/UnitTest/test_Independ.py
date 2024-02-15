#
# t e s t _ I n d e p e n d S l o w . p y
#

from random import sample
from unittest import TestCase

from BestPath import BestPath
import Cost
from Graph import ReadGraph
from IndependSlow import IndSubSet as SubSetSlow
from IndependPrune import IndSubSet as SubSetPrune
from Interfere import PathSelfInter
from LocUtil import ListEq, SetSeed
import MakeNet
from MakeNet import RandNetCirc

class Test(TestCase):
    def test_IndSubSetSlowA(self):
        graph = ReadGraph("interfere_a.graph")

        result = SubSetSlow(graph)
        ans = [[0, 3], [0], [1], [2], [3]]

        self.assertTrue(ListEq(ans, result))

    def test_IndSubSetSlowB(self):
        graph = ReadGraph("interfere_b.graph")

        result = SubSetSlow(graph)
        ans = [[0], [1], [2], [3], [4], [0,2], [0,3], [1,3], [2,4]]

        self.assertTrue(ListEq(ans, result))

    def test_IndSubSetPruneA(self):
        graph = ReadGraph("interfere_a.graph")

        result = SubSetPrune(graph)
        ans = [[0], [1], [2], [3], [0, 3]]

        self.assertTrue(ListEq(ans, result))

    def test_IndSubSetPruneB(self):
        graph = ReadGraph("interfere_b.graph")

        result = SubSetPrune(graph)
        ans = [[0], [1], [2], [3], [4], [0, 2], [0, 3], [1, 3], [2, 4]]

        self.assertTrue(ListEq(ans, result))

    def test_Same(self):
        # constants
        netSize = 200
        rho = 2
        maxNHops = 25

        seed = None

        gamma = 2.0
        snir = 1

        # gen problem
        seed = SetSeed(seed)
        netR = MakeNet.R(netSize, rho)

        net = RandNetCirc(netSize, netR)
        nodeLoc,link = net

        pathEnd = sample(range(netSize), k=2)

        # get path
        linkCost = [Cost.R(nodeLoc[n0], nodeLoc[n1]) for (n0,n1) in link]
        path = BestPath(net, *pathEnd, linkCost)

        if (path is not None):
            nHops = len(path)

            if (len(path) <= maxNHops):
                # make interference graph
                interfearGraph = (nHops, PathSelfInter(net,path,gamma,snir))

                # compair two subsets
                sortKey = lambda p: [len(p), p]
                slowSubSet = sorted(SubSetSlow(interfearGraph), key=sortKey)
                pruneSubSet = sorted(SubSetPrune(interfearGraph), key=sortKey)

                print(f'nHops = {nHops}, nSubSet = {len(pruneSubSet)}')

                good = (slowSubSet == pruneSubSet)
                if not good:
                    self.fail(f'seed = {seed}')
