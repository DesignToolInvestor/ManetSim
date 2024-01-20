#
# f l o w _ g r a p h . p y
#

# system packages
import argparse
from matplotlib import pyplot as plot
import math
from scipy import stats

# local packages
import LocUtil
import LocMath


#######################################
def ParseArgs():
    parser = argparse.ArgumentParser(
        prog='flow_graph',
        description='This program will graph the speed of the '
    )

    # TODO:  Add argument for size of graph
    parser.add_argument('fileName', type=str)
    args = parser.parse_args()

    return args.fileName


#######################################
if __name__ == '__main__':
    # constants
    NUM_POINT = 30

    # parse command line
    fileName = ParseArgs()

    # read file
    with open(fileName, 'r') as file:
        logData = list(map(eval, file.readlines()))

    # select data
    data = LocUtil.Select(lambda info: len(info[3]) == 2, logData)

    # extract data
    graphData = map(lambda info: [info[0], info[4]], data)
    n,time = LocUtil.UnZip(graphData)

    # graph data
    fig,ax = plot.subplots(figsize=(6.5, 6.5))
    plot.loglog(n,time, 'ro',markersize=4)

    # fit line
    logTime = list(map(math.log, time))
    logN = list(map(math.log, n))
    fit = stats.linregress(logN,logTime)

    slope = fit.slope
    intercept = fit.intercept
    print(f'slope: {fit.slope}')

    # graph
    minN,maxN = LocUtil.MinMax(n)
    fitX = LocUtil.Grid1(minN,maxN, NUM_POINT)
    fitY = list(map(lambda x: math.exp(slope * math.log(x) + intercept), fitX))
    plot.loglog(fitX,fitY, color='blue', label='fit')

    # TODO:  Add axis labels and text stating the fit

    # save figure
    plot.savefig('flow_graph.png', dpi=200)
    # plot.show()