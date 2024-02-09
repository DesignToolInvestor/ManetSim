#
# L o c M a t h . p y
#
# TODO:  Move inside some larger library, perhaps called ParkerLevy
#

from fractions import Fraction as Frac
from statistics import median
from math import atan2, exp, log, log10, isclose, pi, sqrt, tan
import random

from LocUtil import MinIndex, MaxIndex, Partition

###############################################################
# 2d point or vector operations
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
# returns a list because a dict is much slower
# TODO:  time the spead of a dict vs. a list
def PowerSet(n):
    # not intended for large n, check for accidental use with large n
    assert(n < 30)

    lim = (1 << n)
    result = []
    for num in range(lim):
        set = []
        for bNum in range(n):
            bit = num & (1 << bNum)
            if bit != 0:
                set.append(bNum)
        result.append(set)

    return result