#
# P l o t F i t . p y
#

from matplotlib import pyplot as plot
from math import log, exp
from scipy import stats

from LocUtil import LogGrid1, Grid1, MinMax
from LocMath import RobustLine


def PlotFitSemiY(
    xData,yData, axis=None,
    label='', xRange=None, varName='N',
    dotColor='maroon', lineColor='blue', dotSize=4):

  # plot dots
  # TODO: how do I look up the default axis
  if axis is None:
    plot.semilogy(xData, yData, 'o', color=dotColor, markersize=dotSize, zorder=0)
  else:
    axis.semilogy(xData, yData, 'o', color=dotColor, markersize=dotSize, zorder=0)

  # fit to data
  logY = [log(y) for y in yData]
  slope, intercept, _, _, _ = stats.linregress(xData, logY)

  text = f'{label} ({exp(intercept):.3} * {exp(slope):.3} ^ {varName})'

  # plot fit
  if xRange is None:
    xRange = MinMax(xData)

  xL = Grid1(*xRange, 30)
  yL = [exp(slope * x + intercept) for x in xL]

  if axis is None:
    plot.semilogy(xL, yL, label=text, linewidth=2, color=lineColor, zorder=1)
  else:
    axis.semilogy(xL, yL, label=text, linewidth=2, color=lineColor, zorder=1)

  return (slope, exp(intercept))

#######################################
def PlotFitLogLog(
    xData,yData, axis=None,
    method="l2", coef=None, label=None, xRange=None,
    varName='N', dotColor='maroon', lineColor='blue', dotSize=4):

  # plot dots
  if axis is None:
    plot.loglog(xData, yData, 'o', color=dotColor, markersize=dotSize, zorder=0)
  else:
    axis.loglog(xData, yData, 'o', color=dotColor, markersize=dotSize, zorder=0)

  # fit to data
  logX = tuple(log(x) for x in xData)
  logY = tuple(log(y) for y in yData)

  if method == 'l2':
    slope, inter, _, _, _ = stats.linregress(logX, logY)
  elif method == 'med':
    (slope, inter), (_,_) = RobustLine(logX, logY)
  elif method == 'given':
    slope, inter = coef
    inter = log(inter)
  else:
    raise ValueError("Method must be 'l2', 'med', or 'given'")

  if label is None:
    text = f'{exp(inter):.3} * {varName} ^ {slope:.3}'
  else:
    text = f'{label} ({exp(inter):.3} * N ^ {slope:.3})'

  # plot fit
  if xRange is None:
    xRange = MinMax(xData)

  xL = LogGrid1(*xRange, 30)
  yL = [exp(inter) * (x ** slope) for x in xL]

  if axis is None:
    plot.loglog(xL, yL, label=text, linewidth=2, color=lineColor, zorder=1)
  else:
    axis.loglog(xL, yL, label=text, linewidth=2, color=lineColor, zorder=1)

  return (slope, exp(inter))