#
# s e t _ l i k e _ p l o t . p y
#

# system packages
import argparse
from matplotlib import pyplot as plot
from math import log, exp
from statistics import median

# open source packages
from engineering_notation import EngNumber

# local packages
from LocUtil import LogGrid1, UnZip
from LocMath import LogInterp1


#########################################
# global constants
nGridPoint = 30


#########################################
def LinFit(data):
    xRaw,_ = UnZip(data)
    intercept = median(y/x for (x,y) in data)

    xL = LogGrid1(min(xRaw),max(xRaw), nGridPoint)
    yL = [intercept*x for x in xL]

    text = f'{EngNumber(intercept)}s * N'
    return (xL,yL, text)


def ConstFit(data):
    xRaw,yRaw = UnZip(data)
    val = median(yRaw)

    xL = LogGrid1(min(xRaw),max(xRaw), nGridPoint)
    yL = [val for x in xL]

    text = f'{EngNumber(val)}s'
    return (xL, yL, text)


def LogFit(data):
    xRaw,yRaw = UnZip(data)
    const = median([y / log(x) for (x,y) in data]) * log(2)

    xL = LogGrid1(min(xRaw),max(xRaw), nGridPoint)
    yL = [const * log(x)/log(2) for x in xL]

    text = f'{EngNumber(const)}s * log[2](N)'
    return (xL, yL, text)


#########################################
def ParseArgs():
    # set up
    parser = argparse.ArgumentParser(
        prog="set_like",
        description='This script generates timing data for set like operations'
    )

    parser.add_argument('impType', type=str)

    # parse args
    args = parser.parse_args()

    # deal with impType
    if args.impType == 'list':
        fitInfo = (LinFit, 'Python List', 1e6, 'Microseconds')
    elif args.impType == 'set':
        fitInfo = (ConstFit, 'Python Set', 1e9, 'Nanoseconds')
    elif args.impType == 'dict':
        raise Exception('not yet implemented')
    elif args.impType == 'sort':
        fitInfo = (LogFit, 'Sorted List', 1e6, 'Microseconds')
    else:
        raise Exception("Implementation type must be 'list', 'set', 'dict', or 'sort'")

    # return results
    return [args.impType, fitInfo]


#########################################
if __name__ == '__main__':
    # constants
    fileNameBase = 'set_set'

    # parse args
    impType, (fitF,impName,unitScale,unitName) = ParseArgs()

    # read data
    with open(f'set_{impType}.log', 'r') as file:
        lineL = file.readlines()
    
    # pattern match on the data
    info = [eval(line) for line in lineL]
    setInfo,resultInfo = UnZip(info)
    setSize,_ = UnZip(setInfo)
    _,hitRatio,time = UnZip(resultInfo)
    
    # fit to data
    if any(t <= 0 for t in time):
        raise Exception('Some data is identically zero (likely due to rounding)')

    # plot data
    fig, ax = plot.subplots(figsize=(9, 6.5))

    y = [unitScale * t for t in time]
    plot.loglog(setSize,y,'o', markersize=3, color='maroon', zorder=0)

    # plot fit
    xFit,yFit,text = fitF(list(zip(setSize,time)))
    print(text)

    yFit = [y * unitScale for y in yFit]
    plot.loglog(xFit,yFit, linewidth=2, color="darkblue", zorder=1)

    # Annotate
    plot.xlabel('Set Size')
    plot.ylabel(f'{unitName} per Search')
    plot.title(f'Implemented as {impName}')

    x = LogInterp1(*ax.get_xlim(), 1/5)
    y = LogInterp1(*ax.get_ylim(), 2/3)
    plot.text(x,y, text, ha='left', va='top')

    # save figure
    plot.savefig(f'set_{impType}.png')
    plot.show()