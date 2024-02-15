#
# t e s t _ c l i c k . p y
#

from unittest import TestCase

from random import shuffle

from ClickSlow import Click as ClickSlow
from ClickPrune import Click as ClickPrune
from LocUtil import SetEq


class Test(TestCase):
    def test_ClickA(self):
        link = [[0,1], [1,2], [1,3], [2,3]]
        graph = (4, link)

        ans = [(0,), (1,), (2,), (3,), (0, 1), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
        shuffle(ans)
        ans = tuple(ans)

        resultSlow = ClickSlow(graph)
        resultPrune = ClickPrune(graph)

        self.assertTrue(SetEq(ans, resultSlow))
        self.assertTrue(SetEq(ans, resultPrune))

    def test_ClickB(self):
        link = [[0,1], [0,5], [1,2], [1,5], [2,3], [2,4], [3,4], [4,5]]
        graph = (6, link)

        result = ClickSlow(graph)

        ans = (
            (0,), (1,), (2,), (3,), (4,), (5,),
            (0,1), (0,5), (1,2), (1,5), (2,3), (2,4), (3,4), (4,5),
            (0,1,5), (2,3,4)
         )
        self.assertTrue(SetEq(ans, result))

    def test_ClickC(self):
        link = [[0,1], [0,2], [0,4], [1,2], [1,4], [2,3], [2,4], [3,4]]
        graph = (5, link)

        result = ClickSlow(graph)

        ans = (
            (0,), (1,), (2,), (3,), (4,),
            (0, 1), (0,2), (0, 4), (1, 2), (1, 4), (2, 3), (2, 4), (3,4),
            (0,1,2), (0,1,4), (0,2,4), (1,2,4), (2,3,4),
            (0,1,2,4)
        )
        self.assertTrue(SetEq(ans, result))