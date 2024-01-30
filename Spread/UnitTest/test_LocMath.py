#
# t e s t _ L o c M a t h . p y
#

from unittest import TestCase

import random

import LocMath
import LocUtil


class Test(TestCase):
    def test_RealToTest(self):
        # constants
        numOfTest = 300

        # do seed
        seed = None
        seed = LocUtil.SetSeed(seed)

        # do tests
        for i in range(numOfTest):
            real = random.random()
            frac = LocMath.RealToFrac(real)
            diff = real - float(frac)

            self.assertTrue(abs(diff) < 1e6, f'seed was {seed}')
