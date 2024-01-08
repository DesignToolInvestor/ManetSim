#
# V i s u a l . p y
#
# This is a file of visualization functions.  It is intended as s sort of local library.
#

# system imports
import math
import matplotlib.pyplot as plot

# local imports
import LocMath
import LocUtil


def GraphBiNet(net):
    # pattern match on net
    nodes, links = net

    # setup plot
    fig, ax = plot.subplots()
    # TODO: setting the size doesn't seem to be working
    plot.figure(figsize = (9, 6.5))
    ax.set_aspect('equal')

    # plot links
    x = []
    y = []
    for link in links:
        x = [nodes[link[0]][0], nodes[link[1]][0]]
        y = [nodes[link[0]][1], nodes[link[1]][1]]
        ax.plot(x,y, color='blue')

    # plot nodes
    # TODO: Create an unzip function
    x = []
    y = []
    for node in nodes:
        x.append(node[0])
        y.append(node[1])

    ax.scatter(x,y, color='red')

    # show graph
    plot.show()


###############################################################################
# Directed networks
def CircPoint(circDef, ang):
    rad,(xCent,yCent) = circDef
    xCent + rad * math.cos(ang)
    yCent + rad * math.sin(ang)

    return [xCent,yCent]
    
    
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
    cord = (xStop - xStart, yStop - yStart)
    cordLen = LocMath.Len(cord)
    cordAng = math.atan2(cord[1], cord[0])

    # compute arc
    maxArcOffSet = cordLen * (1 - math.cos(maxArc/2)) / (2*math.sin(maxArc/2))
    if (maxArcOffSet > maxOffSet):
        yArg = 4*cordLen*maxOffSet / (LocMath.Sqr(cordLen) + 4*LocMath.Sqr(maxOffSet))
        xArg = (LocMath.Sqr(cordLen) - 4*LocMath.Sqr(maxOffSet)) / (LocMath.Sqr(cordLen) + 4*LocMath.Sqr(maxOffSet))
        arc = 2 * math.atan2(yArg,xArg)
    else:
        arc = maxArc

    # compute R
    rad = cordLen / math.sqrt(2*(1 - math.cos(arc)))

    # compute center
    startAngToCent = cordAng + (math.pi - arc)/2
    xCent = xStart + rad * math.cos(startAngToCent)
    yCent = yStart + rad * math.sin(startAngToCent)

    # compute ard
    angStart = math.atan2(yStart - yCent, xStart - xCent)
    angStop = math.atan2(yStop - yCent, xStop - xCent)
    thetas = LocUtil.Grid1(angStart,angStop, NUM_POINT)

    x = list(map(lambda t: CircPoint(rad,(xCent,yCent)), thetas))
    y = list(map(lambda t: CircPoint(rad,(xCent,yCent)), thetas))

    return ((x,y), (rad, (xCent,yCent), (angStart, angStop)))


def ArcArrow(arcDef, pathFrac, headWidth):
    ARROR_ANG = math.pi/3
    
    rad,cent,(angStart, angStop) = arcDef
    point,ang = ArcPoint(arcDef, pathFrac)

    dir = ang + math.pi/2
    headAngOut = dir + ARROR_ANG/2
    headAngIn = dir - ARROR_ANG/2

    headLen = headWidth / math.tan(ARROR_ANG/2)
    tailOut = point + headLen * [math.cos(headAngOut),math.sin(headAngOut)]
    tailIn = point + headLen * [math.cos(headAngIn),math.sin(headAngIn)]
    
    return [[point,tailOut], [point,tailIn]]
    
    
def GraphDirNet(dirNet):
    # pattern match on dirNet
    nodes,links = dirNet

    # setup plot
    fig,ax = plot.subplots()
    # TODO: setting the size doesn't seem to be working
    plot.figure(figsize = (9, 6.5))
    ax.set_aspect('equal')

    # plot links
    for linkNum in range(nLinks):
        link = links[linkNum]
        (x,y),arcDef= Arc(nodes[link[0]],nodes[link[1]])
        ax.plot(x,y, color='blue')

        (x,y) = ArcArrow(arcDef, 0.6, 0.1)
        ax.plot(x,y, color='blue')
        
        (x,y) = ArcLoc(arcDef, 0.4)
        ax.text(x,y, str(linkNum), backgroundcolor="w")

    # Plot nodes.  Want point on top of lines, so they come after line.
    # TODO: Change to create points and then unzip them for plotting
    x = []
    y = []
    for node in nodes:
        x.append(node[0])
        y.append(node[1])

    ax.scatter(x,y, color='red')
    
    # show graph
    plot.show()