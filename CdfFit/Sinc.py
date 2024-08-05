#
# S i n c . p y
#

# This file defines functions for fitting to sinc approximations to noise data.

from numpy import sinc
from scipy.linalg import lstsq

from LocUtil import Grid1, MinMax, UnZip


def FitLstSqr(samp, zRange,nSinc):
  sampZ, sampV = UnZip(samp)
  sincZ = Grid1(*zRange, nSinc)
  h = (zRange[1] - zRange[0]) / (nSinc - 1)

  mat = []
  for z in sampZ:
    row = []
    for sp in sincZ:
      row.append(sinc((z - sp) / h))
    mat.append(row)

  sincV, residue, rank, singVal = lstsq(mat, sampV)

  if rank < nSinc:
    residue = 0
    condNum = float('inf')
  else:
    condNum = singVal[0] / singVal[len(singVal) - 1]

  return (tuple(zip(sincZ,sincV)), residue, condNum)


def InterpZ(sincZ, sincV, grid):
  h = sincZ[1] - sincZ[0]

  result = []
  for z in grid:
    val = 0
    for (sp, sv) in zip(sincZ,sincV):
      val += sv * sinc((z - sp) / h)
    result.append(val)

  return result

def QuadZ(sincPoint):
  _,sincV = UnZip(sincPoint)
  result = sum(sincV)

  return result


###############################################################
# Stuff to work on a Sinc approximation type
# class SincApp(object):
#   def __init__(self):
#     pass
#
#   def Interp(self, grid):
#     sincX = sincInfo['sincX']
#     sincV = sincInfo['sincV']
#     map = sincInfo['map']
#
#     sincZ = tuple(map.Forward(x) for x in sincX)
#
#     result = []
#     for z in grid:
#       val = 0
#       for (sz, sv) in zip(sincZ,sincV):
#         val += sv * sinc((z - sz) / h)
#       result.append(val)
#
#     return result