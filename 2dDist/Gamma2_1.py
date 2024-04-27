#
# G a m m a 2 _ 1 . p y
#

from random import uniform
from math import exp
from scipy.special import lambertw

# This file defines functions for the Gamma distribution where shape (alpha) = 2 and rate
# (beta) = 1.  That is PDF = x * exp(-x), and the CDF = 1 - (x + 1)*exp(-x)
def Cdf(x):
  y = 1 - (1 + x)*exp(-x)
  return y

def InvCdf(y):
  e = exp(1)
  x = -lambertw((y - 1) / e, k=-1) - 1
  return x

def Sample():
  y = uniform(0,1)
  return InvCdf(y)
