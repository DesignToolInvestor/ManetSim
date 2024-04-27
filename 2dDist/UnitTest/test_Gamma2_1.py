#
# t e s t _ G a m m a 2 _ 1 . p y
#

from unittest import TestCase

from random import uniform

from LocUtil import SetSeed
import Gamma2_1

class Gamma2_1Test(TestCase):
  def test_CDF_0a(self):
    seed = SetSeed()
    nSamp = 50
    xL = [uniform(0,8) for _ in range(nSamp)]
    yL = [Gamma2_1.Cdf(x) for x in xL]
    xEstL = [Gamma2_1.InvCdf(y) for y in yL]

    err = [abs(xEst - x) for (xEst,x) in zip(xEstL,xL)]
    relErr = [e/x for (e,x) in zip(err,xL)]
    maxRelErr = max(relErr)

    self.assertTrue(maxRelErr < 1e-12)
