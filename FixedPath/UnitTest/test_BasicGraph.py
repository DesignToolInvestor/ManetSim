#
# t e s t _ B a s i c G r a p h . p y
#

from unittest import TestCase

from math import isclose

from BasicGraph import FracCover, FracPack
from LocMath import IsClose, RealToFrac


class Test(TestCase):
    def test_FracPack(self):
        graph = (5, [(0, 1), (0, 4), (1, 2), (1, 4), (2, 3), (3, 4)])

        weight = FracPack(graph)
        weight = [float(w) for w in weight]

        ans = [1/2, 1/2, 1/2, 1/2, 1/2]
        self.assertTrue(IsClose(ans, weight))


    def test_FracCover(self):
        graph = (5, [(0, 1), (0, 4), (1, 2), (1, 4), (2, 3), (3, 4)])

        weight = FracCover(graph)
        weight = [float(w) for w in weight]

        coverNum = sum(weight)
        self.assertTrue(isclose(5/2, coverNum))
