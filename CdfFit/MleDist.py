#
# M l e D i s t . p y
#

# This file contains code to fine the MLE (Maximum Likelihood Estiment) of a distribution form the
# samples.

# import sympy as sp
import cvxpy as cp

from matplotlib import pyplot as plot
from numpy import sinc
from sympy import lambdify

from LocUtil import Grid1, MinMax, UnZip
from LocMath import Interp1
from Sinc import QuadSikorski, SincApprox


#########################################################################
# This function finds the MLE distribution for a sinc approximation
def Sinc(sampX, map_, nSinc):
  xSym = map_.xSym
  zSym = map_.zSym

  phiPrimeSym = (1 / map_.forSym.diff(xSym)).factor()
  phiPrimeX = lambdify(xSym, phiPrimeSym)

  # process arguments
  sampZ = tuple(map_.Forward(x) for x in sampX)

  # map samples to z
  xRange = MinMax(sampX)
  zMin,zMax = map(map_.Forward, xRange)

  # setup sinc point
  h = (zMax - zMin) / (nSinc - 1)
  sincZ = Grid1(zMin,zMax, nSinc)
  sincX = tuple(map_.Inverse(z) for z in sincZ)

  # setup cost function
  sincVar = cp.Variable(nSinc)

  phiX = lambdify(xSym, map_.forSym)
  logLikeP = lambda x: (
    cp.log(sum(sv * sinc((phiX(x) - sz) / h) for (sz, sv) in zip(sincZ, sincVar))))
  obj = cp.Maximize(sum(logLikeP(x) for x in sampX))

  # setup the constraints
  # TODO: strange that the positive constraint is necessary
  constEach = list(0 <= v for v in sincVar)
  constArea = h * sum(v * phiPrimeX(x) for (x, v) in zip(sincX, sincVar)) == 1

  const = constEach + [constArea]

  # solve the problem
  prob = cp.Problem(obj, const)
  solveResult = prob.solve()

  # return result
  sincV = tuple(sincVar.value)
  return SincApprox(zMin,zMax,nSinc, sincV, map_)


#########################################################################
def RmsDiff(sincApprox, Func, epsMin=1e-6):
  diff = lambda x: sincApprox.InterpX0(x) - Func(x)
  approxZLim = (sincApprox.sincZ[0], sincApprox.sincZ[sincApprox.nSinc - 1])

  nSinc = sincApprox.nSinc
  eps = abs(sincApprox.sincV[0]) + abs(sincApprox.sincV[nSinc - 1])
  if eps < epsMin:
    eps = epsMin

  result = QuadSikorski(diff, sincApprox.map, approxZLim, eps=eps, maxH=sincApprox.h)
  return result


#########################################################################
def PlotPdfEstZ(pdfApprox, pdfF, sampX, annotation=None):
  # parse the arguments
  nSinc = pdfApprox.nSinc
  h = pdfApprox.h

  X2Z = pdfApprox.map.Forward
  Z2X = pdfApprox.map.Inverse

  sampZ = tuple(X2Z(x) for x in sampX)

  # compute the plotting range
  zMin, zMax = MinMax(sampZ)
  plotRange = (zMin - 2 * h, zMax + 2 * h)

  # plot true distribution
  nPlot = 4 * (nSinc + 4) + 1 if 8 < nSinc else 101
  zGrid = Grid1(*plotRange, nPlot)

  xGrid = tuple(Z2X(z) for z in zGrid)
  pdfTrue = tuple(pdfF(x) for x in xGrid)

  plot.plot(zGrid,pdfTrue, c='blue', zorder=-3)

  # plot the sinc points
  plot.plot(pdfApprox.sincZ, pdfApprox.sincV, 'o', c="green", markersize=4, zorder=-1)

  pdfEst = pdfApprox.InterpZ1(zGrid)
  plot.plot(zGrid,pdfEst, c='green', zorder=-2)

  # plot the samples
  sampTrue = tuple(pdfF(x) for x in sampX)
  sampEst = pdfApprox.InterpX1(sampX)

  linesX = (sampZ, sampZ)    # this is x-start-list and x-end list
  linesY = (sampTrue, sampEst)

  plot.plot(linesX, linesY,  c='red', zorder=0)

  # add annotation
  if annotation is not None:
    xMin, xMax, yMin, yMax = plot.axis()
    xPos = Interp1(xMin, xMax, 0.95)
    yPos = Interp1(yMin, yMax, 0.95)
    plot.text(xPos, yPos, annotation, ha='right', va='top')

  plot.xlabel('z')
  plot.ylabel('Pdf (without Jacobian)')
