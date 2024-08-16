#
# M a p . p y
#

# This file creates the most common maps

from sympy import exp, lambdify, log, sqrt


###############################################################
class LogRatio(object):
  def __init__(self, xSym, zSym, xRange=(0,1), z0=0, zScale=1):
    # TODO:  Think about negative zScale
    # check arguments
    xMin,xMax = xRange
    if xMax <= xMin:
      raise ValueError(f'xMin should be less than xMax (received {xRange})')

    # make map and inverse
    self.forSym = zScale * (log((xSym - xMin) / (xMax - xSym)) + z0)
    self.Forward = lambdify(xSym, self.forSym)

    zss = zSym/zScale - z0
    self.invSym = (xMax * exp(zss) + xMin) / (1 + exp(zss))
    self.Inverse = lambdify(zSym, self.invSym)

    # Compute the Jacobian.  This is phi-inverse-prime.
    self.dxDz = self.invSym.diff(zSym).factor()
    self.DxDz = lambdify(zSym, self.dxDz)

    # Compute the inverse Jacobian.  This is phi-prime.
    self.dzDx = self.forSym.diff(xSym).factor()
    self.DzDx = lambdify(xSym, self.dzDx)

    # save stuff needed by other methods
    self.xRange = xRange
    self.z0 = z0
    self.zScale = zScale
    self.xSym = xSym
    self.zSym = zSym

  # TODO:  given duck typing and a lack of protection what it the point accessors methods
  def XSym(self):
    return self.xSym

  def ZSym(self):
    return self.zSym

  def DerivSym(self, ord):
    result = self.forSym.diff(self.xSym, ord).simplify()
    return result

  # TODO: revisit these
  def NullLeftX(self):
    xMin, xMax = self.xRange
    return (self.xSym - xMin) / sqrt(self.zScale * (xMax - xMin))

  def NullRightX(self):
    xMin, xMax = self.xRange
    return (xMax - self.xSym) / sqrt(self.zScale * (xMax - xMin))

  def NullLeftZ(self):
    xMin, xMax = self.xRange
    scale = self.zScale
    zSym = self.zSym
    z0 = self.z0

    zss = zSym/scale - z0
    result = ((xMax - xMin) * exp(zss) + 2*xMin) / sqrt(scale * (xMax - xMin)) / (1 + exp(zss))
    return result

  def NullRightZ(self):
    xMin, xMax = self.xRange
    scale = self.zScale
    zSym = self.zSym
    z0 = self.z0

    zss = zSym/scale - z0
    result = (xMax - xMin) / sqrt(scale * (xMax - xMin)) / (1 + exp(zss))
    return result

  def ShiftScale(self, z0, zScale):
    newZ0 = self.z0 + z0
    newScale = self.zScale * zScale

    return LogRatio(self.xSym, self.zSym, self.xRange, newZ0, newScale)

# TODO:  Add LogSinch, LogTan
# TODO:  Lookup maps from the Integral equations paper
