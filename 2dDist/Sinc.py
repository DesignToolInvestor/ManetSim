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
class SincApprox:
  def __init__(self, zRange, nSinc, sincWeight):
    self.nSinc = nSinc

    zMin,zMax = zRange
    self.h = (zMax - zMin) / (nSinc - 1)

    self.sincPoint = Grid1(zMin,zMax, nSinc)

    self.sincWeight = sincWeight

  def Interp(self, zL):
    result = []

    for z in zL:
      val = sum(w * sinc((z - sp) / self.h) for (w, sp) in zip(self.sincWeight, self.sincPoint))
      result.append(val)
    
    return result


#######################################################
class SincSysApprox(SincApprox):
  def __init__(self, map_, zRange, nSinc, z0, sincWeight, molZ, molWeight):
    super().__init__(zRange, nSinc,sincWeight)

    self.map_ = map_
    self.z0 = z0
    self.molZ = molZ
    self.molWeight = molWeight


  def MolInterpZ(self, zL):
    molVal = [sum(mw * mb(z) for (mb,mw) in zip(self.molZ, self.molWeight)) for z in zL]

    return molVal


  def Interp(self, xL):
    zL = [self.map_.forward(x) - self.z0 for x in xL]

    sincVal = super().Interp(zL)
    molVal = self.MolInterpZ(zL)

    result = [sv + mv for (sv,mv) in zip(sincVal, molVal)]

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

def SincFit(sampX, mapProb, derivOrd, molOrd, nSinc):
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