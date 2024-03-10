#
# N e t P a t h . p y
#

# This library contains a functions for generating and graphing network/path pairs.

from matplotlib import pyplot as plot
from random import sample

from BestPath import BestPath
from Component import Component
from LocMath import Interp1
from LocUtil import UnZip
from MakeNet import RandNetCirc
from Visual import GraphBiNet


########################################################
def MakeNetPath(nNode, netR, costF):
  # make path net
  net = RandNetCirc(nNode, netR)
  nodeLoc,link = net

  # seperate into components
  compL = Component(net)
  domComp = max(compL, key=len)

  # pick flow
  flow = sample(domComp, 2)
  linkCost = [costF(nodeLoc[n0], nodeLoc[n1]) for (n0, n1) in link]
  path = BestPath(net, *flow, linkCost)

  return (net,path)


def PlotNetPath(ax, net, path, title=None, annotate=None):
  # parse args
  nodeLoc,_ = net
  nHop = len(path) - 1

  GraphBiNet(ax, net)

  # highlight path
  for hopNum in range(nHop):
    n0 = path[hopNum]
    n1 = path[hopNum + 1]
    line = (nodeLoc[n0], nodeLoc[n1])
    plot.plot(*UnZip(line), color="yellow", linewidth=3, zorder=-1)

  # mark start and end of path
  x, y = nodeLoc[path[0]]
  plot.plot(x, y, 's', color="limegreen", markersize=10, zorder=-2)

  x, y = nodeLoc[path[nHop]]
  plot.plot(x, y, 'o', color="limegreen", markersize=10, zorder=-2)

  # add annotation
  if title is not None:
    plot.title(title)

  if annotate is not None:
    nNode, rho, seed, nHop = annotate

    x = Interp1(*plot.xlim(), 0.1)
    y = Interp1(*plot.ylim(), 0.9)
    plot.text(
      x, y, f'N = {nNode}\nRho = {rho}\nSeed = {seed}\nnHop = {nHop}\n',
      fontsize=8, va="top", ha="left", multialignment="left")

  # remove axis
  ax.set_axis_off()