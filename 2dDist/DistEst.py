#
# D i s t E s t . p y
#

# This file fits a distribution to a set of samples.  It returns a SincApprox class for the CDF
# that can be differentiated to produce an estiment of the PDF.


from scipy.linalg import lstsq
from sympy import Symbol

from Sinc import SincD, SincApprox
from LocUtil import Flatten


def DistFit(samp, nSinc, map, xSym, zSym, nullOrd, asym):
  # parse arguments
  nSamp = len(samp)

  # make CDF
  sampSort = sorted(samp)
  quant = [(k + 0.5) / nSamp for k in range(nSamp)]

  # map to z
  mapF = map.MapExp().lambdafy(xSym)
  sampZ = [mapF(x) for x in sampSort]

  # shift
  minZ, maxZ = MinMax(sampZ)
  z0 = (maxZ + minZ) / 2

  sampZs = [z - z0 for z in sampZ]

  # find the best scale
  scale = 1

  sampZss = [scale * zs for zs in sampZs]

  # compute the mollifyer set
  leftMolOrd = len(asym[0])
  rightMolOrd = len(asym[1])

  molSetZ = Flatten(MolSetZ(leftMolOrd, rightMolOrd))

  # Compute the fixed mollifyer
  flatAsym = Flatten(asym)
  fixSpec = [(i, val) for (i, val) in enumerate(flatAsym) if val != '*']

  molFixedZ = sum(val * molSetZ[i] for (i, val) in fixSpec)

  # compute the residue
  sampMol = [molFixedZ.subs(z, zss).evalf() for zss in sampZss]
  sampRes = [q - m for (q, m) in zip(quant, sampMol)]

  # construct sinc points
  h = (maxZ - minZ) / (nSinc - 1)
  sincPointZ = [k * h + minZ for k in range(nSinc)]

  # construct the nullifyer
  nullOrdLeft, nullOrdRight = nullOrd
  nullZ = map.NullLeftZ() ** nullOrdLeft * map.NullRightZ() ** nullOrdRight

  # construct sinc basis
  sp = Symbol('sp')
  sincBase = SincD(0, scale * (map.MapExp() - z0 - sp) / h) * nullZ

  # make matrix and RHS
  floatMol = [i for (i, val) in enumerate(flatAsym) if val == '*']

  mat = []
  rhs = []

  for zV in sampZss:
    rowMol = [molSetZ[i].subs(zSym, zV).evalf() for i in floatMol]
    rowSinc = [sincBase.subs({z: zV, sp: spV}).evalf() for spV in sincPointZ]
    row = rowMol + rowSinc

    mat.append(row)
    rhs.append(sampRes)

  # solve system
  temp, _, _, _ = lstsq(mat, rhs)
  weight = tuple(temp)

  # return sinc approx
  sincWeight = weight[nSinc : ]

  molWeight = weight[0 : nSinc]
  molAllZ = molFixedZ + sum(val * molSetZ[i] for (i, val) in zip(floatMol,molWeight))
  molAllX = molAllZ.subs(zSym, map.MapExp())

  nullX = nullZ.subs(zSym, map.MapExp())

  mapSs = map.ShiftScale(z0, scale)

  approx = SincApprox(mapSs, sincWeight, molAllX, nullX)
  return approx
