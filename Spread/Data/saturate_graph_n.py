#
# s a t u r a t e _ g r a p h _ n . p y
#

# system packages
import argparse
from matplotlib import pyplot as plot
import math
import statistics
from scipy import optimize, stats

# local packages
from LocUtil import Grid1, Group, Select, UnZip
from LocMath import LogRange, RobustLine
import SatLog

#######################################
# graphing functions
def AddMedFlowScale(ax, medFlowLen, maxNumStream, maxCap):
    axAlt = ax.secondary_yaxis(
        location='right', functions=(lambda c: c / medFlowLen, lambda s: s * medFlowLen))

    maxFlowLine = math.floor(maxCap / medFlowLen)
    for numFlow in range(1, maxFlowLine + 1):
        y = numFlow * medFlowLen
        plot.plot([1, maxNumStream], [y,y], linestyle='--', linewidth=0.6, color='green')

    axAlt.set_ylabel('Effective Num of Streams (at 100%)')
    return ax


#######################################
def ParseArgs():
    parser = argparse.ArgumentParser(
        prog='saturate_graph_n',
        description='Graph maximum flow rate for random streams over a range of sizes'
    )

    # TODO:  Add argument for size of graph
    parser.add_argument('fileName', type=str)
    args = parser.parse_args()

    return [args.fileName]

#######################################
def Fit(data):
    x,y = UnZip(data)

    form = lambda x, a0, b0:  b0*x / (x + a0)
    [a0,b0],cov = optimize.curve_fit(form,x,y)

    return (a0, b0)


def Lim(data):
    a0,b0 = Fit(data)
    return b0


#######################################
if __name__ == '__main__':
    # constants
    numGraphPoint = 30

    # parse command line
    fileName = ParseArgs()[0]

    # read file
    logData = SatLog.ReadSatLog(fileName)
    if logData == []:
        raise Exception('No data found in file')

    rho = logData[0].rho

    # group by nNode & netSeed
    groupL = Group(lambda elem: (elem.nNode,elem.netSeed), logData)
    nGroup = len(groupL)

    # for each group fit
    result = []
    for group in groupL:
        groupXY = [(elem.nStream, elem.AgFlow()) for elem in group]
        nNode = group[0].nNode
        result.append((nNode, Lim(groupXY)))

    # graph base data
    fig,ax = plot.subplots(figsize=(9, 6.5))

    result = Select(lambda p: p[1] < 200, result)
    xL,yL = UnZip(result)

    # graph dots
    plot.loglog(xL,yL, 'ro',markersize=4, zorder=0)

    plot.xlabel('Num of Node')
    plot.ylabel('Estimated Limit of Flow')

    plot.rcParams['text.usetex'] = True
    plot.title(r'Rho = $\sqrt[3]{{ 5 }} \approx 1.71$')

    # fit
    logX = list(map(math.log, xL))
    logY = list(map(math.log, yL))

    # fit = stats.linregress(logX, logY)
    (slope,intercept), _ = RobustLine(logX,logY)

    # TODO:  clean up
    minLogX = min(logX)
    maxLogX = max(logX)
    logXFit = Grid1(minLogX,maxLogX, numGraphPoint)
    logYFit = list(map(lambda x: slope * x + intercept, logXFit))
    xFit = list(map(math.exp, logXFit))
    yFit = list(map(math.exp, logYFit))

    plot.loglog(xFit,yFit, 'b', linewidth=3, zorder=1)

    # add annotation
    # TODO:  automatically put in the north-west
    logXCent = (minLogX + maxLogX) / 2
    xCent = math.exp(logXCent)
    yCent = math.exp(slope * logXCent + intercept)
    plot.text(
        xCent, yCent, f'${math.exp(intercept):.2f} \cdot N^{{{slope:.2f}}}$',
        ha='center', va='center', fontsize=15,
        bbox=dict(facecolor='white', edgecolor='none'), zorder=2)

    # add tick marks
    # TODO:  automate this
    tickNum = [1,2,3,5]

    xTick = LogRange(min(xL),max(xL), tickNum)
    xTickStr = list(map(str, xTick))
    plot.xticks(ticks=xTick, labels=xTickStr)

    yTick = LogRange(min(yL),max(yL), tickNum)
    yTickStr = list(map(str, yTick))
    plot.yticks(ticks=yTick, labels=yTickStr)

    # save figure
    outFileName = 'lim_flow_cbrt(5).png'
    plot.savefig(outFileName, dpi=200)
    plot.show()
