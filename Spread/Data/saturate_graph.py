#
# s t r e a m _ s a t u r a t e _ g r a p h . p y
#

# system packages
import argparse
from matplotlib import pyplot as plot
import math
import statistics

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

    axAlt.set_ylabel('Num Median Len Streams (at 100%)')
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
    r = data[0][0][1]

    # extract data
    graphData = list(map(lambda info: [info[1][0], info[1][3]], data))
    nFlow,cap = LocUtil.UnZip(graphData)

    ###################################
    # do first graph
    fig,ax = plot.subplots(figsize=(9, 6.5))
    plot.plot(nFlow,cap, 'ro',markersize=4)

    # plot median
    groupData = LocUtil.Group(lambda p: p[0], graphData)

    med = []
    for group in groupData:
        nStream,agFlow = LocUtil.UnZip(group)
        med.append([nStream[0], statistics.median(agFlow)])

    x,y = LocUtil.UnZip(med)
    plot.plot(x,y, 'b')

    # median flow scale
    medFlowLen = MakeNet.MedStreamLern(r)
    maxNumStream = max(map(lambda p: p[0], graphData))
    maxCap = max(map(lambda p: p[1], graphData))
    ax = AddMedFlowScale(ax, medFlowLen, maxNumStream, maxCap)

    # labels and title
    ax.set_xlabel("Num of Stream")
    ax.set_ylabel("Aggregate Capacity")
    ax.set_title(f'N = {nSelect}; Rho = 2')

    # save figure
    plot.savefig(f'flow_graph_A_{nSelect}.png', dpi=200)
    plot.show()

    ###################################
    # do second graph
    figInv, ax = plot.subplots(figsize=(6.5, 6.5))
    x = list(map(lambda x: 1/x, nFlow))
    plot.plot(x,cap, 'ro',markersize=4)

    x,y = LocUtil.UnZip(med)
    x = list(map(lambda x: 1/x, x))
    plot.plot(x,y, 'b')

    plot.savefig(f'flow_graph_B_{nSelect}.png', dpi=200)
    plot.show()