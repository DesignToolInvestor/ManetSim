#
# n h o p _ p l o t . p y
#

import numpy as np
from matplotlib import pyplot as plot, cm
from itertools import repeat

from LocUtil import Grid1, UnZip
from Dist import Hump, SkewHump
from DistEst import SampCdf2


if __name__ == "__main__":
  # constants
  fileName = "nhop.log"

  nPlotPoint = 101

  # read data
  with open(fileName, 'r') as file:
    lineL = file.readlines()

  info = [eval(l) for l in lineL]
  _,_,samp = UnZip(info)

  nHop,dist = UnZip(samp)
  maxHop = max(nHop)
  maxDist = max(dist)

  # plot smooth curve
  fig,ax = plot.subplots(figsize=(6.5, 6.5), subplot_kw={"projection": "3d"})

  distGrid = Grid1(0,maxDist, nPlotPoint)
  for nHop in range(maxHop):
    z = [SampCdf2(samp, (nHop,dg)) for dg in distGrid]
    plot.plot(distGrid, tuple(repeat(nHop,nPlotPoint)), z)

  ax.view_init(30, -135, 0)

  plot.xlabel("Dist.")
  plot.ylabel("Num. Hop")
  ax.set_zlabel("CDF")

  plot.savefig('nhop_500_2_smooth.png')

  # plot CDF of samples
  fig,ax = plot.subplots(figsize=(6.5, 6.5))

  for nHop in range(1,maxHop):
    sampSub = tuple(filter(lambda s: s[0] == nHop, samp))
    if sampSub != ():
      nSampRow = len(sampSub)
      _,distSub = UnZip(sampSub)

      z = [SampCdf2(samp, (nHop,dg)) for dg in distSub]
      plot.plot(distSub, z, '.')


  plot.xlabel("Dist")
  plot.ylabel("CDF")

  plot.savefig('nhop_500_2_samp.png')