#
# v i s u a l i z e . p y
#
# This file creat a graph of a network.
#
# Call as
#   visualize <file_name>

import Net
import sys
import matplotlib.pyplot as plot

def GraphNet(net):
    # pattern match on net
    nodeL, linkL = net

    # setup plot
    fig, ax = plot.subplots()
    # TODO: setting the size doesn't seem to be working
    plot.figure(figsize = (9, 6.5))
    ax.set_aspect('equal')

    # plot links
    x = []
    y = []
    for link in linkL:
        x = [nodeL[link[0]][0], nodeL[link[1]][0]]
        y = [nodeL[link[0]][1], nodeL[link[1]][1]]
        ax.plot(x,y, color='blue')

    # plot nodes
    # TODO: Create an unzip function
    x = []
    y = []
    for node in nodeL:
        x.append(node[0])
        y.append(node[1])

    ax.scatter(x,y, color='red')

    # show graph
    plot.show()


if __name__ == '__main__':
    print(sys.argv)
    fileName = sys.argv[1]

    net = Net.ReadNet(fileName)
    GraphNet(net)
