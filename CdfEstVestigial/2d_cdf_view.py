#
# 2 d _ c d f _ v i e w . p y
#

import numpy as np
from matplotlib import pyplot as plot, cm

from LocUtil import Grid1, UnZip
from Dist import Hump, SkewHump
from DistEst import SampCdf2


###############################################################
def Sample():
  x = xDist.Sample()
  k = 20 ** (1/2 - x)
  y = yDist.Sample(k)

  return (x,y)


###############################
if __name__ == "__main__":
  # constants
  nSample = 2_000

  nPlotPoint = 101

  xDist = Hump()
  yDist = SkewHump()

  plot.subplots(figsize=(6.5, 6.5))

  # synthetic data
  samp = tuple(Sample() for _ in range(nSample))

  # plot the samples
  plot.plot(*UnZip(samp), '.', color='Maroon')
  plot.savefig('2d_samp.png')

  # plot the sample points as CDF
  fig,ax = plot.subplots(figsize=(6.5, 6.5), subplot_kw={"projection": "3d"})

  x,y = UnZip(samp)

  sampCdfF = lambda x,y: SampCdf2(samp, (x,y))
  sampCdfU = np.vectorize(sampCdfF)
  sampCdf = sampCdfU(x,y)

  ax.scatter(x,y, sampCdf, marker='.', c="maroon")

  plot.xlabel("x")
  plot.ylabel("y")
  ax.set_zlabel("CDF")

  ax.view_init(20, -75, 0)

  plot.savefig('2d_samp_cdf.png')

  # plot the sample CDF on grid
  fig,ax = plot.subplots(figsize=(6.5, 6.5), subplot_kw={"projection": "3d"})

  grid = Grid1(0,1, nPlotPoint)
  x,y = np.meshgrid(grid,grid)

  sampCdfF = lambda x,y: SampCdf2(samp, (x,y))
  sampCdfU = np.vectorize(sampCdfF)
  sampCdf = sampCdfU(x,y)

  ax.plot_surface(x,y, sampCdf, cmap=cm.jet)

  plot.xlabel("x")
  plot.ylabel("y")
  ax.set_zlabel("CDF")

  plot.savefig('2d_samp_cdf_grid.png')
