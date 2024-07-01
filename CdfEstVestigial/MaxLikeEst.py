#
# M a x L i k e E s t . p y
#

import numpy as np

from sympy import lambdify, log
from scipy.optimize import fsolve


def MleDistAEst(samp, dist):
  termSym = log(dist.pdfSym).diff(dist.aSym).simplify()

  fTemp = (
    'def f(a, x):\n'
    '  terms = {}\n'
    '  result = np.sum(terms)\n'
    '  return result'
  )
  fCode = fTemp.format(termSym)

  execScope = {}
  exec(fCode, globals(), execScope)
  f = execScope['f']

  ans = fsolve(f, 1, args=samp)

  return ans


def MleDistEst(samp, bases, nullifier, xSym):
  termSym = log(dist.pdfSym).diff(dist.aSym).simplify()

  fTemp = (
    'def f(a, x):\n'
    '  terms = {}\n'
    '  result = np.sum(terms)\n'
    '  return result'
  )
  fCode = fTemp.format(termSym)

  execScope = {}
  exec(fCode, globals(), execScope)
  f = execScope['f']

  ans = fsolve(f, 1, args=samp)

  return ans