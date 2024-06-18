#
# t e s t _ D i s t A . p y
#

from unittest import TestCase

from math import isclose
from dill import load
from sympy import Symbol, exp

from Mollifier import Hermite, MolSetZ
from LocUtil import Grid1

class DistATest(TestCase):
  nPoint = 50
  fileName = '..\\dist_a.dill'

  def IsClose(self, aL, bL):
    self.assertEqual(len(aL), len(bL))

    for (a,b) in zip(aL,bL):
      if not isclose(a,b):
        self.fail()

  def test_DistA_0a(self):
    with open(DistATest.fileName, 'rb') as file:
      distA = load(file)
    a = 0.3

    xL = Grid1(0,1, DistATest.nPoint)
    result = tuple(distA.PdfNum(x,a) for x in xL)
    ans = tuple(0.3 + 1.4*x for x in xL)

    self.IsClose(result, ans)
