#
# M o l l i f i e r . p y
#

from sympy import symbols, factor
from scipy.linalg import solve


# TODO:  Is it worth it to use sympy to get exact rational coefficients
def Hermite(lowVal, highVal, end):
  lowOrd = len(lowVal) - 1
  highOrd = len(highVal) - 1
  totOrd = lowOrd + highOrd + 1

  low,high = end

  # each row of the system is sum(m[i,j]*a[i], i) = r[j]
  m = []
  r = []

  # The polynomial is sum(c[i]*a[i] * x**p[i])
  p = [k for k in range(totOrd + 1)]
  c = [1 for _ in range(totOrd + 1)]

  for k in range(max(lowOrd,highOrd) + 1):
    if k <= lowOrd:
      temp = [c * low**p for (c,p) in zip(c,p)]
      m.append(temp)
      r.append(lowVal[k])

    if k <= highOrd:
      temp = [c * high**p for (c,p) in zip(c,p)]
      m.append(temp)
      r.append(highVal[k])

    # differentiate the polynomial
    c = [c*p for (c,p) in zip(c,p)]
    p = [p - 1 if 0 < p else 0 for p in p]

  a = solve(m,r)

  return tuple(a)


def MolSet(order, end):
  lowOrd,highOrd = order
  low,high = end
  result = []

  for k in range(0, lowOrd + 1):
    lowPoly = MolAtPoint(lowOrd,k, low)
    highPoly = NullAtPoint(highOrd, high)
    result.append(factor(lowPoly*highPoly))

  for k in range(0, highOrd + 1):
    lowPoly = NullAtPoint(lowOrd, low)
    highPoly = MolAtPoint(highOrd, k, high)
    result.append(factor(lowPoly * highPoly))

  return result


if __name__ == "__main__":
  molL = MolSet((1,1), (0,1))

  for mol in molL:
    print(mol)
