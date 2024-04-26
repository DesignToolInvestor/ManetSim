#
# t e s t _ M o l l i f i e r . p y
#

from unittest import TestCase

from math import isclose

from Mollifier import Hermite

class Test(TestCase):
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