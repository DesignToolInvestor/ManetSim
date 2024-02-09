#
# t e s t _ I n d e p e n d S l o w . p y
#

from unittest import TestCase

from IndependSlow import IndSubSet as SubSetSlow
from IndependPrune import IndSubSet as SubSetPrune
from LocUtil import ListEq
from Graph import ReadGraph

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
