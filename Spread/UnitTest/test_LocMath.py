#
# t e s t _ L o c M a t h . p y
#

import math
from math import pi
from unittest import TestCase
import random

import LocMath
from LocUtil import SetEq, SetSeed

class Test(TestCase):
    # test fractions between o and 1
    def test_RealToTest_a(self):
        # constants
        numOfTest = 300

        # do seed
        seed = None
        seed = SetSeed(seed)

        # do tests
        for i in range(numOfTest):
            real = random.random()
            frac = LocMath.RealToFrac(real)
            diff = real - float(frac)

            self.assertTrue(abs(diff) < 1e6, f'seed was {seed}')

    # TODO: add RealToFrac test for numbers approaching zero

    # test mixed fractions
    def test_RealToTest_b(self):
        # constants
        numOfTest = 300
        numer = 2*3*5*7*11
        maxNum = 99

        # do seed
        seed = None
        seed = SetSeed(seed)

        # do tests
        for i in range(numOfTest):
            real = random.randint(0, (maxNum - 1)*numer)/numer + 1 + random.random()/1e8
            frac = LocMath.RealToFrac(real)
            diff = real - float(frac)

            self.assertTrue(abs(diff) < 1e6, f'seed was {seed}')

    def test_IsClose(self):
        list0 = [1,2,3,4,5,6]
        list1 = [1.000_001, 1.999_999, 3.000_002, 3.999_998, 5.000_003, 5.999_997]
        self.assertTrue(LocMath.IsClose(list0, list1, 1e-5))


    def test_LogRange(self):
        result = LocMath.LogRange(2.9, 49, [1,2,3,5])
        self.assertTrue(LocMath.IsClose(result, [3.0, 5.0, 10.0, 20.0, 30.0, 50.0]))

        result = LocMath.LogRange(1.1, 31, [1,2,3,5])
        self.assertTrue(LocMath.IsClose(result, [1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 30.0]))

        result = LocMath.LogRange(0.06, 1.5, [1,2,3,5])
        self.assertTrue(LocMath.IsClose(result, [0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 2.0]))


    def test_Wrap(self):
        # constants
        listLen = 10

        # set seed
        seed = None
        seed = SetSeed(seed)

        # setup list
        list_ = [random.random() for _ in range(listLen)]
        rem = [v % 1 for v in list_]
        truth = [r if r < 0.5 else r - 1 for r in rem]

        # do test
        result = LocMath.Wrap(list_, -0.5, 0.5)

        self.assertTrue(LocMath.IsClose(truth, result), f'Seed = {seed}')

    def test_CircDiff(self):
        case0 = [0, 3, 7, 5]
        self.assertTrue([3,4,-1,-5], LocMath.CircDiff(case0))


    def test_MaxGapAng(self):
        deg = [0, 22, 105, -170, -55]
        rad = [d * pi/180 for d in deg]
        ansDeg = 247.5
        ansRad = ansDeg * pi/180

        self.assertTrue(math.isclose(ansRad , LocMath.CircDiff(rad)))

    def test_PowerSet(self):
        result = LocMath.PowerSet(3)
        ans = [[], [0], [1], [2], [0,1], [0,2], [1,2], [0,1,2]]

        self.assertTrue(SetEq(ans, result))

    def test_PowerSetTup(self):
        result = LocMath.PowerSetTup(3)
        ans = ((), (0,), (1,), (2,), (0,1), (0,2), (1,2), (0,1,2))

        self.assertTrue(SetEq(ans, result))