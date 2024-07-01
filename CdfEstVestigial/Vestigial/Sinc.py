#
# S i n c . p y
#

# system packages
from numpy import sinc

from matplotlib import pyplot as plot
from scipy.linalg import lstsq

# local files
from LocUtil import Grid1
from Mollifier import MolSet
from Map import LogRatio


#######################################################
class SincApprox(object):
  def __init__(self, map_, zRange, nSinc, sincWeight, nullZ, molZ, molWeight, maxDeriv=0):
    self.map_ = map_

    self.nSinc = nSinc
    minZ,maxZ = zRange
    self.h = (maxZ - minZ) / (nSinc - 1)

    self.sincPointZ = [k * self.h + minZ for k in range(nSinc)]

    self.sincWeight = sincWeight

    self.nullZ = nullZ

    self.molZ = molZ
    self.molWeight = molWeight

    self.maxDeriv = maxDeriv


  def Interp(self, xPoint):
    result = []
    for z in xPoint:
      z = self.map_.forward(x)

      val = 0
      for k in range(self.nSinc):
        val += self.sincWeight[k] * sinc((z - self.sincPointZ[k]) / self.h) * self.nullZ(z)

      for k in range(len(self.molZ)):
        val += self.molWeight[k] * self.molZ[k](z)

      result.append(val)

    return result


  def Deriv(self, ord, xPoint):
    if ord > self.maxDeriv:
      raise Exception(f'approximation not computed for derivatives of order {ord}')

    nulDeriv = null

    result = []
    for z in xPoint:
      z = self.map_.forward(x)

      val = 0
      for k in range(self.nSinc):
        val += self.sincWeight[k] * sinc((z - self.sincPointZ[k]) / self.h) * self.nullZ(z)

      for k in range(len(self.molZ)):
        val += self.molWeight[k] * self.molZ[k](z)

      result.append(val)

    return result


  def SincPoint(self):
    zUnShift = [z + self.z0 for z in self.sincPoint]
    xL = [self.map_.inverse(z) for z in zUnShift]

    molVal = self.MolInterpZ(self.sincPoint)
    val = [mv + sv for (mv,sv) in zip(molVal, self.sincWeight)]

    return tuple(zip(xL, val))


#######################################################
# TODO:  Do SVD, soft threshold singular values to noise floor of samples
# TODO:  Is this known to be well conditioned ???
def SincFitNoMap(sampZV, zRange, nSinc):
  # unpack arguments
  zMin,zMax = zRange
  h = (zMax - zMin) / (nSinc - 1)
  sincPoint = Grid1(*zRange, nSinc)

  # setup matrices
  # TODO: should  create a hardware floating point version of this (and lots of other stuff)
  a = []
  b = []
  for (sampZ,sampVal) in sampZV:
    interpVal = [sinc((sampZ - sp) / h) for sp in sincPoint]
    a.append(interpVal)
    b.append(sampVal)

  # solve for weights
  # TODO: Add error checking
  temp,_,_,_ = lstsq(a, b)
  weight = tuple(temp)

  result = SincApprox(zRange,nSinc,weight)

  return result


#######################################################
def SincFit(sampX, mapProb, nSinc):
  # unpack arguments
  nSamp = len(sampX)

  # construct sampled CDF
  sampSort = sorted(sampX)
  quant = [(k + 0.5) / nSamp for k in range(nSamp)]

  # map to z
  sampZ = [mapProb.forward(x) for x in sampSort]

  # ########    debugging code    #######
  # plot.plot(sampZ, quant, '*', c="Maroon")
  # plot.xlabel('Z')
  # plot.show()
  # ########    debugging code    #######

  # shift z
  (zMin,zMax) = (sampZ[0], sampZ[nSamp - 1])
  z0 = (zMax + zMin) / 2

  h = (zMax - zMin) / (nSinc - 1)

  sampZShift = [z - z0 for z in sampZ]

  # do mollifiers
  molSet = MolSet((1,1))

  # TODO:  This is problem specific
  molX = lambda x: x*x*(3 - 2*x)
  mapMol = LogRatio()
  molZ = lambda z: molX(mapMol.inverse(z))

  resZ = [q - molZ(z) for (z,q) in zip(sampZShift, quant)]

  # fit sinc expansion to residual
  zShiftRange = (sampZShift[0], sampZShift[nSamp - 1])
  sincFit = SincFitNoMap(zip(sampZShift,resZ), zShiftRange, nSinc)

  # ########    debugging code    #######
  # plot.plot(sampZShift, resZ, '*', c="Maroon")
  # plot.xlabel('Shifted Z')
  # plot.ylabel('Residual')
  #
  # plot.plot(sincFit.sincPoint, sincFit.sincWeight, 'o', c="Blue", markersize=10, zorder=-1)
  #
  # zL = Grid1(*zShiftRange, 20)
  # interp = sincFit.Interp(zL)
  # plot.plot(zL, interp, c="blue")
  #
  # plot.show()
  # ########    debugging code    #######

  # construct estimation of CDF
  result = SincSysApprox(mapProb, zShiftRange, nSinc, z0, sincFit.sincWeight, [molZ], [1])

  return result


#######################################################
def SincFitDeriv(sampX, mapProb, derivOrd, molOrd, nSinc):
  # unpack arguments
  nSamp = len(sampX)

  # construct sampled CDF
  sampSort = sorted(sampX)
  quant = [(k + 0.5) / nSamp for k in range(nSamp)]

  # map to z
  sampZ = [mapProb.forward(x) for x in sampSort]

  # ########    debugging code    #######
  # plot.plot(sampZ, quant, '*', c="Maroon")
  # plot.xlabel('Z')
  # plot.show()
  # ########    debugging code    #######

  # shift z
  (zMin,zMax) = (sampZ[0], sampZ[nSamp - 1])
  z0 = (zMax + zMin) / 2

  h = (zMax - zMin) / (nSinc - 1)

  sampZShift = [z - z0 for z in sampZ]

  # mollifiers
  # TODO:  This is problem specific
  molX = lambda x: x*x*(3 - 2*x)
  mapMol = LogRatio()
  molZ = lambda z: molX(mapMol.inverse(z))

  resZ = [q - molZ(z) for (z,q) in zip(sampZShift, quant)]

  # fit sinc expansion to residual
  zShiftRange = (sampZShift[0], sampZShift[nSamp - 1])
  sincFit = SincFitNoMap(zip(sampZShift,resZ), zShiftRange, nSinc)

  # ########    debugging code    #######
  # plot.plot(sampZShift, resZ, '*', c="Maroon")
  # plot.xlabel('Shifted Z')
  # plot.ylabel('Residual')
  #
  # plot.plot(sincFit.sincPoint, sincFit.sincWeight, 'o', c="Blue", markersize=10, zorder=-1)
  #
  # zL = Grid1(*zShiftRange, 20)
  # interp = sincFit.Interp(zL)
  # plot.plot(zL, interp, c="blue")
  #
  # plot.show()
  # ########    debugging code    #######

  # construct estimation of CDF
  result = SincSysApprox(mapProb, zShiftRange, nSinc, z0, sincFit.sincWeight, [molZ], [1])

  return result