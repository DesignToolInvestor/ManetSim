#
# 1 d _ t o _ d i s t . p y
#

from math import asinh, exp, log, sinh
from matplotlib import pyplot as plot

from Dist import Erlang2_1
from LocUtil import Grid1, MinMax, SetSeed
from Vestigial.Sinc import SincFitNoMap
from Map import

##############################################################################
if __name__ == "__main__":
  # constants
  nSamp = 1_000
  nPlotPoint = 50

  nBase = 6

  givenSeed = None
  seedDig = 3

  # synthetic data
  seed = SetSeed(givenSeed, digits=seedDig)
  if givenSeed is None:
    print(f'Seed = {seed}')

  dist = Erlang2_1()
  samp = [dist.Sample() for _ in range(nSamp)]
  sampQuant = [(k + 0.5)/nSamp for k in range(nSamp)]

  sampSort = sorted(samp)

  # set up problem map
  phi = lambda x: log(sinh(x))
  phiInv = lambda z: asinh(exp(z))
  probMap = Map(phi, phiInv)

  ##############################################################################
  fig,ax = plot.subplots(3, figsize=(6.5, 9))

  #############################
  # plot sorted samples on x with CDF
  ax[0].plot(sampSort, sampQuant, '*', c="Maroon", label="samples", zorder=1)

  minX, maxX = MinMax(sampSort)
  xL = Grid1(minX,maxX, nPlotPoint)
  quant = tuple(dist.Cdf(x) for x in xL)

  ax[0].plot(xL, quant, c="Blue", label="cdf", zorder=0)

  xCent = probMap.Inv(0)
  ax[0].plot((xCent,xCent), (0,1), '--', c="Green")

  ax[0].set_xlabel('X Value')
  ax[0].set_ylabel('Quantile')

  #############################
  # plot samples on z
  sampZ = [probMap.For(s) for s in sampSort]
  ax[1].plot(sampZ, sampQuant, '*', c="Maroon", label="samples", zorder=1)

  minZ,maxZ = probMap.For(minX), probMap.For(maxX)
  zL = Grid1(minZ, maxZ, nPlotPoint)
  zQuantL = tuple(dist.Cdf(probMap.Inv(z)) for z in zL)
  ax[1].plot(zL, zQuantL, c="Blue", label="cdf", zorder=0)

  ax[1].plot((0,0), (0,1), '--', c="Green")

  ax[1].set_xlabel('Z Value')
  ax[1].set_ylabel('Quantile')

  #############################
  # plot samples on shifted z
  zCent = (maxZ + minZ) / 2

  phi = lambda x: probMap.For(x) - zCent
  phiInv = lambda z: probMap.Inv(z + zCent)
  mapShift = Map(phi, phiInv)

  #############################
  # plot samples and CDF on the strip
  sampZ = [mapShift.For(s) for s in sampSort]
  ax[2].plot(sampZ, sampQuant, '*', c="Maroon", label="samples", zorder=1)

  minZs,maxZs = minZ - zCent, maxZ - zCent
  zL = Grid1(minZs, maxZs, nPlotPoint)
  zQuantL = tuple(dist.Cdf(mapShift.Inv(z)) for z in zL)
  ax[2].plot(zL, zQuantL, c="Blue", label="cdf", zorder=0)

  ax[2].plot((minZs, minZs), (0,1), '--', c="Green")
  ax[2].plot((maxZs, maxZs), (0,1), '--', c="Green")

  ax[2].set_xlabel('Shifted Z Value')
  ax[2].set_ylabel('Quantile')

  #############################
  plot.savefig('1d_dist_a.png')

  ##############################################################################
  fig,ax = plot.subplots(3, figsize=(6.5, 9))

  #############################
  # plot the mollifyer and the CDF
  ax[0].plot(xL, quant, c="Maroon")

  molMapFor = lambda y: log(y / (1 - y))
  molMapInv = lambda z: exp(z) / (1 + exp(z))
  molMap = Map(molMapFor,molMapInv)

  molYF = lambda y: y**2
  molXF = lambda x: molYF(molMap.Inv(probMap.For(x)))
  molX = [molXF(x) for x in xL]

  ax[0].plot(xL, molX, c="Blue", label="cdf", zorder=0)

  #############################
  # plot the resitual and the sample residuals
  sampRes = [q - molXF(x) for (x,q) in zip(sampSort,sampQuant)]

  ax[1].plot(sampSort, sampRes, '*', c="Maroon", label="sample residual", zorder=1)

  resX = [q - m for (q,m) in zip(quant,molX)]
  ax[1].plot(xL, resX, c="Blue", label="cdf - mollifyer", zorder=0)

  #############################
  # plot function to be estimated by sinc series
  ax[2].plot(sampZ, sampRes, '*', c="Maroon", label="samples", zorder=1)

  zL = Grid1(minZs, maxZs, nPlotPoint)

  resZ = lambda z: dist.Cdf(mapShift.Inv(z)) - molXF(mapShift.Inv(z))
  resStrip = [resZ(z) for z in zL]

  ax[2].plot(zL, resStrip, c="Blue", label="cdf", zorder=0)

  #############################
  # save figure
  plot.savefig('1d_dist_b.png')

  ##############################################################################
  fig,ax = plot.subplots(3, figsize=(6.5, 9))

  #############################
  # plot sinc fit to data
  ax[0].plot(sampZ, sampRes, '.', c="Maroon", label="samples", zorder=1)

  resSamp = tuple(zip(sampZ,sampRes))
  fit = SincFitNoMap(resSamp, (minZs,maxZs),nBase)

  ax[0].plot(fit.sincPoint, fit.weight, 'o', markersize=8, c="Blue")

  yL = fit.Interp(zL)
  ax[0].plot(zL, yL, c="Blue", label="cdf", zorder=0)

  #############################
  plot.savefig('1d_dist_c.png')