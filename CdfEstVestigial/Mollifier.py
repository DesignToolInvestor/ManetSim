#
# M o l l i f i e r . p y
#

# This file contains functions that compute the set of mollifyers that represent the bases of the
# of the space of end conditions for a specified order of derivatives. 

from sympy import Symbol, exp, solve


def Hermite(lowVal, highVal, xRange, ySym):
  leftOrd = len(lowVal) - 1
  rightOrd = len(highVal) - 1
  totOrd = leftOrd + rightOrd + 1

  xMin,xMax = xRange

  # set up
  coef = [Symbol(f'a{i}') for i in range(totOrd + 1)]
  form = sum(coef[i] * ySym ** i for i in range(totOrd + 1))
  constraint = []

  # Do left side
  poly = form
  for dOrd in range(leftOrd + 1):
    constraint.append(poly.subs(ySym, xMin) - lowVal[dOrd])
    poly = poly.diff(ySym).simplify()

  # Do right side
  poly = form
  for dOrd in range(rightOrd + 1):
    constraint.append(poly.subs(ySym, xMax) - highVal[dOrd])
    poly = poly.diff(ySym).simplify()

  # solve the system
  coefVal = solve(constraint, coef)
  result = form.subs(coefVal).factor()

  return result


# Returns a flat list of the basis mollifiers with derivative values equal to one from the zeroth
# derivative upto the specified derivative order.
def MolSetZ(zSym, derivOrd):
  # parse arg
  leftOrd, rightOrd = derivOrd

  # set up
  ySym = Symbol('y')
  xRange = (0,1)
  invMap = exp(zSym) / (1 + exp(zSym))

  result = []

  # do left hand molifyers
  highVal = [0 for _ in range(rightOrd + 1)]
  for derivDeg in range(0, leftOrd + 1):
    lowVal = [0 for _ in range(derivDeg)] + [1] + [0 for _ in range(derivDeg + 1, leftOrd + 1)]
    polyY = Hermite(lowVal, highVal, (0,1), ySym)
    polyZ = polyY.subs(ySym, invMap).factor()
    result.append(polyZ)

  lowVal = [0 for _ in range(leftOrd + 1)]
  for derivDeg in range(0, rightOrd + 1):
    highVal = [0 for _ in range(derivDeg)] + [1] + [0 for _ in range(derivDeg + 1, rightOrd + 1)]
    polyY = Hermite(lowVal, highVal, xRange, ySym)
    polyZ = polyY.subs(ySym, invMap).factor()
    result.append(polyZ)

  return result
