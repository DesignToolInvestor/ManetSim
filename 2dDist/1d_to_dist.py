#
# 1 d _ t o _ d i s t . p y
#

from math import asinh, exp, log, sinh, sqrt
from matplotlib import pyplot as plot

import Gamma2_1
from LocUtil import Grid1
from Mollifier import MolSet
from Sinc import Map


###########################
if __name__ == "__main__":
  # constants
  nSamp = 75
  nPlotPoint = 50
  xRange = (0,7)

  # synthetic data
  samp = [Gamma2_1.Sample() for _ in range(nSamp)]
  quant = [(k + 0.5)/nSamp for k in range(nSamp)]

  sampSort = sorted(samp)

  # plot CDF
  fig,ax = plot.subplots(3, figsize=(6.5, 9))

  ax[0].plot(sampSort, quant, '*', c="Maroon", label="samples", zorder=1)

  xL = Grid1(*xRange, nPlotPoint)
  yL = tuple(Gamma2_1.Cdf(x) for x in xL)
  ax[0].plot(xL,yL, c="Blue", label="cdf", zorder=0)

  ax[0].set_xlabel('Value')
  ax[0].set_ylabel('Quantile')

  # plot CDF minus mollifiers
  molSet = MolSet((0,0), (0,1))

  molF = lambda x: x
  unitInv = lambda z: exp(z) / (exp(z) + 1)

  phi = lambda x: log(sinh(x))
  phiInv = lambda z: asinh(exp(z))
  map = Map(phi,phiInv)

  shiftQuant = [q - molF(unitInv(map.For(s))) for (q,s) in zip(quant,sampSort)]
  ax[1].plot(sampSort, shiftQuant, '*', c="Maroon", label="samples", zorder=1)

  xL = Grid1(*xRange,nPlotPoint)
  res = [1 - (x + 1) * exp(-x) - sinh(x) / (sinh(x) + 1) for x in xL]
  ax[1].plot(xL, res, c="Blue", label="cdf", zorder=0)

  # plot CDF minus mollifiers in z
  mapSamp = [map.For(s) for s in sampSort]

  ax[2].plot(mapSamp, shiftQuant, '*', c="Maroon", label="samples", zorder=1)

  # plot function to be estimated by sinc series
  mapSamp = [map.For(s) for s in sampSort]

  ax[2].plot(mapSamp, shiftQuant, '*', c="Maroon", label="samples", zorder=1)

  zL = Grid1(-8,8, nPlotPoint)
  resStrip = [
    1 - (asinh(exp(z)) + 1) / (exp(z) + sqrt(1 + exp(2*z))) - exp(z) / (exp(z) + 1)
  for z in zL]

  ax[2].plot(zL, resStrip, c="Blue", label="cdf", zorder=0)

  # plot function to be estimated by sinc series
  mapSamp = [map.For(s) for s in sampSort]

  ax[2].plot(mapSamp, shiftQuant, '*', c="Maroon", label="samples", zorder=1)

  zL = Grid1(-8,8, nPlotPoint)
  resStrip = [
    1 - (asinh(exp(z)) + 1) / (exp(z) + sqrt(1 + exp(2*z))) - exp(z) / (exp(z) + 1)
  for z in zL]

  ax[2].plot(zL, resStrip, c="Blue", label="cdf", zorder=0)

  # save the figure
  plot.savefig('1d_dist.png')
