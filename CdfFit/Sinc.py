#
# S i n c . p y
#

# This file defines functions for fitting to sinc approximations to noise data.

from math import floor, ceil
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


def Interp(sincPoint, grid):
  h = sincPoint[1][0] - sincPoint[0][0]  # TODO:  the goal is to make an ADT (automatic data type)

  result = []
  for z in grid:
    val = 0
    for (sp, sv) in sincPoint:
      val += sv * sinc((z - sp) / h)
    result.append(val)

  return result
