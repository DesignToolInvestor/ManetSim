#
# S i n c F i t . p y
#

# This file defines functions for fitting to sinc approximations to noise data.

from math import floor, ceil
from numpy import sinc
from scipy.linalg import lstsq

from LocUtil import Grid1, MinMax

def Fit(sampZ, resZ, h):
  zMin, zMax = MinMax(sampZ)
  nSinc = floor((zMax - zMin) / h) + 1

  zMid = (zMin + zMax) / 2
  sincRange = h * (nSinc - 1)

  sincPointZ = Grid1(zMid - sincRange/2, zMid + sincRange/2, nSinc)

  mat = []
  for z in sampZ:
    row = []
    for sp in sincPointZ:
      row.append(sinc((z - sp) / h))
    mat.append(row)

  sincVal, residue, rank, singVal = lstsq(mat, resZ)

  if rank < len(sincPointZ):
    residue = 0
    condNum = float('inf')
  else:
    condNum = singVal[0] / singVal[len(singVal) - 1]

  return (tuple(sincVal), sincPointZ, residue, condNum)