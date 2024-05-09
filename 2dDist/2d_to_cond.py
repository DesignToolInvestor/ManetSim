#
# 2 d _ t o _ c o n d . p y
#

from math import log
from random import uniform
from matplotlib import pyplot as plot

from LocMath import Bisect
from LocUtil import UnZip


###############################################################
def XSamp():










def Sample():
  x = XSamp()
  y = YSamp(x)

  return (x,y)


###############################
if __name__ == "__main__":
  # constants
  nSample = 10_000

  xDist =
  # synthetic data
  samp = tuple(Sample() for _ in range(nSample))

  # plot the samples
  plot.subplots(figsize=(6.5, 6.5))

  plot.plot(*UnZip(samp), '.', color='Maroon')

  plot.show()
