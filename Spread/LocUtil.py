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