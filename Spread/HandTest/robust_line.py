#
# r o b u s t _ l i n e . p y
#

from matplotlib import pyplot as plot
from math import atan, tan, pi
from random import random

from LocUtil import Grid1, Partition, SetSeed
from LocMath import RobustLine

def CauchyRand():
    cdf = random()
    return -1 / tan(pi * cdf)


if __name__ == '__main__':
    # constants
    numPoint = 100
    seed = None
    seedDigits = 3
    dotSize = 4

    # make points
    seed = SetSeed(seed, digits=seedDigits)
    print(f'Seed = {seed}')

    xL = [2*random() - 1 for _ in range(numPoint)]
    yL = [x + CauchyRand()/4 for x in xL]

    # debugging figure
    fig,ax = plot.subplots()

    plot.plot(xL,yL, 'ro', markersize=dotSize)

    # fit
    (slope,inter),(centX,centY) = RobustLine(xL, yL)

    xFit = Grid1(-1,1, numPoint)
    yFit = [slope*x + inter for x in xFit]
    plot.plot(xFit,yFit, 'b', linewidth=2)

    # plot center
    plot.plot(centX,centY, 'b*', markersize=12)

    # add title
    ang = atan(slope) * 180/pi
    plot.title(f'N={numPoint}, Ang={ang:.1f} (err = {ang-45:.2f}), Seed = {seed}')

    # save figure
    plot.show()
    plot.savefig(f'RobustLine/{numPoint}_{seed}.png')