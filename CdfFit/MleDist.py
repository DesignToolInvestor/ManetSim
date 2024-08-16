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
from Sinc import InterpZ


#########################################################################
# This function finds the MLE distribution for a sinc approximation
def Sinc(sampX, map_, nSinc):
  # process arguments
  nSamp = len(sampX)
  sampSort = sorted(sampX)

  # Analize the map
  zSym = map_.zSym
  xSym = map_.xSym

  # map samples to z
  zMin,zMax = map_.Forward(sampX[0]), map_.Forward(sampX[nSamp - 1])

  # setup sinc point
  h = (zMax - zMin) / (nSinc - 1)
  sincZ = Grid1(zMin,zMax, nSinc)
  sincX = tuple(map_.Inverse(z) for z in sincZ)

  # setup cost function
  sincVar = cp.Variable(nSinc)

  phiX = lambdify(xSym, map_.forSym)   # for code clarity
  logLike = lambda x: \
    cp.log(sum(sv * sinc((phiX(x) - sx) / h) for (sx, sv) in zip(sincX, sincVar)))
  objective = cp.Maximize(sum(logLike(z) for z in sampZ))

  # setup the constraints
  # TODO: strange that the positive constraint is necessary
  constEach = tuple(0 <= sv for sv in sincVar)

  phiPrime = map_.DzDx    # for code clarity
  constArea = h * sum(sv * phiPrime(sx) for (sx, sv) in zip(sincX, sincVar)) == 1

  const = constEach + (constArea,)

  # solve the problem
  prob = cp.Problem(objective, const)
  prob.solve()

  sincV = tuple(sincVar.value)
  sincPoint = tuple(zip(sincX, sincV))

  # return result
  return sincPoint


#########################################################################
def RmsDiff(sincApprox, func, eps=1e-6):
  sincPoint,map_ = sincApprox
  nSinc = len(sincPoint)

  # TODO:  Make this a seperate module called QuadSikorski
  # set up
  zMin,zMax = map_.Forward(sincPoint[0][0]), map_.Forward(sincPoint[nSinc - 1][0])
  zMid = (zMax - zMin) / 2
  h = (zMax - zMin) / (nSinc - 1)

  diffZ = lambda z: sincApprox.InterpZ(z) - func(z)

  # Initial samples ... need to at least meet the Nyquest critera
  sampL = []

  z = zMid
  leftCount = 0

  while True:
    samp = diffZ(z) * phiPrimeZ(z)
    if (z <= zMin) and (abs(samp) < eps/3):
      break

    sampL.append(samp)
    z = z - h
    leftCount += 1

  z = zMid + h
  rightCount = 1

  while True:
    samp = diffZ(z) * phiPrimeZ(z)
    if (z <= zMin) and (abs(samp) < eps/3):
      break

    sampL.append(samp)
    z = z + h
    rightCount += 1

  prevVal = LowRoundSum(sampL)

  # iterate on h
  h = h /2


#########################################################################
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
