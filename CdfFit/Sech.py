#
# S e c h . p y
#

# This file contains functions for preforming Sech approximations.

from math import pi, cosh, sqrt

def Sech(z, h,beta):
  k1 = h ** (1 - beta) / sqrt(pi)
  k2 = h ** (-beta)
  result = k1 / cosh(k2 * z)

  return result
