#
# p l o t _ s s s f . p y
#

import argparse
from matplotlib import pyplot as plot
from statistics import median

from LocUtil import UnZip


#######################################
def ParseArgs():
    parser = argparse.ArgumentParser(
        prog="plot_sssf",
        description='This script will plot the achievable capacity for SSSFs'
    )

    parser.add_argument('fileName', type=str)
    parser.add_argument('metric', type=str)

    # parse args
    args = parser.parse_args()

    # deal with metric
    if args.metric == "sp":
        metric = ("sp", "shortest path")
    elif args.metric == "xr":
        metric = ("xr", "exclusion range")
    elif args.metric == "xa":
        metric = ("xa", "exclusion area")
    else:
        raise Exception("Must specify metric.  Either 'sp', 'xr', or 'xa'")

    # return results
    return [args.fileName, metric]


##################################################################
def HopFig(nHop,cap, rho,midDist,metric):
    # do graph
    fig, ax = plot.subplots(figsize=(9, 6.5))

    plot.plot(nHop, cap, 'o', markersize=5, color="maroon")

    # annotation
    plot.xlabel('Num. of Hops')
    plot.ylabel('Archived Capacity')
    plot.title(f'Single Strand Single Flow ({metric[1]})')

    plot.text(
        0, 0.95 * max(cap), f'N = {nNode}\nRho = {rho}\nMed. Dist. = {midDist:.2f}',
        va="top", ha="left", multialignment="left")

    # save figure
    plot.savefig(f"300_2_{metric[0]}_hop.png")
    plot.show()

    plot.close(fig)


def DistFig(dist,cap, rho,midDist,metricStr):
    # do graph
    fig, ax = plot.subplots(figsize=(9, 6.5))

    plot.plot(dist, cap, 'o', markersize=5, color="maroon")

    # annotation
    plot.xlabel('Dist.')
    plot.ylabel('Archived Capacity')
    plot.title(f'Single Strand Single Flow ({metric[1]})')

    plot.text(
        0, 0.95 * max(cap), f'N = {nNode}\nRho = {rho}\nMed. Dist. = {midDist:.2f}',
        va="top", ha="left", multialignment="left")

    # save figure
    plot.savefig(f"300_2_{metric[0]}_dist.png")
    plot.show()

    plot.close(fig)


##################################################################
if __name__ == "__main__":
    # constants
    fileName,metric = ParseArgs()

    # read log
    with open(fileName, "r") as file:
        link = file.readlines()

    # pattern match data
    temp = [eval(l) for l in link]
    infoL = [info for info in temp if info[2] is not None]

    netInfo,capInfo,result = UnZip(infoL)
    nHop,_,dist = UnZip(capInfo)
    chromNum,_,_ = UnZip(result)

    nNode,rho,_ = netInfo[0]

    # compute cap
    cap = [d/c for (d,c) in zip(dist, chromNum)]

    # do graphs
    HopFig(nHop,cap, rho,median(dist),metric)
    DistFig(dist,cap, rho,median(dist),metric)