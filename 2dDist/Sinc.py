#
# S i n c . p y
#

from sympy import Function, pi, sin

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