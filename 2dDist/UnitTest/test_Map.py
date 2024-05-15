#
# t e s t _ M a p . p y
#

from unittest import TestCase

from sympy import Symbol, exp, log

from Map import LogRatio
from LocMath import SymEq


class TestLogRatio(TestCase):
  def test_MapExp_0a(self):
    x = Symbol('x')
    z = Symbol('z')
    map = LogRatio(x,z)

    mapExp = map.MapExp()
    mapAns = log(x / (1 - x))
    self.assertTrue(SymEq(mapExp,mapAns))

    invExp = map.InvExp()
    invAns = exp(z) / (1 + exp(z))
    self.assertTrue(SymEq(invExp,invAns))

  def test_MapExp_0b(self):
    x = Symbol('x')
    z = Symbol('z')
    map = LogRatio(x,z, (-1,1))

    mapExp = map.MapExp()
    mapAns = log((x + 1) / (1 - x))
    self.assertTrue(SymEq(mapExp,mapAns))

    invExp = map.InvExp()
    invAns = (exp(z) - 1) / (1 + exp(z))
    self.assertTrue(SymEq(invExp,invAns))

  def test_MapExp_0c(self):
    x = Symbol('x')
    z = Symbol('z')
    map = LogRatio(x,z, (0,2), 1)

    mapExp = map.MapExp()
    mapAns = log(x / (2 - x)) - 1
    self.assertTrue(SymEq(mapExp,mapAns))

    invExp = map.InvExp()
    invAns = 2*exp(z + 1) / (1 + exp(z + 1))
    self.assertTrue(SymEq(invExp,invAns))

  def test_MapExp_0d(self):
    x = Symbol('x')
    z = Symbol('z')
    map = LogRatio(x, z, (-1, 0), -1, 2)

    mapExp = map.MapExp()
    mapAns = 2 * (log(-(x + 1) / x) + 1)
    self.assertTrue(SymEq(mapExp, mapAns))

    invExp = map.InvExp()
    invAns = -1 / (1 + exp(z/2 - 1))
    self.assertTrue(SymEq(invExp, invAns))

  def test_InvExp_0a(self):
    self.fail()

  def test_deriv(self):
    self.fail()
