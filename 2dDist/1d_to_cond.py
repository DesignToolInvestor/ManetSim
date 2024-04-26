#
# 1 d _ t o _ c o n d . p y
#

from scipy.special import lambertw
from math import exp
from matplotlib import pyplot as plot
from random import uniform

from LocUtil import Grid1


#####################################################
# These functions deal with the distribution Gamma distribution where shape (alpha) = 2 and rate
# (beta) = 1.  That is PDF = x * exp(-x)
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




###########################
if __name__ == "__main__":
  # constants
  nSamp = 75
  nPlotPoint = 50
  xRange = (0,7)

  # synthetic data
  samp = [Sample() for _ in range(nSamp)]

  # plot CDF
  fig,ax = plot.subplots()

  y = [(k + 0.5)/nSamp for k in range(nSamp)]
  plot.plot(sorted(samp), y, '*', c="Maroon", label="samples", zorder=1)

  xL = Grid1(*xRange, nPlotPoint)
  yL = tuple(Cdf(x) for x in xL)
  plot.plot(xL,yL, c="Blue", label="cdf", zorder=0)

  plot.xlabel('Value')
  plot.ylabel('Quantile')

  plot.show()

  # estimated the distribution
