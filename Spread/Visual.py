#
# V i s u a l . p y
#
# This is a file of visualization functions.  It is intended as s sort of local library.
#
import enum
# system imports
import math
import matplotlib.pyplot as plot

# local imports
import LocMath
import LocUtil

enum.Enum('NetElm', ['NODE','LINK','ALL'])

def GraphBiNet(ax, net, showNode=True, showLink=True):
    # pattern match on net
    nodeL, linkL = net

    # axis properties
    ax.set_aspect('equal')

    # plot nodeL
    if showNode:
        x,y = LocUtil.UnZip(nodeL)
        ax.scatter(x,y, color='red', s=4)

    # plot link
    if showLink:
        # TODO:  Figure out how to do this with improved versions of UnZip and Index
        x = []
        y = []
        for link in linkL:
            x = [nodeL[link[0]][0], nodeL[link[1]][0]]
            y = [nodeL[link[0]][1], nodeL[link[1]][1]]
            ax.plot(x,y, color='blue', linewidth=0.3)

    return ax


###############################################################################
# Directed networks

#######################################
# Arcs
# Might be vestigial, but don't delete yet, hard to create and might need later
def CircPoint(circDef, ang):
    rad,(xCent,yCent) = circDef

    x = xCent + rad * math.cos(ang)
    y = yCent + rad * math.sin(ang)

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
    cordLen = LocMath.Len(cord)
    cordAng = math.atan2(cord[1], cord[0])

    # compute arc
    maxArcOffSet = cordLen * (1 - math.cos(maxArc/2)) / (2*math.sin(maxArc/2))
    if (maxArcOffSet > maxOffSet):
        yArg = 4*cordLen*maxOffSet / (LocMath.Sqr(cordLen) + 4*LocMath.Sqr(maxOffSet))
        xArg = (LocMath.Sqr(cordLen) - 4*LocMath.Sqr(maxOffSet)) / (LocMath.Sqr(cordLen) + 4*LocMath.Sqr(maxOffSet))
        arcAng = 2 * math.atan2(yArg,xArg)
    else:
        arcAng = maxArc

    # compute R
    rad = cordLen / math.sqrt(2*(1 - math.cos(arcAng)))

    # compute center
    startAngToCent = cordAng + (math.pi - arcAng)/2
    xCent = xStart + rad * math.cos(startAngToCent)
    yCent = yStart + rad * math.sin(startAngToCent)

    # compute ard
    angStart = math.atan2(yStart - yCent, xStart - xCent)
    angStop = angStart + arcAng
    angs = LocUtil.Grid1(angStart,angStop, NUM_POINT)

    points = list(map(lambda ang: CircPoint((rad,(xCent,yCent)), ang), angs))
    x,y = LocUtil.UnZip(points)

    return ((x,y), (rad, (xCent,yCent), (angStart, angStop)))


def ArcArrow(arcDef, pathFrac, headWidth):
    ARROR_ANG = math.pi/3
    
    point,ang = ArcPoint(arcDef, pathFrac)

    dir = ang + math.pi/2
    headAngOut = dir - math.pi + ARROR_ANG/2
    headAngIn = dir - math.pi - ARROR_ANG/2

    headLen = headWidth / math.tan(ARROR_ANG/2)
    outVec = [headLen * math.cos(headAngOut), headLen * math.sin(headAngOut)]
    tailOut = [point[0] + outVec[0], point[1] + outVec[1]]
    inVec = [headLen * math.cos(headAngIn), headLen * math.sin(headAngIn)]
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
    MAX_ARC = math.pi/3

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
        
        point = LocMath.Interp(seg, 2/3)
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