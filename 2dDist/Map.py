#
# M a p . p y
#

# This file creates the most common maps

from sympy import diff, exp, log



###############################################################
class LogRatio(object):
  def __init__(self, xSym, zSym, xRange=(0,1), z0=0, zScale=1):
    xMin,xMax = xRange
    if xMax <= xMin:
      raise ValueError(f'xMin should be less than xMax (received {xRange})')

    self.xSym = xSym
    self.zSym = zSym
    
    self.map = zScale * (log((xSym - xMin) / (xMax - xSym)) + z0)

    zss = zSym/zScale - z0
    self.inv = (xMax * exp(zss) + xMin) / (1 + exp(zss))

  def MapExp(self):
    return self.map

  def InvExp(self):
    return self.inv
  
  def Deriv(self, ord):
    result = self.map.diff(self.xSym, ord).simplify()
    return result


###############################################################
