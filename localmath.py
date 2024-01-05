#
# localmath.py
#
# TODO:  Move inside some larger library, perhaps called ParkerLevy
#

import math

def Sqr(num):
    return num*num

# TODO:  Move to project math library
def Dist(node1, node2):
    return math.sqrt(Sqr(node2[0] - node1[0]) + Sqr(node2[1] - node1[1]))