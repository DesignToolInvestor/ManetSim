#
# L o c U t i l . p y
#


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