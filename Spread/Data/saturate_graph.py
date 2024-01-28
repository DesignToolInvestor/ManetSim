#
# s t r e a m _ s a t u r a t e _ g r a p h . p y
#

# system packages
import argparse
from matplotlib import pyplot as plot
import math
import statistics
import scipy

# local packages
import LocUtil
import MakeNet

#######################################
# graphing functions
# def GraphData():

# def GraphMed():

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
        prog='flow_graph',
        description='This program will graph the speed of the '
    )

    # TODO:  Add argument for size of graph
    parser.add_argument('fileName', type=str)
    parser.add_argument('-n', type=int)

    args = parser.parse_args()

    return [args.fileName, args.n]

#######################################
if __name__ == '__main__':
    # constants
    numGraphPoint = 30

    # parse command line
    fileName,nSelect = ParseArgs()

    # read file
    with open(fileName, 'r') as file:
        lines = file.readlines()
        logData = list(map(eval, lines))

    # select data
    data = LocUtil.Select(lambda info: info[0][0] == nSelect, logData)
    rho = list(
        map(lambda p: MakeNet.Rho(*p),
            map(lambda info: info[0][0:2], logData)))
    n,rho = data[0][0][:2]

    # extract data
    graphData = list(map(lambda info: [info[1][0], info[1][2] * info[1][3]], data))
    nFlow,cap = LocUtil.UnZip(graphData)

    # group by num of flow
    groupData = LocUtil.Group(lambda p: p[0], graphData)

    med = []
    for group in groupData:
        nStream,agFlow = LocUtil.UnZip(group)
        med.append([nStream[0], statistics.median(agFlow)])

    ###################################
    # fit to medians
    x,y = LocUtil.UnZip(med)
    form = lambda x, a0, b0:  b0*x / (x + a0)

    [a0,b0],cov = scipy.optimize.curve_fit(form,x,y)
    print(f'a0 = {a0}, b0 = {b0}')

    maxNumStream = max(map(lambda p: p[0], graphData))
    xFit = LocUtil.Grid1(1, maxNumStream, numGraphPoint)
    yFit = list(map(lambda x: b0*x / (x + a0), xFit))

    ###################################
    # do main graph
    fig,ax = plot.subplots(figsize=(9, 6.5))
    plot.plot(nFlow,cap, 'ro',markersize=4, zorder=0)

    # plot medians
    x,y = LocUtil.UnZip(med)
    plot.plot(x,y, 'go', markersize=12, zorder=1)

    # plot fit
    plot.plot(xFit,yFit, 'b', linewidth=3, zorder=2)

    # plot asymptote
    yAsym = [b0 for _ in range(numGraphPoint)]
    plot.plot(xFit,yAsym, 'b--', linewidth=2, zorder=2)

    # add text
    r = MakeNet.R(n,rho)
    rMed = MakeNet.MedStreamLern(r)

    # TODO:  create a white background
    plot.text(
        (1 + maxNumStream)/2, b0 + 0.5, f'Asymptote ({b0:.1f} links or {b0/rMed:.2f} streams)',
         ha='center', va='bottom', fontsize=15, zorder=3)

    # median flow scale
    maxCap = max(map(lambda p: p[1], graphData))
    ax = AddMedFlowScale(ax, rMed, maxNumStream, maxCap)

    # labels and title
    ax.set_xlabel("Num of Stream")
    ax.set_ylabel("Aggregate Capacity")
    ax.set_title(f'N = {nSelect}; Rho = {rho}')

    # save figure
    plot.savefig(f'flow_graph_{rho}_{nSelect}_main.png', dpi=200)
    plot.show()

    ###################################
    # do second graph
    # figInv, ax = plot.subplots(figsize=(9, 6.5))
    # x = list(map(lambda x: 1/x, nFlow))
    # plot.plot(x,cap, 'ro',markersize=4,zorder=0)
    #
    # x,y = LocUtil.UnZip(med)
    # x = list(map(lambda x: 1/x, x))
    # plot.plot(x,y, 'b',zorder=1, linewidth=2)
    #
    # plot.savefig(f'flow_graph_{rho}_{nSelect}_inv.png', dpi=200)
    # plot.show()
