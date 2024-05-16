#
# S i n c . p y
#

from sympy import Function, pi, sin

from LocUtil import MinMax

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

class SincBasis(Function):
  @classmethod
  def eval(cls, , arg):
    pass

def DistFit(samp, map, xSym,zSym, nullOrd, asym):
  # parse arguments
  nSamp = len(samp)

  # make CDF
  sampSort = sorted(samp)
  quant = [(k + 0.5) / nSamp for k in range(nSamp)]

  # map to z
  mapF = map.MapExp().lambdafy(xSym)
  zL = [mapF(x) for x in sampSort]

  # shift
  minZ,maxZ = MinMax(z)
  z0 = (maxZ + minZ) / 2

  zS = [z - z0 for z in zL]

  #