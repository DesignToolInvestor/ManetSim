#
# t e s t _ B e s t P a t h . p y
#

# This script will generate a graph of the Dijkstra algorithm results for visual inspection.

import argparse
from math import isfinite
from matplotlib import pyplot as plot
from random import sample

from BestPath import BestPath
from Cost import MetricArg
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
    parser.add_argument('-flow', type=str)

    # parse args
    args = parser.parse_args()

    # deal with flow
    flow = eval(args.flow) if args.flow is not None else None

    # deal with metric
    costF,metric = MetricArg(args.metric, args.gamma, args.snirDb)

    # return results
    return [
        args.folder, costF, metric, args.n, args.rho, flow, args.seed, args.gamma, args.snirDb
    ]


#################################################################################
if __name__ == "__main__":
    # parse arguments
    folder,costF,metric,nNode,rho,flow,seed,_,_ = ParseArgs()

    # constants
    numSeedDig = 2

    # make network
    seed = SetSeed(seed, numSeedDig)
    print(f'Seed: {seed}')

    r = MakeNet.R(nNode,rho)
    net = RandNetCirc(nNode, r)
    nodeLoc,linkL = net

    # build ground truth
    linkCost = [costF(*Sub(nodeLoc, link)) for link in linkL]

    if flow is None:
        flow = sample(range(len(nodeLoc)), k=2)

    path = BestPath(net, *flow, linkCost)
    nHop = len(path)

    # print graph
    fig,ax = plot.subplots(figsize=(6.5,6.5))

    # costLab = [round(c,1) for c in cost]
    # linkCostLab = [round(c,1) for c in linkCost]
    # GraphBiNet(ax, net, True, True, nodeNum=costLab, linkNum=linkCostLab)
    GraphBiNet(ax, net, True, True, nodeNum=[k for k in range(nNode)])

    # show backtrack
    for hopNum in range(nHop - 1):
        n0 = path[hopNum]
        n1 = path[hopNum + 1]
        line = (nodeLoc[n0], nodeLoc[n1])
        plot.plot(*UnZip(line), color="yellow", linewidth=3, zorder=-1)

    # add annotation
    plot.title(f'Best Path ({metric[1]})')

    x = min(loc[0] for loc in nodeLoc)
    y = max(loc[1] for loc in nodeLoc)
    plot.text(
        x,y, f'N = {nNode}\nRho = {rho}\nSeed = {seed}\nnHop = {nHop}\n{metric[1]}',
        fontsize=8, va="top", ha="left", multialignment="left")

    # save figure
    fileName = f'{folder}/dijkstra_{metric[0]}_{nNode}_{seed}'
    plot.savefig(fileName, dpi=200)
    # plot.show()
