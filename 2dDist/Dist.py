#
# D i s t . p y
#

# This file contains several example distributions

from collections import namedtuple
from math import atan2, cos, exp, log, pi, sin, sqrt
from random import uniform
from scipy.special import lambertw

from LocMath import Bisect


###############################################################
class Dist(object):
  def Sample(self):
    y = uniform(0, 1)
    return self.InvCdf(y)


class BiSectDist(Dist):
  def InvCdf(self, y, tol=1e-14):
    x = Bisect(self.Cdf, y, (0, 2), tol=tol)
    return x
  

#######################################
class Uniform(Dist):
  def __init__(self, minX, maxX):
    self.minX = minX
    self.maxX = maxX

  def Pdf(self, x):
    if (self.minX <= x) and (x <= self.maxX):
      y = 1 / (self.maxX - self.minX)
    else:
      y = 0

    return y

  def Cdf(self, x):
    if (x < self.minX):
      y = 0
    elif (self.maxX < x):
      y = 1
    else:
      y = (x - self.minX) / (self.maxX - self.minX)

    return y

  def InvCdf(self, y):
    if (y < 0) or (1 < y):
      raise Exception("probability must be in the range [0,1]")
    else:
      x = y * (self.maxX - self.minX) + self.minX

    return x


#######################################
# This class defines the Erlang Distribution where shape (k) = 2 and rate (lambda) = 1.
# That is PDF = x * exp(-x), and the CDF = 1 - (x + 1)*exp(-x)
class Erlang2_1(Dist):
  def __init__(self):
    pass

  def Pdf(self, x):
    y = x * exp(-x)
    return y

  def Cdf(self, x):
    y = 1 - (1 + x)*exp(-x)
    return y

  def InvCdf(self, y):
    e = exp(1)
    x = -lambertw((y - 1) / e, k=-1) - 1
    return x


#######################################
# Example A

# The PDF for this distribution is 6 * x * (1 - x).  It is a downward facing parabola, goes to zero
# at x=0 and x=1, and has a height of 3/2 at x=1/2.
class Hump(Dist):
  def __init__(self):
    pass

  def Pdf(self, x):
    y = 6 * x * (1 - x)
    return y

  def Cdf(self, x):
    y = (3 - 2*x)*x*x
    return y

  def InvCdf(self, y):
    temp1 = sqrt(y)
    temp3 = sqrt(1 - y)
    temp8 = atan2(2*temp1*temp3, 1 - 2*y)
    temp9 = temp8/3
    temp10 = cos(temp9)
    temp11 = sqrt(3)
    temp12 = sin(temp9)
    x = (temp11*temp12)/2 - temp10/2 + 1/2

    return x

#######################################
# Example B
class ExampB(BiSectDist):
  def __init__(self):
    pass

  def Pdf(self, x):
    y = 3/2 * x * (1-x) * (1 - cos(3/2 * pi * x))
    return y

  def Cdf(self, x):
    t1 = x**2
    t5 = pi**2
    t9 = (3 * pi * x) / 2
    t10 = sin(t9)
    t13 = cos(t9)
    t25 = \
      (t10 * (-16 + t5 * (18 * t1 - 36 * x)) -
        9 * pi * ((8 * t13 * (-x + 1)) / 3 - 8 / 3 + t5 * (x - 3) * t1)) / \
      (36 * t5 * pi)
    
    return t25


#######################################
class SkewHump(BiSectDist):
  def __init__(self):
    pass


  # TODO: Accuracy is probably limited to around 1e-11 (or a little better)
  def _Area(self, k):
    if abs(k - 1) < 0.03:
      result = (k * (k * (k * (k/84 - 31/420) + 27/140) - 19/70) + 1/5) + 3/28
    else:
      result = k * ((k + 1)*log(k) - 2*k + 2) / (k - 1)**3

    return result


  def Pdf(self, x, k):
    area = self._Area(k)
    y =  k * x * (1 - x) / (1 + (k - 1) * x) ** 2 / area

    return y


  def Cdf(self, x, k):
    if abs(k - 1) < 0.03:
      ord0 = (-2*x + 3) * x*x
      ord1 = ((3*x - 6)*x + 3) * x*x
      ord2 = (((-18/5*x + 15/2)*x - 21/5)*x + 3/10) * x*x
      ord3 = (((4*x -42/5)*x + 24/5)*x -2/5) * x*x*x
      ord4 = ((((((-30/7*x + 9)*x - 129/25)*x) + 9/20)*x + 3/350)* - 9/700) * x*x
      ord5 = ((((((9/2*x - 66/7)*x + 9/700)*x - 9/700)*x - 12/25)*x + 27/5)*x + 3/350) * x*x*x

      w = k - 1
      y = ((((ord5*w + ord4)*w + ord3)*w + ord2)*w + ord1)*w + ord0

    else:
      t1 = k ** 2
      t4 = -1 + k
      t5 = x * t4
      t6 = 1 + t5
      t7 = log(t6)
      t16 = log(k)
      y = ((t7 * (t1*x + k - x + 1) - x * (t5 + k + 1) * t4) / ((t16 * (k + 1) - 2 * k + 2) * t6))

    return y