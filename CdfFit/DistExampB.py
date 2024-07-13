#
# D i s t E x a m p B . p y
#

# This file creates a distribution of type "Example B".  Because Python uses "Duck Typing",
# there is no master class that defines a distribution type.

import sympy as sp
from math import cos, pi, sin

import Dist


class ExampB(Dist.BiSectDist):
  def __init__(self, xLabel='x'):
    self.xSym = sp.Symbol(xLabel)

    # TODO:  Make this general
    self.a = 0
    self.b = 2

    self.pdfSym = 3 * self.xSym * (2 - self.xSym) / 4 * (1 - sp.cos(3 * sp.pi * self.xSym / 2))

  def Pdf(self, x):
    y = 3 / 4 * x * (2 - x) * (1 - cos(3 / 2 * pi * x))
    return y

  def Cdf(self, x):
    t1 = x ** 2
    t5 = pi ** 2
    t9 = (3 * pi * x) / 2
    t10 = sin(t9)
    t13 = cos(t9)
    t25 = \
      (t10 * (-16 + t5 * (18 * t1 - 36 * x)) -
       9 * pi * ((8 * t13 * (-x + 1)) / 3 - 8 / 3 + t5 * (x - 3) * t1)) / \
      (36 * t5 * pi)

    return t25