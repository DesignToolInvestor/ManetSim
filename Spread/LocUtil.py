#
# L o c U t i l . p y
#

import random

def Index(table, index):
    result = []
    for i in index:
        if type(i) == list:
            value = Index(table, i)
        else:
            value = table[i]

        result.append(value)
    return result


def Grid1(start, stop, nPoint):
    len = stop - start
    return list(map(lambda k: start + len * (k / (nPoint - 1)), range(nPoint)))


def UnZip(zip):
    x = []
    y = []

    for elem in zip:
        x.append(elem[0])
        y.append(elem[1])

    return (x,y)


# Not completed; doesn't work
def PointToXY(pointLines):
    map(lambda line: UnZip(line), pointLines)

    return []


def SetSeed(seed = None, digits = 5):
    MAX_SEED = 10**digits - 1
    if seed == None:
        random.seed()
        seed = random.randint(0, MAX_SEED)
    return seed


def FlattenAll(input):
    result = []

    for elem in input:
        t = type(elem)
        if (t == list) or (t == tuple):
            result.extend(elem)
        else:
            result.append(elem)

    return result


# TODO:  rewrite as a one-liner (ethan)
# TODO:  use sorting to make int O(n * ln(m)) rather than O(n * m)
def ListMinus(a,b):
    result = []
    for elem in a:
        if elem not in b:
            result.append(elem)
    return result


def List2Str(inL):
    out = "["

    nIn = len(inL)
    for k in range(nIn - 1):
        out += str(inL[k]) + ", "

    out += str(inL[nIn - 1]) + "]"

    return out


def MaskToIndex(mask):
    result = []
    for i in range(len(mask)):
        if mask[i]:
            result.append(i)

    return result


def MapInverse(map_, nOld):
    assert(max(map_) < nOld)
    invMap = [-1 for _ in range(nOld)]
    for newId in range(len(map_)):
        oldId = map_[newId]
        invMap[oldId] = newId

    return invMap