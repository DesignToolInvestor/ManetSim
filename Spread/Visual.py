#
# V i s u a l . p y
#
# This is a file of visualization functions.  It is intended as s sort of local library.
#

# system imports
import enum
from math import atan2, cos, sin, pi, sqrt, tan
import matplotlib.pyplot as plot

# local imports
from LocMath import Ang, MaxGapAng, Sqr
from LocUtil import Grid1, Index, UnZip
import MakeNet
from Net import Net2Fan

enum.Enum('NetElm', ['NODE','LINK','ALL'])


def GraphBiNet(ax, net, showNode=True, showLink=True, nodeNum=None, netRad=None):
    # parse arguments
    nodeLoc, linkL = net
    nNode = len(nodeLoc)

    if netRad is None:
        netRad = MakeNet.R(nNode,2)

    # axis properties
    ax.set_aspect('equal')

    # plot nodeL
    if showNode:
        x,y = UnZip(nodeLoc)
        ax.scatter(x,y, color='red', s=4)

    # label the nodes
    # TODO:  scale this by the density
    r = 0.05 * netRad
    if nodeNum is not None:
        neighborTab = Net2Fan(net)
        angTab = [[Ang(*Index(nodeLoc,[k,n])) for n in neighborTab[k]] for k in range(nNode)]
        textAng = [MaxGapAng(angTab[k]) for k in range(nNode)]

        for nodeId in range(nNode):
            nodeX,nodeY = nodeLoc[nodeId]
            plot.text(
                nodeX + cos(textAng[nodeId])*r, nodeY + sin(textAng[nodeId])*r,
                str(nodeNum[nodeId]), color="red", ha="center", va="center")

    # plot link
    if showLink:
        # TODO:  Figure out how to do this with improved versions of UnZip and Index
        x = []
        y = []
        for link in linkL:
            x = [nodeLoc[link[0]][0], nodeLoc[link[1]][0]]
            y = [nodeLoc[link[0]][1], nodeLoc[link[1]][1]]
            ax.plot(x,y, color='blue', linewidth=0.3)


###############################################################################
# Directed networks

#######################################
# Arcs
# Might be vestigial, but don't delete yet, hard to create and might need later
def CircPoint(circDef, ang):
    rad,(xCent,yCent) = circDef

    x = xCent + rad * cos(ang)
    y = yCent + rad * sin(ang)

    return [x,y]
    
    
def ArcPoint(arcDef, pathFrac):
    rad,cent,(angStart,angStop) = arcDef
    
    angRange = (angStop - angStart)
    ang = angStart + pathFrac*angRange
    
    return CircPoint((rad,cent), ang), ang


# TODO:  Fix so that it handles wrapping correctly
def Arc(start,stop, maxOffSet,maxArc):
    NUM_POINT = 30;

    xStart,yStart = start
    xStop,yStop = stop
    cord = [xStop - xStart, yStop - yStart]
    cordLen = Len(cord)
    cordAng = atan2(cord[1], cord[0])

    # compute arc
    maxArcOffSet = cordLen * (1 - cos(maxArc/2)) / (2*sin(maxArc/2))
    if (maxArcOffSet > maxOffSet):
        yArg = 4*cordLen*maxOffSet / (Sqr(cordLen) + 4*Sqr(maxOffSet))
        xArg = (Sqr(cordLen) - 4*Sqr(maxOffSet)) / (Sqr(cordLen) + 4*Sqr(maxOffSet))
        arcAng = 2 * atan2(yArg,xArg)
    else:
        arcAng = maxArc

    # compute R
    rad = cordLen / sqrt(2*(1 - cos(arcAng)))

    # compute center
    startAngToCent = cordAng + (pi - arcAng)/2
    xCent = xStart + rad * cos(startAngToCent)
    yCent = yStart + rad * sin(startAngToCent)

    # compute ard
    angStart = atan2(yStart - yCent, xStart - xCent)
    angStop = angStart + arcAng
    angs = Grid1(angStart,angStop, NUM_POINT)

    points = list(map(lambda ang: CircPoint((rad,(xCent,yCent)), ang), angs))
    x,y = UnZip(points)

    return ((x,y), (rad, (xCent,yCent), (angStart, angStop)))


def ArcArrow(arcDef, pathFrac, headWidth):
    ARROR_ANG = pi/3
    
    point,ang = ArcPoint(arcDef, pathFrac)

    dir = ang + pi/2
    headAngOut = dir - pi + ARROR_ANG/2
    headAngIn = dir - pi - ARROR_ANG/2

    headLen = headWidth / tan(ARROR_ANG/2)
    outVec = [headLen * cos(headAngOut), headLen * sin(headAngOut)]
    tailOut = [point[0] + outVec[0], point[1] + outVec[1]]
    inVec = [headLen * cos(headAngIn), headLen * sin(headAngIn)]
    tailIn = [point[0] + inVec[0], point[1] + inVec[1]]
    
    return [[point,tailOut], [point,tailIn]]
    

#######################################
# vistigual GraphDirNet section
#     for linkNum in range(nLink):
#         link = linkL[linkNum]
#
#         (x,y),arcDef = Arc(nodeL[link[0]],nodeL[link[1]], MAX_OFF_SET,MAX_ARC)
#         ax.plot(x,y, color='blue')
#
#         lines = ArcArrow(arcDef, 2/3, 0.05)
#         x = [[lines[0][0][0], lines[1][0][0]], [lines[0][1][0], lines[1][1][0]]]
#         y = [[lines[0][0][1], lines[1][0][1]], [lines[0][1][1], lines[1][1][1]]]
#         ax.plot(x,y, color='blue')
#
#         (x,y),ang = ArcPoint(arcDef, 1/3)
#         ax.text(x,y, str(linkNum), va="center", ha="center")

# TODO:  Change the interface to pass in and out the axis
# TODO:  Combine with GraphBiNet
def GraphDirNet(dirNet):
    MAX_OFF_SET = 0.05
    MAX_ARC = pi/3

    # pattern match on dirNet
    nodeL,linkL = dirNet
    nLink = len(linkL)

    # setup plot
    fig,ax = plot.subplots()
    ax.set_aspect('equal')

    # plot linkL
    for linkNum in range(nLink):
        link = linkL[linkNum]
        
        seg = [nodeL[link[0]], nodeL[link[1]]]
        x = [seg[0][0], seg[1][0]]
        y = [seg[0][1], seg[1][1]]
        ax.plot(x,y, color='blue', linewidth=0.2)
        
        point = Interp(seg, 2/3)
        ax.text(point[0],point[1], str(linkNum), color="blue", ha="center", va="center")

    # Plot nodeL.  Want point on top of lines, so they come after line.
    # TODO: Change to create points and then unzip them for plotting
    x = []
    y = []
    for node in nodeL:
        x.append(node[0])
        y.append(node[1])

    ax.scatter(x,y, color='red')
    
    # show graph
    plot.show()