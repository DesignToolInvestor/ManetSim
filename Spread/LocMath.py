#
# L o c M a t h . p y
#
# TODO:  Move inside some larger library, perhaps called ParkerLevy
#

import math
import random

def Sqr(num):
    return num*num


def VecDiff(node0, node1):
    return (node1[0] - node0[0], node1[1] - node0[1])


def Len(vec):
    return math.sqrt(Sqr(vec[0]) + Sqr(vec[1]))


def Dist(node0, node1):
    return Len(VecDiff(node0,node1))



def Interp(seg, pathFrac):
    start,stop = seg

    vecDiff = VecDiff(start,stop)
    result = [start[0] + pathFrac * vecDiff[0], start[1] + pathFrac * vecDiff[1]]

    return result


def RandLog(min, max):
    return math.exp(random.uniform(math.log(min), math.log(max)))