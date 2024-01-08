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