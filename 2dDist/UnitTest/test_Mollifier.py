#
# t e s t _ M o l l i f i e r . p y
#

from unittest import TestCase

from math import isclose

from Mollifier import Hermite, MolSet

class HermiteTest(TestCase):
  def test_Hermite_0a(self):
    result = Hermite((1,0),(0,), (0,1))
    ans = [1,0,-1]
    ok = all(isclose(a,r) for (a,r) in zip(ans,result))
    self.assertTrue(ok)

  def test_Hermite_0b(self):
    result = Hermite((0,1),(0,), (0,1))
    ans = [0,1,-1]
    ok = all(isclose(a,r) for (a,r) in zip(ans,result))
    self.assertTrue(ok)

  def test_Hermite_0c(self):
    result = Hermite((0, 0), (1,), (0, 1))
    ans = [0, 0, 1]
    ok = all(isclose(a, r) for (a, r) in zip(ans, result))
    self.assertTrue(ok)

  def test_Hermite_0d(self):
    result = Hermite((1,0),(0,0), (-1,1))
    ans = [1/2, -3/4, 0, 1/4]
    ok = all(isclose(a,r) for (a,r) in zip(ans,result))
    self.assertTrue(ok)

  def test_Hermite_0e(self):
    result = Hermite((0,1),(0,0), (-1,1))
    ans = [1/4, -1/4, -1/4, 1/4]
    ok = all(isclose(a,r) for (a,r) in zip(ans,result))
    self.assertTrue(ok)

  def test_Hermite_0f(self):
    result = Hermite((0, 0), (1,0), (-1, 1))
    ans = [1/2, +3/4, 0, -1/4]
    ok = all(isclose(a, r) for (a, r) in zip(ans, result))
    self.assertTrue(ok)

  def test_Hermite_0g(self):
    result = Hermite((0, 0), (0,1), (-1, 1))
    ans = [-1/4, -1/4, 1/4, 1/4]
    ok = all(isclose(a, r) for (a, r) in zip(ans, result))
    self.assertTrue(ok)

class MolSetTest(TestCase):
  def Match(self, a,b):
    for (a,b) in zip(a,b):
      if type(a) == list:
        self.Match(a,b)
      elif not isclose(a,b):
        self.fail()

  def test_MolSet_0a(self):
    result = MolSet((1,0),(0,1))
    ans = [[1,0,-1], [0,1,-1], [0, 0, 1]]
    self.Match(ans,result)

  def test_MolSet_0b(self):
    result = MolSet((1,1),(-1,0))
    ans = [[0,0,3,2], [0,0,1,1], [1,0,-3,-2], [0,1,2,1]]
    self.Match(ans,result)