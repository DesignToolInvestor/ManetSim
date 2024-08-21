#
# S i n c . p y
#

# This file defines functions for fitting to sinc approximations to noise data.

from math import ceil, isfinite, pi
from numpy import sinc
from scipy.optimize import fsolve

from LocUtil import Grid1, MinMax, UnZip


###############################################################
class SincApprox(object):
  def __init__(self, zMin,zMax,nSinc, sincV, map_):
    self.nSinc = nSinc

    self.sincZ = Grid1(zMin,zMax, nSinc)
    self.h = (zMax - zMin) / (nSinc - 1)

    self.sincX = tuple(map_.Inverse(z) for z in self.sincZ)
    self.sincV = sincV

    self.map = map_

  def InterpX1(self, gridX):
    gridZ = tuple(self.map.Forward(x) for x in gridX)
    result = self.InterpZ1(gridZ)

    return result

  def InterpZ1(self, gridZ):
    result = tuple(self.InterpZ0(z) for z in gridZ)
    return result

  def InterpX0(self, x):
    z = self.map.Forward(x)
    result = self.InterpZ0(z)

    return result

  def InterpZ0(self, z):
    result = sum(sv * sinc((z - sz) / self.h) for (sz, sv) in zip(self.sincZ, self.sincV))
    return result

  def EnvZ(self, z):
    nSinc = self.nSinc
    h = self.h

    if (self.sincZ[0] <= z) and (z <= self.sincZ[self.nSinc - 1]):
      result = self.InterpZ0(z)
    else:
      def TailEnv(z, zk, h):
        if abs((z - zk) / h) < 0.5:
          result = sinc((z - zk) / h)
        else:
          result = h / (pi * abs(z - zk))
        return result

      terms = tuple((-1) ** k * self.sincV[k] * TailEnv(z, self.sincZ[k], h) for k in range(nSinc))
      result = abs(sum(terms))

    return result


###############################################################
# TODO:  Do fsolve in x domain to avoid the need for approxZLim (at least for finite domain)
# TODO:  Add heuristic for starting that we are far enough out to have the right asymptotics.
# TODO:  Think about what to do when the function has zeros that may confuse the limits
# TODO:  Factor out starting criteria to avoid overhead in repeated applications.
# TODO:  Factor out starting criteria to allow escalation
# TODO:  Add check for non-exponential convergence caused by discontinuities at end in zRange
def QuadSikorskiWrap(Func, map_, approxZLim, eps=1e-6, maxH=None):
  Z2X = map_.Inverse
  InvWeight = map_.DzDx
  SummandX = lambda x: Func(x) / InvWeight(x)
  SummandZ = lambda z: SummandX(Z2X(z))

  zLowLim,zHighLim = approxZLim
  zMin = fsolve(lambda z: abs(SummandZ(z[0])) - 0.4*eps, zLowLim)[0]
  assert(isfinite(zMin))

  zMax = fsolve(lambda z: abs(SummandZ(z[0])) - 0.4*eps, zHighLim)[0]
  assert(isfinite(zMin))

  if maxH is None:
    n = 10
  else:
    n = ceil((zMax - zMin) / maxH)

  h = (zMax - zMin) / (n - 1)

  samp = tuple(SummandZ(zMin + k*h) for k in range(n + 1))
  result = h * sum(samp)

  for itNum in range(10):
    prevResult = result

    n *= 2
    h /= 2

    newSamp = tuple(SummandZ(zMin + k*h) for k in range(1,n + 1, 2))
    samp += newSamp

    result = h * sum(samp)
    if abs(result - prevResult) < 0.2*eps:
      break

  return (result, (zMin,zMax,n))

#######################################
def QuadSikorski(Func, map_, zRange, nStart):
  Z2X = map_.Inverse
  InvWeight = map_.DzDx
  SummandX = lambda x: Func(x) / InvWeight(x)
  SummandZ = lambda z: SummandX(Z2X(z))

  zMin, zMax = zRange
  n = nStart
  h = (zMax - zMin) / (n - 1)

  eps = abs(Func(Z2X(zMin))) + abs(Func(Z2X(zMax)))

  samp = tuple(SummandZ(zMin + k*h) for k in range(n))
  result = h * sum(samp)

  for itNum in range(10):
    prevResult = result

    n *= 2
    h /= 2

    newSamp = tuple(SummandZ(zMin + k*h) for k in range(1,n + 1, 2))
    samp += newSamp

    result = h * sum(samp)
    if abs(result - prevResult) < eps:
      break

  return (result, n)
