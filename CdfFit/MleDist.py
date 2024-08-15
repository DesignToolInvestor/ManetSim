#
# M l e D i s t . p y
#

# This file contains code to fine the MLE (Maximum Likelihood Estiment) of a distribution form the
# samples.

import sympy as sp
import cvxpy as cp
from matplotlib import pyplot as plot

from numpy import sinc

from LocUtil import Grid1, MinMax, UnZip
from Sinc import InterpZ


def DistZ(sampX, map_, nSinc):
  # process arguments
  sampSort = sorted(sampX)

  # Analize the map
  zSym = map_.zSym
  xSym = map_.xSym

  jacobSym = map_.invSym.diff(zSym).factor()
  jacob = sp.lambdify(zSym, jacobSym)

  # map samples to z
  sampZ = tuple(map_.Forward(x) for x in sampSort)

  # setup sinc point
  sincVal = cp.Variable(nSinc)
  zMin,zMax = MinMax(sampZ)

  h = (zMax - zMin) / (nSinc - 1)
  sincZ = Grid1(zMin,zMax, nSinc)

  # setup cost function
  logLike = lambda z: \
    cp.log(sum(sv * sinc((z - sz) / h) for (sz, sv) in zip(sincZ, sincVal)))

  objective = cp.Maximize(sum(logLike(z) * jacob(z) for z in sampZ))

  # setup constraints
  constEach = tuple(0 <= sv for sv in sincVal)
  constArea = h * sum(sv for (sz, sv) in zip(sincZ, sincVal)) == 1
  const = constEach + (constArea,)

  # solve the problem
  prob = cp.Problem(objective, const)
  print(f'Num. Constraints = {len(prob.constraints)}')
  print(prob.constraints)

  prob.solve(verbose=True)

  sincV = list(sincVal.value)
  sincPoint = tuple(zip(sincZ, sincV))

  # return result
  return sincPoint


def PlotEstZ(sincPointZ, tureDist, map_, zRange, sampX=None, nPlot=101):
  # compute (and plot) the PDF of Z
  zGrid = Grid1(*zRange, nPlot)
  xGrid = tuple(map_.Inverse(z) for z in zGrid)
  pdfX = tuple(tureDist.Pdf(x) for x in xGrid)
  pdfZ = tuple(v * map_.JacobZ(z) for (z, v) in zip(zGrid, pdfX))

  plot.plot(zGrid, pdfZ, c='blue', zorder=-2)

  # plot the sinc estiment of the PDF
  sincZ, sincV = UnZip(sincPointZ)
  plot.plot(sincZ, sincV, 'o', c='green', markersize=8, zorder=-1)

  estGrid = InterpZ(sincZ, sincV, zGrid)
  plot.plot(zGrid, estGrid, c='green', zorder=-1)

  # show the samples used to compute the estimation
  if sampX is not None:
    sampZ = tuple(map_.Forward(x) for x in sampX)
    sampEst = InterpZ(sincZ,sincV, sampZ)

    plot.plot(sampZ,sampEst, '+', color='red', zorder=0)

  # annotate the plot
  plot.xlabel('z')
  plot.ylabel('PDF (of Z)')
