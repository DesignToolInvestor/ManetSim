#
# D i s t . p y
#

# This file creates base classes for use in creating distribution classes.

from random import random
from LocMath import Bisect


class Dist(object):
  def Sample(self):
    y = random()
    return self.InvCdf(y)

class BiSectDist(Dist):
  def InvCdf(self, y, tol=1e-14):
    x = Bisect(self.Cdf, y, (0, 2), tol=tol)
    return x
