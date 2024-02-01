#
# L o c M a t h . p y
#
# TODO:  Move inside some larger library, perhaps called ParkerLevy
#

from fractions import Fraction as Frac
from statistics import median
from math import atan2, exp, log, log10, isclose, pi, sqrt, tan
import random

from LocUtil import MinIndex, Partition


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


def Interp(seg, pathFrac):
    start,stop = seg

    vecDiff = Diff(start,stop)
    result = [start[0] + pathFrac * vecDiff[0], start[1] + pathFrac * vecDiff[1]]

    return result


def RandLog(min, max):
    return exp(random.uniform(log(min), log(max)))


#######################################
def RoundRem(num):
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
    numWhole,rem = RoundRem(num)
    diff = rem

    whole = []
    while abs(diff) > num*eps:
        w,rem = RoundRem(1/rem)
        whole.append(w)

        approx = numWhole + ContFrac(whole)
        diff = num - approx

    if whole == []:
        return numWhole
    else:
        return numWhole + ContFrac(whole)


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


def Wrap(list_, low,high):
    range = high - low
    result = [(v - low) % range + low for v in list_]

    return result


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