#
#  C d f F i t 1 . p y
#

from math import exp, log

from LocUtil import Sub


def EstAsym(sampX, probMap):
  sampZ = [probMap.Forward(x) for x in sampX]


# TODO:  add scaling so as to minimize the RMS residual
# TODO:  create a higher level function that maximizes n without overfitting
def CdfFit1(sampX, probMap):
  # process arguments
  nSamp = len(sampX)
  sampSort = sorted(sampX)

  # map samples to z
  sampZ = tuple(probMap.Forward(x) for x in sampSort)

  # compute the quantile
  quant = [(k + 0.5)/nSamp for k in range(nSamp)]

  # estimate the asymtotes
  nEnd = round(0.15 * nSamp)

  leftIndex = range(nEnd)
  leftSampZ = Sub(sampZ, leftIndex)
  rightLogQ = log(Sub(quant, leftIndex))
  a1,a0 = ToLimProj(leftSampZ, rightLogQ)

  rightIndex = range(nSamp - nEnd - 1, nSamp)
  b1,b0 = ToLimProj(Sub(sampSort, rightIndex), Sub(quant, rightIndex))

  return (a0,a1, b0,b1)
