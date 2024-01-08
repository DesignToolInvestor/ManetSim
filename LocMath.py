#
# L o c M a t h . p y
#
# TODO:  Move inside some larger library, perhaps called ParkerLevy
#

import math

def Sqr(num):
    return num*num


def Dist(node1, node2):
    return math.sqrt(Sqr(node2[0] - node1[0]) + Sqr(node2[1] - node1[1]))


def Len(vector):
    return math.sqrt(Sqr(vector[0]) + Sqr(vector[1]))
