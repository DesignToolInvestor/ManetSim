#
# L o c M a t h . p y
#
# TODO:  Move inside some larger library, perhaps called ParkerLib
#

import random

from fractions import Fraction as Frac
from heapq import heapify, heappop, heappush
from math import acos, atan2, exp, log, log10, isclose, pi, sqrt, tan
from statistics import median

from LocUtil import MinIndex, MaxIndex, Partition, Sub

###############################################################
def Interp1(low,high,frac):
  return frac*(high-low)+low


def LogInterp1(low,high,frac):
  logLow = log(low)
  logHigh = log(high)
  logResult = frac * (logHigh - logLow) + logLow

  return exp(logResult)


def Interp2(start,stop, frac):
  x0,y0 = start
  x1,y1 = stop
  return (Interp1(x0,x1, frac), Interp1(y0,y1, frac))


###############################################################
# 2d point or vector operations
# TODO:  create a point class ... this is wildly out of hand ... doing so will allow operator
#  overloading
def Sqr(num):
  return num*num


def Diff(node0, node1):
  return (node1[0] - node0[0], node1[1] - node0[1])


def MagSqr(vec):
  return Sqr(vec[0]) + Sqr(vec[1])


def Mag(vec):
  return sqrt(MagSqr(vec))


def DistSqr(loc0, loc1):
  return MagSqr(Diff(loc0,loc1))


def Dist(node0, node1):
  return sqrt(DistSqr(node0, node1))


def Ang(start,end):
  return atan2(end[1] - start[1], end[0] - start[0])


def Interp(seg, frac):
  start,stop = seg

  vecDiff = Diff(start,stop)
  result = [start[0] + frac * vecDiff[0], start[1] + frac * vecDiff[1]]

  return result


def Cent(seg):
  return Interp(seg, 1/2)


def Scale(scale, point):
  return (scale * point[0], scale * point[1])


def Add(a,b):
  return (a[0] + b[0], a[1] + b[1])


def Perp(vec):
  x,y = vec
  dist = Mag(vec)
  result = (-y/dist, x/dist)

  return result


###############################################################
def RoundDivMod(num):
  whole = round(num)
  rem = num - whole

  return [whole,rem]


def ContFrac(numer):
  n = len(numer)

  result = Frac(1, numer[n-1])
  for i in range(n-2, -1, -1):
    result = 1 / (numer[i] + result)

  return result


# This is using a continued fraction expansion
# TODO:  create 2 pages in the programing manual with a proof of why this works
# TODO:  Do a cleaner job of dealing with the end cases
def RealToFrac(num, eps=1e-6):
  if abs(num) < eps:
    return 0
  else:
    numWhole,rem = RoundDivMod(num)
    diff = rem

    whole = []
    while abs(diff) > num*eps:
      w,rem = RoundDivMod(1/rem)
      whole.append(w)

      approx = numWhole + ContFrac(whole)
      diff = num - approx

    if whole == []:
      return numWhole
    else:
      return numWhole + ContFrac(whole)


###############################################################
def RandLog(min, max):
  return exp(random.uniform(log(min), log(max)))


def LogRange(low,high, majicNum):
  logMajicNum = [log10(num) for num in majicNum]

  lowDec,logLowFrac = divmod(log10(low), 1)
  highDec,logHighFrac = divmod(log10(high), 1)

  lowIndex = MinIndex([abs(majic - logLowFrac) for majic in logMajicNum])
  highIndex = MinIndex([abs(majic - logHighFrac) for majic in logMajicNum])

  result = []
  decade = lowDec
  majicIndex = lowIndex

  # tricky logic
  while not ((highDec < decade) or ((decade == highDec) and (highIndex < majicIndex))):
    result.append(majicNum[majicIndex] * 10**decade)

    if majicIndex < len(majicNum) - 1:
      majicIndex += 1
    else:
      majicIndex = 0
      decade += 1

  return result


def IsClose(a,b, rel_tol=1e-09, abs_tol=0.0):
  aLen = len(a)
  if (aLen != len(b)):
    return False
  else:
    close = isclose(a[0],b[0], rel_tol=rel_tol, abs_tol=abs_tol)
    i = 0
    while close and (i < aLen):
      close = isclose(a[i],b[i], rel_tol=rel_tol, abs_tol=abs_tol)
      i += 1

    return close


def Wrap(data, low,high):
  range = high - low

  if isinstance(data,list):
    result = [Wrap(v,low,high) for v in data]
  else:
    result = (data - low) % range + low

  return result


###############################################################
def CircDiff(list_):
  listLen = len(list_)
  return [list_[(k+1) % listLen] - list_[k] for k in range(listLen)]


def MaxGapAng(angL):
  listLen = len(angL)
  if listLen == 0:
    return 0;
  elif listLen == 1:
    return Wrap(angL[0] + pi, 0,2*pi)
  else:
    angL.sort()
    temp = CircDiff(angL)
    gapAng = Wrap(temp, 0,2*pi)

    maxGapIndex = MaxIndex(gapAng)
    ang0 = angL[maxGapIndex]
    midAng = Wrap(ang0 + gapAng[maxGapIndex] / 2, 0,2*pi)

    return midAng


###############################################################
def RobustLine(x,y):
  centX = median(x)
  centY = median(y)

  # TODO: can do without partitioning with wrapping ... think about rather this is better
  left,right = Partition(lambda p: p[0] < centX, list(zip(x,y)))

  temp = [atan2(y - centY, x - centX) for (x,y) in left]
  temp1 = Wrap(temp, 0, 2*pi)
  angLeft = list(map(lambda a: a - pi, temp1))
  angRight = [atan2(y - centY, x - centX) for (x,y) in right]

  ang = angLeft + angRight
  medAng = median(ang)

  slope = tan(medAng)
  inter = centY - tan(medAng) * centX

  return ((slope,inter), (centX,centY))


##############################################################
def PowerSet(n):
  # not intended for large n, check for accidental use with large n
  assert(n < 28)

  lim = (1 << n)
  result = []
  for num in range(lim):
    nextSet = []
    for bNum in range(n):
      bit = num & (1 << bNum)
      if bit != 0:
        nextSet.append(bNum)
    result.append(tuple(nextSet))

  return tuple(result)


def PowerSetTup(n):
  # not intended for large n, check for accidental use with large n
  assert(n < 30)

  lim = (1 << n)
  result = tuple(tuple(i for i in range(n) if (num & (1 << i))) for num in range(lim))

  return tuple(result)


#################################################
def CircClipCirc(circ, clipCirc):
  circCent, circRad = circ
  clipCent, clipRad = clipCirc

  clipToCirc = Dist(circCent, clipCent)
  if (clipRad + circRad) < clipToCirc:
    return None

  elif (clipToCirc + circRad) < clipRad:
    return (circCent, (0, 2 * pi))

  else:
    baseAng = Ang(clipCent, circCent)
    angChange = acos(
      (Sqr(clipRad) - Sqr(circRad) - Sqr(clipToCirc)) / (2 * circRad * clipToCirc))
    return (circCent, (baseAng - angChange, baseAng + angChange))


#################################################
def Bisect(func, val, range_, tol=1e-12):
  low,high = range_

  lowVal = func(low)
  highVal = func(high)
  if (lowVal <= val) and (val <= highVal):
    sign = 1
  elif (highVal <= val) and (val <= lowVal):
    sign = -1
  else:
    raise Exception("end point don't straddle value")

  while tol < (high - low):
    mid = (high + low) / 2
    midVal = func(mid)

    if 0 < (val - midVal)*sign:
      low = mid
    else:
      high = mid

  return (high + low) / 2


#######################################
def SymEq(a,b):
  diff = (a - b).simplify()
  return (diff == 0)

###############################################################
# FFT Folding and UnFolding Functions
def FftUnFold(n, data):
  if (n % 2):    # that is if odd
    mid = (n - 1) // 2
    result = tuple(Sub(data, range(mid + 1, n))) + tuple(Sub(data, range(mid)))
  else:    # that is if even
    mid = n // 2
    result = tuple(Sub(data, range(mid, n))) + tuple(Sub(data, range(mid)))

  return result


# TODO:  return energy ... adding positive and negative frequency components might be wrong
def FftUnFoldReal(n, data):
  if (n % 2):    # that is, if odd
    mid = (n - 1) // 2
    result = (data[0],) + tuple(data[k] + data[n-k] for k in range(1, mid + 1))
  else:    # that is, if even
    mid = n // 2
    result = (data[0],) + tuple(data[k] + data[n-k] for k in range(1, mid)) + (data[mid],)

  return result
