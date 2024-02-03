#
# L o c U t i l . p y
#

import random


# TODO:  consider changing this to return an iterator rather than a list (might be faster)
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


# works with either a list of lists or a list of tuples
def UnZip(zip):
    firstElem = zip[0]
    if not isinstance(firstElem, list) and not isinstance(firstElem, tuple):
        return zip
    else:
        nOut = len(zip[0])
        result = [[] for _ in range(nOut)]

        for elem in zip:
            for k in range(nOut):
                result[k].append(elem[k])

        return result

def SetSeed(seed=None, digits=5):
    if seed == None:
        random.seed()
        maxSeed = 10 ** digits - 1
        seed = random.randint(0, maxSeed)

    random.seed(seed)

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


def Select(func, list_):
    result = []
    for i in range(len(list_)):
        if func(list_[i]):
            result.append(list_[i])

    return result


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


def MinMax(list_):
    min_ = max_ = list_[0]
    for i in range(1, len(list_)):
        if list_[i] < min_:
            min_ = list_[i]
        if list_[i] > max_:
            max_ = list_[i]

    return [min_, max_]


def Unique(list_):
    sortList = sorted(list_.copy())

    prev = sortList[0]
    result = [prev]

    for elem in sortList[1:]:
        if elem != prev:
            result.append(elem)
            prev = elem
    
    return result


def Partition(func, list_):
    trueL = []
    falseL = []
    for elem in list_:
        if func(elem):
            trueL.append(elem)
        else:
            falseL.append(elem)

    return (trueL, falseL)

def Group(func, list_):
    sortList = sorted(list_.copy(), key=func)

    prevKey = func(sortList[0])
    group = [sortList[0]]
    result = []

    for elem in sortList[1:]:
        key = func(elem)
        if key == prevKey:
            group.append(elem)
        else:
            result.append(group)
            prevKey = key
            group = [elem]

    result.append(group)

    return result


def MinIndex(list_):
    minIndex = 0
    for i in range(1, len(list_)):
        if list_[i] < list_[minIndex]:
            minIndex = i
    return minIndex

def IndexOfFirst(func, list_):
    for i in range(len(list_)):
        if func(list_[i]):
            return i

    return None


def Swap(list_, index0, index1):
    temp = list_[index0]
    list_[index0] = list_[index1]
    list_[index1] = temp
