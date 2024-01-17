#
# d o m _ c o m p . p y
#

# This is a script for hand checking of the DomCompSubNet function which extracts the dominant
# component of the network and returns it as a new network.

import math
import matplotlib.pyplot as plot

import LocUtil
import NetPath
import MakeNet
import Visual

if __name__ == "__main__":
    # set constants
    N = 200
    RHO = 2
    R = math.sqrt(N / RHO / math.pi)

    SEED = None

    # generate network
    # TODO:  Extract this beginning part and share it with other scripts
    seed = LocUtil.SetSeed(SEED, 3)
    print(f'Seed = {seed}')

    net = MakeNet.RandNetCirc(N,R)
    node,link = net

    # plot network
    fig, ax = plot.subplots(figsize=(6.5, 6.5))
    ax = Visual.GraphBiNet(ax, net)
    fileName = f'base_{N}_{seed}.png'
    fig.savefig(fileName, dpi=200)

    # extract dominant component as a subnetwork
    subNet = NetPath.DomCompSubNet(net)

    # plot network
    fig, ax = plot.subplots(figsize=(6.5, 6.5))
    ax = Visual.GraphBiNet(ax, subNet)
    fileName = f'dom_comp_{N}_{seed}.png'
    fig.savefig(fileName, dpi=200)