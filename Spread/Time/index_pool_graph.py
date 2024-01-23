#
# i n d e x _ p o o l _ g r a p h . p y
#

import math
from scipy import stats

# system libraries
import matplotlib.pyplot as plot

# local libraries
from LocUtil import UnZip, MinMax, Grid1

if __name__ == '__main__':
    # constants
    NUM_GRAPH_POINT = 30
    FILE_NAME = "index_pool.log"

    # read data
    with open(FILE_NAME, "r") as file:
        lineL = file.readlines()
        info = list(map(eval, lineL))

    # graph dots
    fig, ax = plot.subplots()
    n,time = UnZip(info)
    ax.loglog(n,time, 'or', markersize=3)

    # fit data to power function
    logN = list(map(math.log, n))
    logTime = list(map(math.log, time))

    fit = stats.linregress(logN,logTime)
    slope = fit.slope
    intercept = fit.intercept

    # graph fit
    minN, maxN = MinMax(n)
    fitX = Grid1(minN, maxN, NUM_GRAPH_POINT)
    fitY = list(map(lambda x: math.exp(slope * math.log(x) + intercept), fitX))
    plot.loglog(fitX, fitY, color='blue', label='fit', linewidth=3)

    # add annotation
    plot.xlabel('Index Size')
    plot.ylabel('Time in Seconds')

    # TODO: clean up formatting
    legend = f'{math.exp(intercept)} * n^{slope}'
    plot.text(2e3, 2, legend)

    # save figure
    plot.savefig('flow_graph.png', dpi=200)

    # TODO: add second graph that shows the time per element