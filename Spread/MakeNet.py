#
# M a k e N e t . p y
#

import math
import random

import LocMath

#######################################
# helper functions for dealing with density
def MedStreamLern(r):
    return r * 0.8919521800533872


def MeanStreamLen(r):
    return r * 0.9057653371064005


def Rho(n, r):
    return math.pi * LocMath.Sqr(r) / n


def R(n, rho):
    return math.sqrt(n / rho / math.pi)


#######################################
# make random node locations
def RandNodeCirc(n, maxRad) -> list[[float,float]]:
    result = []
    for i in range(n):
        angle = random.random() * 2 * math.pi
        radQ = random.random()
        rad = math.sqrt(radQ * maxRad*maxRad)
        x = rad * math.cos(angle)
        y = rad * math.sin(angle)
        result.append([x,y])
    return result


#######################################
# brute force link discovery
def FindBiLinksSlow(nodeLoc) -> list[int,int]:
    n = len(nodeLoc)

    link = []
    for k in range(n):
        for j in range(k+1,n):
            if LocMath.Dist(nodeLoc[k],nodeLoc[j]) < 1:
                link.append([k,j])

    return link


# TODO:  Think about rather links should be sorted or not.  Right now they are not.
def FindDirLinksSlow(nodeLoc) -> list[int,int]:
    n = len(nodeLoc)

    link = []
    for k in range(n):
        for j in range(k+1,n):
            if LocMath.Dist(nodeLoc[k],nodeLoc[j]) < 1:
                link.append([k,j])
                link.append([j,k])

    return link


###############################################################################
# fast link discovery


###############################################################################
def RandNetCirc(n,r, dir=False) -> [list[[float,float], list[int,int]]]:
    nodeLoc = RandNodeCirc(n, r)

    if dir:
        links = FindDirLinksSlow(nodeLoc)
    else:
        links = FindBiLinksSlow(nodeLoc)

    return (nodeLoc, links)