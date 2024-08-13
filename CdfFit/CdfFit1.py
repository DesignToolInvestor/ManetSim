#
#  C d f F i t 1 . p y
#

import sympy as sp
import cvxpy as cp

from math import exp, log


from LocUtil import Grid1, MinMax, Sub


def EstAsym(sampX, map_):
  # process arguments
  nSamp = len(sampX)
  sampSort = sorted(sampX)

  # map samples to z
  sampZ = tuple(map_.Forward(x) for x in sampSort)

  # compute the quantile
  quant = [(k + 0.5)/nSamp for k in range(nSamp)]

  # estimate the asymtotes
  nEnd = round(0.15 * nSamp)

  leftIndex = range(nEnd)
  leftSampZ = Sub(sampZ, leftIndex)
  leftLogQ = log(Sub(quant, leftIndex))
  a1,a0 = ToLimProj(leftSampZ, leftLogQ)

  rightIndex = range(nSamp - nEnd - 1, nSamp)
  rightSampZ = Sub(sampZ, rightIndex)
  rightLoqQ = log(1 - Sub(quant, leftIndex))
  b1,b0 = ToLimProj(rightSampZ, rightLoqQ)

  return (a0,a1, b0,b1)


