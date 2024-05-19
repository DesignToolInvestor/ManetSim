#
# S i n c . p y
#

from sympy import Symbol, Function, lambdify, pi, sin
from numpy import sinc

class SincD(Function):
  # TODO: Add check for negative dOrd
  # TODO: Should it evaluate if arg is an integer and dOrd is zero ???
  # TODO: Should we define constants for S(1,k) where k is an integer ???
  @classmethod
  def eval(cls, dOrd, arg):
    if dOrd.is_integer is False:
      raise TypeError('dOrd should be an integer')

  # TODO: mpmath seems to work extra hard around all integers ... would like absolute precision
  # TODO: derive a bound on the error of the series and use it for picking the switch over
  def _eval_evalf(self, prec):
    dOrd,arg = self.args

    if dOrd == 0:
      argVal = (pi*arg)._eval_evalf(prec)
      if 1e-2 < abs(argVal):
        val = (sin(argVal) / argVal)._eval_evalf(prec)
      else:
        piXSqr = pi*pi * arg*arg
        series = ((-piXSqr/5040 + 1/120) * piXSqr - 1/6) * piXSqr + 1
        val = series.evalf(prec)

    return val

  def fdiff(self, argIndex):
    if argIndex != 2:
      raise Exception('differentiation with respect to order of differentiation not supported')

    dOrd,arg = self.args
    return SincD(dOrd + 1, arg)


##################################################################################
class SincApprox(object):
  def __init__(self, map_, zRange, nSinc, sincWeight, nullZ, molZ, molWeight, maxDeriv=0):
    self.map_ = map_

    self.nSinc = nSinc
    minZ,maxZ = zRange
    self.h = (maxZ - minZ) / (nSinc - 1)

    self.sincPointZ = [k * self.h + minZ for k in range(nSinc)]

    self.sincWeight = sincWeight

    self.nullZ = nullZ

    self.molZ = molZ
    self.molWeight = molWeight

    self.maxDeriv = maxDeriv

  def Interp(self, xPoint):
    result = []

    mapF = lambdify(map.XSym(), self.map_.ForExp(), "math")

    for x in xPoint:
      z = mapF(x)

      val = self.molX(x)
      for k in range(self.nSinc):
        val += self.sincWeight[k] * sinc((z - self.sincPointZ[k]) / self.h) * self.nullZ(z)

      result.append(val)

    return result
