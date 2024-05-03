#
# D i s t . p y
#

# This file contains several example distributions

from collections import namedtuple
from math import atan2, cos, exp, sin, sqrt
from random import uniform
from scipy.special import lambertw


###############################################################
class Dist(object):
  def Sample(self):
    y = uniform(0, 1)
    return self.InvCdf(y)

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
class ExampA(Dist):
  def __init__(self):
    pass

  def Pdf(self, x):
    y = 6*x * (1 - x)
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
