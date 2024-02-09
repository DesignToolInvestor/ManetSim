#
# C o s t . p y
#

# This library contains functions that are used for defining the cost of links

from LocMath import Dist, Sqr
from Interfere import InterDist


def R(loc0, loc1):
    return Dist(loc0, loc1)


def ExcluR(loc0, loc1, gamma, snir):
    dist = Dist(loc0, loc1)
    cost = InterDist(dist, gamma, snir)

    return cost


def ExcluArea(loc0, loc1, gamma, snir):
    dist = Dist(loc0, loc1)
    cost = Sqr(InterDist(dist, gamma, snir))

    return cost
