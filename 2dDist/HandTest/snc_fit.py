#
# s i n g _ f i t . p y
#
import random
from math import exp, log
from matplotlib import pyplot as plot
from random import uniform, gauss

from Sinc import SincFit
from LocUtil import Grid1, UnZip, MinMax

if __name__ == "__main__":
  # constants
  nSamp = 50
  noiseLev = 0.02

  nPlotPoint = 150

  func = lambda x: x * (1-x)
  phi = lambda x: log(x / (1 - x))

  # compute samples
  sampX = [uniform(0,1) for _ in range(nSamp)]
  sampVal = [func(x) + gauss(0,noiseLev) for x in sampX]
  sampZ = [phi(x) for x in sampX]

  zRange = MinMax(sampZ)

  samp = list(zip(sampZ,sampVal))
  fit = SincFit(samp, zRange,6)

  # do plot
  fig,ax = plot.subplots()

  # plot sinc points
  plot.plot(fit.sincPoint, fit.weight, 'o', c="maroon", markersize=12, zorder=1)
  
  # plot sinc estimation
  zGrid = Grid1(*zRange, nPlotPoint)
  interp = fit.Interp(zGrid)
  plot.plot(zGrid,interp, c="maroon", zorder=1)

  # plot true function
  valL = [exp(z) / (1 + exp(z))**2 for z in zGrid]
  plot.plot(zGrid, valL, c="Blue", zorder=0)

  # plot samples
  plot.plot(*UnZip(samp), 'o', c="Blue", zorder=0)

  # annotate  
  plot.xlabel('z')

  plot.show()
