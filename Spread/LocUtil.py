#
# L o c U t i l . p y
#

from math import log, exp
import random
import sys


# TODO:  consider changing this to return an iterator rather than a list (might be faster)
def Sub(table, index):
    result = []
    for i in index:
        if type(i) == list:
            value = Sub(table, i)
        else:
            value = table[i]

        result.append(value)
    return result


def Grid1(start, stop, nPoint):
    len = stop - start
    return [start + len * (k / (nPoint - 1)) for k in range(nPoint)]

def LogGrid1(start, stop, nPoint):
    logStart = log(start)
    logStop = log(stop)
    logRange = logStop - logStart

    result = [exp(logStart + logRange * (k / (nPoint - 1))) for k in range(nPoint)]
    return result

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


# TODO:  combine with Flatten
def FlattenAll(input):
    result = []

    for elem in input:
        t = type(elem)
        if (t == list) or (t == tuple):
            result.extend(elem)
        else:
            result.append(elem)

    return result


# use numLev=0 to flatten to all levels
def Flatten(list_, numLev=1):
    result = []

    for elem in list_:
        t = type(elem)
        if (t != list) and (t != tuple) and (t != set):
            result.append(elem)
        elif (numLev == 1):
            result.extend(elem)
        else:
            result.extend(Flatten(elem, numLev - 1))

    return result


def List2Str(inL):
    out = "["

    nIn = len(inL)
    for k in range(nIn - 1):
        out += str(inL[k]) + ", "

    out += str(inL[nIn - 1]) + "]"

    return out


# TODO: Deprecated.  Replace with [x for x in l if f(x)]
def Select(func, list_):
    result = []
    for elem in list_:
        if func(elem):
            result.append(elem)

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


def MinIndex(list_):
    minIndex = 0
    for i in range(1, len(list_)):
        if list_[i] < list_[minIndex]:
            minIndex = i
    return minIndex


# originally created to support lists of tuples which is not supported by the system index method
def Index(list_, elem):
    listLen = len(list_)
    index = 0
    while (index < listLen) and (list_[index] != elem):
        index += 1

    if index == listLen:
        return None
    else:
        return index


###########################################
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



def MaxIndex(list_):
    maxIndex = 0
    for i in range(1, len(list_)):
        if list_[maxIndex] < list_[i]:
            maxIndex = i
    return maxIndex


def IndexOfFirst(func, list_):
    for i in range(len(list_)):
        if func(list_[i]):
            return i

    return None


def Swap(list_, index0, index1):
    temp = list_[index0]
    list_[index0] = list_[index1]
    list_[index1] = temp


#######################################
def ListEq(a,b):
    return (sorted(a) == sorted(b))


def SetEq(a,b):
    sortedA = sorted(a)
    sortedB = sorted(b)

    return (sortedA == sortedB)


def ListMinus(a,b):
    locA = a.copy()
    locB = b.copy()

    locA.sort()
    locB.sort()

    iA = iB = 0
    result = []
    while (iA < len(a)) and (iB < len(b)):
        if locA[iA] == locB[iB]:
            iA += 1
            iB += 1
        else:
            if locA[iA] < locB[iB]:
                result.append(locA[iA])
                iA += 1
            else:
                iB += 1

    # at most one of the loop will execute
    for i in range(iA, len(a)):
        result.append(locA[i])
    for i in range(iB, len(b)):
        result.append(locB[i])
        
    return result


def DebugMode():
    has_trace = hasattr(sys, 'gettrace') and sys.gettrace() is not None
    has_breakpoint = sys.breakpointhook.__module__ != "sys"

    return has_trace or has_breakpoint


def BinIn(ordList, elem):
    lowI = 0
    highI = len(ordList) - 1

    lowElem = ordList[lowI]
    highElem = ordList[highI]

    if (elem < lowElem) or (highElem < elem):
        return False
    elif (elem == lowElem) or (elem == highElem):
        return True
    else:
        while (lowI + 1 < highI):
            midI = (lowI + highI) // 2
            midElem = ordList[midI]

            if (midElem == elem):
                return True
            elif (elem < midElem):
                highI = midI
            else:
                lowI = midI

        return False