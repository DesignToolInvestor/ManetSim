#
# visualize.py
#
# This file creat a graph of a network.
#
# Call as
#   visualize <file_name>

import scanf
import sys
import matplotlib.pyplot as plot
import numpy as np

def ReadNet(fileName):
    file = open(fileName, 'r')

    line = file.readline()
    nNode = scanf.scanf("%d", line)[0]

    nodeL = []
    for nodeNum in range(nNode):
        line = file.readline()
        node = scanf.scanf("%f, %f", line)
        nodeL.append(node)

    line = file.readline()
    nLink = scanf.scanf("%d", line)[0]

    linkL = []
    for linkNum in range(nLink):
        line = file.readline()
        link = scanf.scanf("%d, %d", line)
        linkL.append(link)

    file.close()

    return (nodeL, linkL)


def GraphNet(net):
    # TODO:
    nodeL, linkL = net

    # plot nodes
    # TODO: Create an unzip function
    x = []
    y = []
    for node in nodeL:
        x.append(node[0])
        y.append(node[1])

    fig, ax = plot.subplots()
    ax.scatter(x,y, color='red')

    # plot links
    x = []
    y = []
    for link in linkL:
        line = (nodeL[link[0]], nodeL[link[1]])
        linkLine.append(line)

    ax.plot(x,y, color='blue')

    plot.show()


if __name__ == '__main__':
    print(sys.argv)
    fileName = sys.argv[1]

    net = ReadNet(fileName)
    GraphNet(net)
