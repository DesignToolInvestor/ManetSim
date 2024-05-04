#
# d i s t _ b . p y
#

from matplotlib import pyplot as plot
from random import uniform

from LocUtil import Grid1, SetSeed
import Dist


###############################################################
if __name__ == "__main__":
  # constants
  xRange = (0,2)

  nPlotPoint = 100
  fileName = 'dist_b.png'

  # setup
  dist = Dist.ExampB()

  # graph the CDF
  fig,ax = plot.subplots(figsize=(9, 6.5))

  xL = Grid1(*xRange, nPlotPoint)
  yL = [dist.Cdf(x) for x in xL]
  plot.plot(xL, yL, c="Blue")

  plot.savefig(fileName)
