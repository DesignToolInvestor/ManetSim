#
# t e s t _ S i n c . p y
#

from unittest import TestCase

from math import cos, log, pi
from sympy import Symbol

from Map import LogRatio
from Sinc import QuadSikorski


class Test(TestCase):
  def test_QuadSikorski_0a(self):
    rateLim = 9

    Func = lambda x: 3 / 4 * x * (2 - x) * (1 - cos(3 / 2 * pi * x))

    xSym = Symbol('x')
    zSym = Symbol('z')
    map_ = LogRatio( xSym,zSym, (0,2))

    approxLim = (-2,4)
    epsL = tuple(10**p for p in range(-2,-10,-1))

    for eps in epsL:
      est,quadInfo = QuadSikorski(Func, map_, approxLim, eps=eps)
      _,_,n = quadInfo

      if (eps < abs(1 - est)) or (-rateLim * log(eps) < n):
        print(quadInfo)
        self.fail()
