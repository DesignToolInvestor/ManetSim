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
from CliqueSlow import Clique as CliqueSlow
from CliquePrune import Clique as CliquePrune
from Cost import LinkR, MetricCostF
from Interfere import InterDist, PathSelfInter
from LocMath import Add, Cent, Diff, Dist, Interp1, Scale, Perp
from LocUtil import SetEq, SetSeed, Sub, UnZip
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
    costF,metric = MetricCostF(args.metric, args.gamma, args.snirDb)

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


###############################################################
def PlotCirc(net, path, gamma,snir):
    nodeLoc,link = net
    nHops = len(path) - 1

    # plot just the node along the path
    pathLoc = Sub(nodeLoc, path)
    x, y = UnZip(pathLoc)
    plot.plot(x, y, 'o', color="darkblue", markersize=5, zorder=0)

    # plot source and sink markers
    x,y = nodeLoc[path[0]]
    plot.plot(x, y, 's', color="limegreen", markersize=10, zorder=-2)

    x,y = nodeLoc[path[nHops]]
    plot.plot(x, y, 'o', color="limegreen", markersize=10, zorder=-2)

    # plot links along the path
    x,y = UnZip(pathLoc)
    plot.plot(x, y, color="crimson", zorder=-1)

    # label links
    for i in range(nHops):
        x,y = Cent((pathLoc[i], pathLoc[i + 1]))
        plot.text(
            x,y, str(i), color="black", ha="center", va="center",
            bbox=dict(facecolor='white', edgecolor='none'), zorder=1)

    # do circles for exclusion zone
    reciverLoc = pathLoc[1:]
    hopDist = [Dist(pathLoc[k], pathLoc[k + 1]) for k in range(nHops)]

    excluR = [InterDist(dist, gamma, snir) for dist in hopDist]
    circL = [Circle(cent, r, nPointCirc) for (cent, r) in zip(reciverLoc, excluR)]

    for circ in circL:
        plot.plot(*UnZip(circ), 'g--')
        
    # do circle diameters
    for i in range(nHops):
        linkDir = Diff(*pathLoc[i: i+2])
        perpDir = Perp(linkDir)

        a = Add(reciverLoc[i], Scale(excluR[i], perpDir))
        b = Add(reciverLoc[i], Scale(-excluR[i], perpDir))

        plot.plot([a[0], b[0]], [a[1],b[1]], 'k:')


#######################################
if __name__ == "__main__":
    # constants
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
    netR = MakeNet.NetR(nNode, rho)
    net = RandNetCirc(nNode, netR)
    nodeLoc, linkL = net

    flow = sample([k for k in range(nNode)], k=2)

    # find best flow
    linkCost = [LinkR(nodeLoc[n0], nodeLoc[n1]) for (n0, n1) in linkL]
    path = BestPath(net, *flow, linkCost)

    if path is None:
        print (f'Seed = {seed}, path = None')
    else:
        nHops = len(path) - 1
        print(f'{nHops} hops')

        # start new plot
        fig, ax = plot.subplots(figsize=(6.5, 6.5))
        ax.set_aspect('equal')

        ####################################
        # plot path
        snir = 10 ** (snirDb / 20)
        PlotCirc(net, path, gamma,snir)

        # do annotation
        annotate = f'N = {nNode}\nnHops = {nHops}\nseed = {seed}'

        x = Interp1(*ax.get_xlim(), 0.05)
        y = Interp1(*ax.get_ylim(), 0.95)
        plot.text(x,y, annotate, ha='left', va='top', multialignment="left")

        ####################################
        # interference graph
        linkLink = PathSelfInter(net,path,gamma,snir)
        print(linkLink)

        # put interference graph on the plot
        n = len(linkLink)
        if n == 0:
            text = 'None'
        else:
            text = "".join(f'{linkLink[i]}\n' for i in range(n - 1)) + str(linkLink[n - 1])

        x = Interp1(*ax.get_xlim(), 0.05)
        y = Interp1(*ax.get_ylim(), 0.05)
        plot.text(x,y, text, ha='left', va='bottom', multialignment="left")

        ####################################
        # clique number
        cliqueSlow = cliqueSlow((nHops,linkLink))
        cliquePrune = cliquePrune((nHops, linkLink))

        assert(SetEq(cliqueSlow, cliquePrune))

        chromNum = max(map(len,cliquePrune))
        text = f'Num Clique = {len(cliquePrune)}\nChrom # = {chromNum}'

        x = Interp1(*ax.get_xlim(), 0.95)
        y = Interp1(*ax.get_ylim(), 0.95)
        plot.text(x, y, text, ha='right', va='top')

        # annotate
        plot.title(f'Intra Path Interference')

        # save figure
        assert(rho == 2.0)
        fileName = f'Interfere/rings_{nNode}_2_{seed}_{metric[0]}.png'
        plot.savefig(fileName, dpi=200)
        # plot.show()