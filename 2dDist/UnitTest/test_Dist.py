#
# t e s t _ Dist. p y
#

from unittest import TestCase

# system packages
from random import uniform
from matplotlib import pyplot as plot

# local files
from LocUtil import Grid1, SetSeed
import Dist


class Erling2_1Test(TestCase):
  def test_Erling2_1_0a(self):
    nSamp = 50
    seed = SetSeed()
    dist = Dist.Erlang2_1

    xL = [uniform(0,8) for _ in range(nSamp)]
    yL = [dist.Cdf(x) for x in xL]
    xEstL = [dist.InvCdf(y) for y in yL]

    err = [abs(xEst - x) for (xEst,x) in zip(xEstL,xL)]
    relErr = [e/x for (e,x) in zip(err,xL)]
    maxRelErr = max(relErr)

    if 1e-12 <= maxRelErr:
      print(f'Erling2_1_0a test failed (seed = {seed})')
      self.fail()

class DistATest(TestCase):
  def test_ExampA_0a(self):
    nSamp = 50
    seed = SetSeed()
    dist = Dist.ExampA

    xL = [uniform(0,1) for _ in range(nSamp)]
    yL = [dist.Cdf(x) for x in xL]
    xEstL = [dist.InvCdf(y) for y in yL]

    err = [abs(xEst - x) for (xEst,x) in zip(xEstL,xL)]

    relErr = [e/x for (e,x) in zip(err,xL)]
    maxRelErr = max(relErr)

    if 1e-12 <= maxRelErr:
      print(f'Erling2_1_0a test failed (seed = {seed})')
      self.fail()

