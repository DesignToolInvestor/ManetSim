#
# D i s t A . p y
#

# This header may be edited manually, but the operational core of this file (everything below the
# "magic line") will be replaced by the results of a symbolic computation performed in the
# Jupyter notebook *dist_a.ipynb*.

# This file defines a distribution in the namespace DistA.  The PDF of the distribution is
# defined for x over [0,1] by:
#   a + 2*(1 - a) * x

####################### generated code beyond this point ######################
import math
from sympy import Symbol, sqrt
from random import uniform

xSym = Symbol('x')
qSym = Symbol('q')
aSym = Symbol('a')

pdfSym = aSym + xSym*(2 - 2*aSym)
cdfSym = aSym*xSym + xSym**2*(1 - aSym)
invCdfSym = (aSym - sqrt(aSym**2 - 4*aSym*qSym + 4*qSym))/(2*(aSym - 1))


def PdfNum(x,a):
  return a + x*(2 - 2*a)

def CdfNum(x,a):
  return a*x + x**2*(1 - a)

def InvCdfNum(q,a):
  if abs(a - 1) < 0.01:
    result = q + (a - 1)**5*(21*(2*q - 1)**6 - 35*(2*q - 1)**4 + 15*(2*q - 1)**2 - 1)/32 + (a - 1)**4*(6*q + 7*(2*q - 1)**5 - 10*(2*q - 1)**3 - 3)/16 + (a - 1)**3*(5*(2*q - 1)**4 - 6*(2*q - 1)**2 + 1)/16 + (a - 1)**2*(-2*q + (2*q - 1)**3 + 1)/4 + (a - 1)*((2*q - 1)**2 - 1)/4
  else:
    result = (a - math.sqrt(a**2 - 4*a*q + 4*q))/(2*(a - 1))

  return result


def GenSamp(a):
  q = uniform(0,1)
  result = InvCdfNum(q,a)
  return result
