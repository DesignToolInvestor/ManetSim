#
# t e s t _ D i s t A . p y
#

import numpy as np
from unittest import TestCase

from math import isclose
from sympy import Symbol, exp

from Mollifier import Hermite, MolSetZ
from LocUtil import Grid1
import DistA


class DistATest(TestCase):
  nPoint = 50

  def IsClose(self, aL, bL):
    self.assertEqual(len(aL), len(bL))

    for (a, b) in zip(aL, bL):
      if not isclose(a, b):
        self.fail()

  def test_DistA_0a(self):
    a = 0.3

    xL = Grid1(0, 1, DistATest.nPoint)
    result = tuple(DistA.PdfNum(x, a) for x in xL)
    ans = tuple(0.3 + 1.4 * x for x in xL)

    self.IsClose(result, ans)

  def test_DistA_0b(self):
    prob = DistA.PdfNum(0.6, 0.7)
    if (type(prob) != float):
      self.fail()

    # TODO:  fix so that this is np.float32
    prob32 = DistA.PdfNum(np.float32(0.6), np.float32(0.7))
    if (type(prob32) != np.float64):
      self.fail()

    cum = DistA.CdfNum(0.6, 0.7)
    if (type(cum) != float):
      self.fail()

    cumb32 = DistA.PdfNum(np.float32(0.6), np.float32(0.7))
    if (type(cumb32) != np.float64):
      self.fail()

    x = DistA.InvCdfNum(0.6, 0.7)
    if (type(x) != float):
      self.fail()

    x = DistA.PdfNum(np.float32(0.6), np.float32(0.7))
    if (type(x) != np.float64):
      self.fail()

    x = DistA.GenSamp(0.3)
    if (type(x) != float):
      self.fail()

    x = DistA.GenSamp(np.float32(0.3))
    if (type(x) != np.float64):
      self.fail()