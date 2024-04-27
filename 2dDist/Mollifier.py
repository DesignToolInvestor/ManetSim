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
  p = [derivDeg for derivDeg in range(totOrd + 1)]
  c = [1 for _ in range(totOrd + 1)]

  for derivDeg in range(max(lowOrd,highOrd) + 1):
    if derivDeg <= lowOrd:
      temp = [c * low**p for (c,p) in zip(c,p)]
      m.append(temp)
      r.append(lowVal[derivDeg])

    if derivDeg <= highOrd:
      temp = [c * high**p for (c,p) in zip(c,p)]
      m.append(temp)
      r.append(highVal[derivDeg])

    # differentiate the polynomial
    c = [c*p for (c,p) in zip(c,p)]
    p = [p - 1 if 0 < p else 0 for p in p]

  a = solve(m,r)

  return tuple(a)


def MolSet(order, end):
  lowOrd,highOrd = order
  totOrd = lowOrd + highOrd + 1

  low,high = end
  result = []

  highVal = [0 for _ in range(highOrd + 1)]
  for derivDeg in range(0, lowOrd + 1):
    lowVal = [0 for _ in range(derivDeg)] + [1] + [0 for _ in range(derivDeg + 1, lowOrd + 1)]
    poly = Hermite(lowVal, highVal, end)
    result.append(poly)

  lowVal = [0 for _ in range(lowOrd + 1)]
  for derivDeg in range(0, highOrd + 1):
    highVal = [0 for _ in range(derivDeg)] + [1] + [0 for _ in range(derivDeg + 1, highOrd + 1)]
    poly = Hermite(lowVal, highVal, end)
    result.append(poly)

  return result


if __name__ == "__main__":
  molL = MolSet((1,1), (0,1))

  for mol in molL:
    print(mol)
