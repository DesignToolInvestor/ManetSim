#
# t e s t _ I n d e x P o o l . p y
#

from unittest import TestCase

import random
import enum

import LocUtil
import IndexPool

###################################################################################################
class TestIndexPool(TestCase):
    def setUp(self):
        self.indexPool = IndexPool.IndexPool(10)

class Basic(TestIndexPool):
    def test_push(self):
        for i in range(10):
            self.indexPool.Push(i)
        expectedPool = [k for k in range(10)]
        self.assertEqual(self.indexPool.pool, expectedPool)

    def test_pop_end(self):
        for i in range(10):
            self.indexPool.Push(i)
        for i in range(9, -1, -1):
            value = self.indexPool.Pop()
            self.assertEqual(value, i)
        value = self.indexPool.Pop()
        self.assertEqual(value,None)

    def test_drop(self):
        for i in range(10):
            self.indexPool.Push(i)
        for i in range(10):
            value = self.indexPool.Drop(i)
        self.assertEqual(self.indexPool.pool, [])

# TODO:  Increase the size of the index
class Shuffle(TestIndexPool):
    def test_pool(self):
        # Helper function
        # TODO:  Think about the best way to avoid nexted methods
        def Check(trueMask, calcList):
            tureList = []
            for i in range(10):
                if trueMask[i]:
                    tureList.append(i)

            calcCopy = self.indexPool.pool.copy()
            calcCopy.sort()

            self.assertEqual(calcCopy, tureList)

        # load index pool
        seed = LocUtil.SetSeed()
        active = []
        for i in range(10):
            coinFlip = random.choices([True,False])[0]
            active.append(coinFlip)
            if coinFlip:
                self.indexPool.Push(i)
        Check(active, self.indexPool.pool)

        # shuffle stuff around
        # TODO:  use the Enum package
        for i in range(50):
            op = random.randint(0,2)

            match op:
                case 0:     # do push
                    i = random.randint(0, 9)
                    active[i] = True
                    self.indexPool.Push(i)
                    Check(active, self.indexPool.pool)
                case 1:     # do pop
                    i = self.indexPool.Pop()
                    if i != None:
                        active[i] = False
                        Check(active, self.indexPool.pool)
                case 2:     # do drop
                    activeL = LocUtil.MaskToIndex(active)
                    if len(activeL) > 0:
                        i = random.choices(activeL)[0]
                        active[i] = False
                        self.indexPool.Drop(i)
                        Check(active, self.indexPool.pool)