#
# g r a p h _ i n t r a _ i n t e r f e r e . p y
#

# This script graphs the interference rings

# system packages
import argparse
import matplotlib.pyplot as plot
from math import sqrt, cos, sin, pi
from random import sample

# local libraries
from BestPath import BestPath
import Cost
from Cost import ExcluR, MetricArg
from LocMath import Cent, Dist
from LocUtil import SetSeed, Sub, UnZip
import MakeNet
from MakeNet import RandNetCirc


###############################################################
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

    # deal with metric
    costF,metric = MetricArg(args.metric, args.gamma, args.snirDb)

    # deal with flow
    flow = eval(args.flow) if args.flow is not None else None

    # return results
    return [
        args.folder, costF, metric, args.n, args.rho, flow, args.seed, args.gamma, args.snirDb
    ]


###############################################################
def Circle(cent, r, nPoint):
    x,y = cent
    theta = [k * 2*pi/nPoint for k in range(nPoint)]
    theta.append(0)
    point = [(x + r*cos(t), y + r*sin(t)) for t in theta]

    return point


#######################################
if __name__ == "__main__":
    # constants
    seed = None
    numSeedDig = 2

    snirDb = 0
    gamma = 2

    nPointCirc = 30

    # parse args
    folder,costF,metric,nNode,rho,flow,seed,_,_ = ParseArgs()

    # set seed
    seed = SetSeed(seed, digits=numSeedDig)
    print(f'seed = {seed}')

    # make net
    rad = MakeNet.R(nNode, rho)
    net = RandNetCirc(nNode, rad)
    nodeLoc, linkL = net

    flow = sample([k for k in range(nNode)], k=2)

    # find best flow
    linkCost = [Cost.R(nodeLoc[n0], nodeLoc[n1]) for (n0, n1) in linkL]
    path = BestPath(net, *flow, linkCost)
    nHops = len(path) - 1 if path is not None else None
    print(f'{nHops} hops')

    # start new graph
    fig, ax = plot.subplots(figsize=(6.5, 6.5))
    ax.set_aspect('equal')

    # plot just the node along the path
    pathLoc = Sub(nodeLoc, path)
    x, y = UnZip(pathLoc)
    plot.plot(x, y, 'o', color="darkblue", markersize=5, zorder=0)

    # plot source and sink markers
    x,y = nodeLoc[flow[0]]
    plot.plot(x, y, 's', color="limegreen", markersize=10, zorder=-2)

    x,y = nodeLoc[flow[1]]
    plot.plot(x, y, 'o', color="limegreen", markersize=10, zorder=-2)

    # plot links along the path
    x,y = UnZip(pathLoc)
    plot.plot(x, y, color="crimson", zorder=-1)

    # do circles for exclusion zone
    destLoc = pathLoc[1:]
    snir = 10 ** (snirDb / 20)

    excluR = [ExcluR(pathLoc[k], pathLoc[k+1], gamma, snir) for k in range(nHops)]
    print(f'exR = {excluR}')
    circL = [Circle(cent, r, nPointCirc) for (cent, r) in zip(destLoc, excluR)]

    for circ in circL:
        plot.plot(*UnZip(circ), 'g--')

    # annotate
    plot.title(f'Intra Path Interference')

    x = ax.get_xlim()
    y = ax.get_ylim()
    annotate = f'N = {nNode}\nnHops = {nHops}\nseed = {seed}'
    plot.text(x[0],y[1], annotate, ha='left', va='top', fontsize=10, multialignment="left")

    # save figure
    assert(rho == 2.0)
    fileName = f'Interfere/rings_{nNode}_2_{seed}_{metric[0]}.png'
    plot.savefig(fileName, dpi=200)

    plot.show()