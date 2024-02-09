#
# t e s t _ D i j k s t r a . p y
#

# This script will generate a graph of the Dijkstra algorithm results for visual inspection.

import argparse
from math import isfinite
from matplotlib import pyplot as plot
import random

import Cost
from Dijkstra import DijkstraBack, DijkstraFor
from LocUtil import SetSeed, Sub, UnZip
from MakeNet import RandNetCirc
import MakeNet
from Visual import GraphBiNet


#######################################
def ParseArgs():
    parser = argparse.ArgumentParser(
            prog="plot_sssf",
            description='This script will plot the achievable capacity for SSSFs'
    )

    parser.add_argument('folder', type=str)
    parser.add_argument('metric', type=str)

    parser.add_argument('-n', type=int, default=50)
    parser.add_argument('-rho', type=float, default=2.0)
    parser.add_argument('-seed', type=int)
    parser.add_argument('-gamma', type=float, default=2.0)
    parser.add_argument('-snirDb', type=float, default=0)
    parser.add_argument('-source', type=int)

    # parse args
    args = parser.parse_args()

    # deal with metric
    if args.metric == "hc":
            metric = ("hc", "hop count")
            costF = lambda p0,p1: 1
    elif args.metric == "sp":
            metric = ("sp", "shortest path")
            costF = Cost.R
    elif args.metric == "xr":
            metric = ("xr", "exclusion range")
            snir = 10 ** (args.snirDb / 20)
            costF = lambda p0,p1: Cost.ExcluR(p0,p1, args.gamma, snir)
    elif args.metric == "xa":
            metric = ("xa", "exclusion area")
            snir = 10 ** (args.snirDb / 20)
            costF = lambda p0,p1: Cost.ExcluArea(p0,p1, args.gamma, snir)
    else:
            raise Exception("Must specify metric.  Either 'hc'. sp', 'xr', or 'xa'")

    # deal with flow
    source = eval(args.source) if args.source is not None else None

    # return results
    return [
        args.folder, costF, metric, args.n, args.rho, args.seed, args.gamma, args.snirDb, source
    ]


#################################################################################
if __name__ == "__main__":
    # parse arguments
    folder,costF,metric,nNode,rho,seed,_,_,source = ParseArgs()

    # constants
    numSeedDig = 2

    # make network
    seed = SetSeed(seed, numSeedDig)
    print(f'Seed: {seed}')

    # TODO: change RandNetCirc to RandCircNet and to take n & r ... do everywhere at once
    r = MakeNet.R(nNode,rho)
    net = RandNetCirc(nNode, r)
    nodeLoc,linkL = net

    # build ground truth
    linkCost = [costF(*Sub(nodeLoc, link)) for link in linkL]

    if source is None:
        source = random.randint(0, len(nodeLoc) - 1)

    cost,back = DijkstraFor(net, source, linkCost)

    # print graph
    fig,ax = plot.subplots(figsize=(6.5,6.5))

    costLab = [round(c,1) for c in cost]
    linkCostLab = [round(c,1) for c in linkCost]
    # GraphBiNet(ax, net, True, True, nodeNum=costLab, linkNum=linkCostLab)
    GraphBiNet(ax, net, True, True, nodeNum=[k for k in range(nNode)], linkNum=linkCostLab)

    # show backtrack
    for nodeId in range(nNode):
        if isfinite(cost[nodeId]) and (0 <= back[nodeId]):
            line = (nodeLoc[nodeId], nodeLoc[back[nodeId]])
            plot.plot(*UnZip(line), color="yellow", linewidth=5, zorder=-1)

    # add annotation
    plot.title(f'N = {nNode}; Rho = {rho}; Seed = {seed}; {metric[1]}')

    # save figure
    fileName = f'{folder}/dijkstra_{metric[0]}_{nNode}_{seed}'
    plot.savefig(fileName, dpi=200)
    # plot.show()
