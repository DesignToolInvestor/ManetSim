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


# This is using a continued fraction expansion
# TODO:  create 2 pages in the programing manual with a proof of why this works
def RealToFrac(num, eps=1e-6):
    whole = []
    while abs(num) > eps:
        num = 1 / num
        lastWhole = round(num)
        whole.append(lastWhole)
        num -= lastWhole

    result = Frac(1, whole[len(whole) - 1])
    for k in range(len(whole) - 2, -1, -1):
        result = Frac(1, 1 + result)

    return result