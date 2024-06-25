#
# M a x L i k e E s t . p y
#

import numpy as np

from sympy import lambdify, log
from scipy.optimize import fsolve

from DistA import aSym, xSym, pdfSym


# This is a throw away function that will need to be replaced by a general function
# TODO: Why is this slow ???
def MaxLikeDistA_lambdify(samp):
  termSym = log(pdfSym).diff(aSym).simplify()
  termF = lambdify((xSym,aSym), termSym)

  f = lambda a,samp: sum(termF(x,a) for x in samp)[0]

  result = fsolve(f,1, args=list(samp))

  return result[0]

# TODO: This is even slower ???
def MaxLikeDistA_loop(samp):
  def f(a, samp):
    sum_ = 0
    for x in samp:
      sum_ += (1 - 2*x) / (a[0] + 2*(1-a[0])*x)
    return sum_

  result = fsolve(f,1, args=list(samp))

  return result[0]

# Try this
def MaxLikeDistA_numPyLoop(samp):
  def f(aL, samp):
    a = np.float64(aL[0])
    sum_ = 0
    for x in samp:
      sum_ += (1 - 2*x) / (a + 2*(1-a)*x)
    return sum_

  result = fsolve(f,1, args=samp)

  return result[0]

# Try this
def MaxLikeDistA_vect(samp):
  def f(a, samp):
    assert(type(samp) == np.ndarray)
    terms = (1 - 2*samp) / (a + 2*(1-a)*samp)
    return np.sum(terms)

  result = fsolve(f,1, args=samp)
  return result[0]