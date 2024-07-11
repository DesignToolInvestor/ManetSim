#
# 3 d _ p l o t . p y
#

from matplotlib import pyplot as plot
from math import pi, cos, sin
from numpy import linspace
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def WallSeg(p0,p1):
    x0,y0,z0 = p0
    x1,y1,z1 = p1
    result = [p0, p1, (x1,y1,0), (x0,y0,0)]

    return result


if __name__ == "__main__":
    nPoint = 25

    theta = linspace(0, pi, nPoint)
    xL = [cos(t - pi / 2) for t in theta]
    yL = [sin(t - pi / 2) for t in theta]
    zL = theta

    fig, ax = plot.subplots(subplot_kw=dict(projection='3d'))
    plot.plot(xL,yL,zL, color="darkblue")
    plot.plot(xL, yL, [0 for _ in range(nPoint)], color="darkblue")

    point = list(p for p in zip(xL,yL,zL))
    print(point)
    temp = WallSeg(point[0],point[1])

    for i in range(nPoint - 1):
        wallSeg = WallSeg(point[i],point[i+1])
        ax.add_collection(Poly3DCollection([wallSeg], color="lightblue", alpha=0.5))

    ax.set(xlabel='x', ylabel='y', zlabel='z')

    plot.show()