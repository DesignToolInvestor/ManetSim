#
# M a p . p y
#

# This file creates the most common maps

from attrs import define, field
from collections import namedtuple
from math import exp, log

@define
class Map:
  z0 = field()
  xRange = field()

  forward = field()
  inverse = field()
  deriv = field()


class LogRatio(Map):
  def __init__(self, xRange=(0,1), z0=None):
    xMin,xMax = xRange

    if z0 is None:
      z0 = (xMin + xMax) / 2
    elif (z0 < xMin) or (xMax < z0):
      raise Exception('Point that maps to zero must be within xRange')

    forwardF = lambda x: log((x - xMin) / (xMax - x)) - z0
    inverseF = lambda z: (xMax - xMin) * exp(z + z0) / (1 + exp(z + z0)) + xMin
    derivF = lambda x: (xMax - xMin) / (x - xMin) / (xMax - x)

    super().__init__(z0, xRange, forwardF,inverseF, derivF)
