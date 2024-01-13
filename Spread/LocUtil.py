#
# L o c U t i l . p y
#

#import random


def Index(table, index):
    result = []
    for k in index:
        result.append(table[k])
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


def SetSeed(seed):
    MAX_SEED = 99_999
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