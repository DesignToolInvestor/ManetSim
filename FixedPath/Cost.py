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


#######################################
def MetricArg(metricArg, gamma,snirDb):
    # deal with metric
    if metricArg == "hc":
            metric = ("hc", "hop count")
            costF = lambda p0,p1: 1
    elif metricArg == "sp":
            metric = ("sp", "shortest path")
            costF = R
    elif metricArg == "xr":
            metric = ("xr", "exclusion range")
            snir = 10 ** (snirDb / 20)
            costF = lambda p0,p1: ExcluR(p0,p1, gamma, snir)
    elif metricArg == "xa":
            metric = ("xa", "exclusion area")
            snir = 10 ** (snirDb / 20)
            costF = lambda p0,p1: ExcluArea(p0,p1, gamma, snir)
    else:
            raise Exception("Must specify metric.  Either 'hc'. sp', 'xr', or 'xa'")

    return (costF, metric)