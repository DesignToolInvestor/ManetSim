#
# t e s t _ M o l l i f i e r . p y
#

from unittest import TestCase

from math import isclose
from sympy import Symbol, exp

from Mollifier import Hermite, MolSetZ


##########################################################
class HermiteTest(TestCase):
  def SymMatch(self, a, b):
    if (a - b).simplify() != 0:
      self.fail()

  def test_Hermite_0a(self):
    y = Symbol('y')
    result = Hermite((1,0),(0,), (0,1), y)
    ans = -y*y + 1
    self.SymMatch(result, ans)

  def test_Hermite_0b(self):
    y = Symbol('y')
    result = Hermite((0,1),(0,), (0,1), y)
    ans = (-y + 1)*y
    self.SymMatch(result, ans)

  def test_Hermite_0c(self):
    y = Symbol('y')
    result = Hermite((0, 0), (1,), (0, 1), y)
    ans = [0, 0, 1]
    ans = y*y
    self.SymMatch(result, ans)

  def test_Hermite_0d(self):
    y = Symbol('y')
    result = Hermite((1,0),(0,0), (-1,1), y)
    ans = [1/2, -3/4, 0, 1/4]
    ans = (((y * y) - 3)*y + 2) / 4
    self.SymMatch(result, ans)

  def test_Hermite_0e(self):
    y = Symbol('y')
    result = Hermite((0,1),(0,0), (-1,1), y)
    ans = [1/4, -1/4, -1/4, 1/4]
    ans = (((y - 1)*y - 1)*y + 1) / 4
    self.SymMatch(result, ans)

  def test_Hermite_0f(self):
    y = Symbol('y')
    result = Hermite((0, 0), (1,0), (-1, 1), y)
    ans = [1/2, +3/4, 0, -1/4]
    ans = ((-y*y + 3)*y + 2) / 4
    self.SymMatch(result, ans)

  def test_Hermite_0g(self):
    y = Symbol('y')
    result = Hermite((0, 0), (0,1), (-1, 1), y)
    ans = [-1/4, -1/4, 1/4, 1/4]
    ans = (((y + 1) * y - 1) * y - 1) / 4
    self.SymMatch(result, ans)


class MolSetTest(TestCase):
  def SymMatch(self, aL, bL):
    for (a,b) in zip(aL,bL):
      if (a - b).simplify() != 0:
        self.fail()

  def test_MolSet_0a(self):
    z = Symbol('z')
    result = MolSetZ(z, (1,0))
    ans = [
      (2*exp(z) + 1) / (1 + exp(z))**2, (exp(z)) / (1 + exp(z))**2, (exp(2*z)) / (1 + exp(z))**2
    ]
    self.SymMatch(ans, result)

  def test_MolSet_0b(self):
    z = Symbol('z')
    result = MolSetZ(z, (1,1))
    ans = [
      (3*exp(z) + 1) / (1 + exp(z)) ** 3,
      exp(z) / (1 + exp(z)) ** 3,
      exp(2*z) * (exp(z) + 3) / (1 + exp(z)) ** 3,
      -exp(2*z) / (1 + exp(z)) ** 3
    ]
    self.SymMatch(ans, result)