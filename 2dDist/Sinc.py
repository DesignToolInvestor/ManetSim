#
# S i n c . p y
#

# system packages
from numpy import sinc
from collections import namedtuple
from matplotlib import pyplot as plot
from scipy.linalg import lstsq

# local files
from LocUtil import Grid1


#######################################################
Map = namedtuple('Map', ['For', 'Inv'])

class SincApprox:
  def __init__(self, zRange, nBase, weigth):
    self.map = map

    self.zRange = zRange
    self.nBase = nBase

    self.zLow,self.zHigh = zRange
    self.h = (self.zHigh - self.zLow) / (nBase - 1)
    self.sincPoint = Grid1(*zRange, nBase)
    
    self.weight = weigth

  # TODO:  Make a one liner or at least a two liner (after creating tests)
  def Interp(self, zL):
    result = []
    
    for z in zL:
      val = 0
      for k in range(self.nBase):
        val += self.weight[k] * sinc((z - self.sincPoint[k]) / self.h)
      result.append(val)

    return(result)
    

#######################################################
# TODO:  Do SVD, soft threshold singular values to noise floor of samples
# TODO:  Is this known to be well conditioned ???
def SincFit(samp, xRange, nBase):
  # unpack arguments
  xLow,xHigh = xRange
  h = (xHigh - xLow) / (nBase - 1)
  sincPoint = Grid1(*xRange, nBase)

  # setup matrices
  # TODO: should  create a hardware floating point version of this (and lots of other stuff)
  a = []
  b = []
  for (sampZ,sampVal) in samp:
    interpVal = [sinc((sampZ - sp) / h) for sp in sincPoint]
    a.append(interpVal)
    b.append(sampVal)

  # for i in range(nBase):
  #   xL = [sz for (sz,_) in samp]
  #   val = [a[j][i] for j in range(len(samp))]
  #   plot.plot(xL, val, '*', c="blue")

  plot.show()

  # solve for weights
  temp,_,_,_ = lstsq(a, b)
  weight = tuple(temp)

  result = SincApprox(xRange,nBase,weight)

  return result


def FindShift(lowX,highX, mapFor):
  shift = 0

  for i in range(5):
    lowZ = mapFor(lowX)
    highZ = mapFor(highX)

    mid = (lowZ + highZ) / 2
