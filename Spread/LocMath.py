#
# L o c M a t h . p y
#
# TODO:  Move inside some larger library, perhaps called ParkerLevy
#

from fractions import Fraction as Frac
import math
import random

def Sqr(num):
    return num*num


def Diff(node0, node1):
    return (node1[0] - node0[0], node1[1] - node0[1])


def MagSqr(vec):
    return Sqr(vec[0]) + Sqr(vec[1])


def Mag(vec):
    return math.sqrt(MagSqr(vec))


def DistSqr(loc0, loc1):
    return MagSqr(Diff(loc0,loc1))


def Dist(node0, node1):
    return math.sqrt(DistSqr(node0, node1))


def Interp(seg, pathFrac):
    start,stop = seg

    vecDiff = Diff(start,stop)
    result = [start[0] + pathFrac * vecDiff[0], start[1] + pathFrac * vecDiff[1]]

    return result


def RandLog(min, max):
    return math.exp(random.uniform(math.log(min), math.log(max)))


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