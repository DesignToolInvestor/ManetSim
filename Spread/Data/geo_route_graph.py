#
# g e o _ r o u t e _ g r a p h . p y
#

# TODO:  should be moved to a different project.
import math
from scipy import stats

# system libraries
import matplotlib.pyplot as plot

# local libraries
from LocUtil import UnZip, MinMax, Grid1

if __name__ == '__main__':
    # constants
    NUM_GRAPH_POINT = 30
    FILE_NAME = "geo_route_5.log"

    # read data
    with open(FILE_NAME, "r") as file:
        # TODO: can this be done on one line
        lineL = file.readlines()
        infoL = list(map(eval, lineL))

    n = list(map(lambda info: info[0][0], infoL))
    fracGood = list(map(lambda info: info[1][1] / info[1][0], infoL))

    # graph dots
    fig, ax = plot.subplots(figsize=(9,6.5))
    ax.semilogx(n,fracGood, 'or', markersize=3)

    # fit data to power function
    # logN = list(map(math.log, n))
    # logTime = list(map(math.log, time))
    #
    # fit = stats.linregress(logN,logTime)
    # slope = fit.slope
    # intercept = fit.intercept

    # graph fit
    # minN, maxN = MinMax(n)
    # fitX = Grid1(minN, maxN, NUM_GRAPH_POINT)
    # fitY = list(map(lambda x: math.exp(slope * math.log(x) + intercept), fitX))
    # plot.loglog(fitX, fitY, color='blue', label='fit', linewidth=3)

    # add annotation
    plot.xlabel('Num Nodes')
    plot.ylabel('Fraction of Success')

    # TODO: clean up formatting
    # legend = f'{math.exp(intercept)} * n^{slope}'
    # plot.text(2e3, 2, legend)
    # TODO: Automate the extraction of the value of rho
    plot.title(f'Geo-Routing (rho = {5})')

    # save figure
    plot.savefig('geo_route.png', dpi=200)

    # TODO: add second graph that shows the time per element