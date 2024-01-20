#
# s t r e a m _ s a t u r a t e _ g r a p h . p y
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
    NET_SIZE = 200

    # parse command line
    fileName = ParseArgs()

    # read file
    with open(fileName, 'r') as file:
        lines = file.readlines()
        logData = list(map(eval, lines))

    # select data
    data = LocUtil.Select(lambda info: info[0][0] == NET_SIZE, logData)
    rho = list(map(lambda info: info[0][0] / (math.pi * LocMath.Sqr(info[0][1])), logData))

    # extract data
    graphData = list(map(lambda info: [info[1][0], info[1][2]], data))
    nFlow,cap = LocUtil.UnZip(graphData)

    # graph data
    fig,ax = plot.subplots(figsize=(6.5, 6.5))
    plot.plot(nFlow,cap, 'ro',markersize=4)

    # plot median
    groupData = LocUtil.Group(lambda p: p[0], graphData)

    result = []
    for group in groupData:
        nStream,agFlow = LocUtil.UnZip(groupData)
        result.append([nStream[0], median(agFlow)])

    plot.plot(LocUtil.UnZip(result), 'b')

    # labels and title
    ax.set_xlabel("Num of Stream")
    ax.set_ylabel("Aggregate Capacity")
    ax.set_title(f'N = {NET_SIZE}; Rho = 2')

    # save figure
    plot.savefig('flow_graph.png', dpi=200)
    plot.show()