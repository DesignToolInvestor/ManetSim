#
# n e t . p y
#
# This file (or module) is intended for reading and writing network descriptions.
#
# The network file consists of the following logical elements:
#   <num_node> <node_locations> <num_link> <links>
#
# where:
#   <num_node> is a non-negative integer indicating the number of nodes
#   <node_locations> is an ordered list of the node locations
#   <num_link> is a non-negative integer indicating the number of links
#   <links> is a list of the links
#
# The information encoding is:
#   * The node list is ordered from 0 to num_node - 1.
#   * The node locations are represented by floating point coordinates in the form x,y (spaces are ignored).
#   * The links are represented by a pair of nodes n0,n1 (spaces are ignored), where n0 and n1 are indices into the list
#     of nodes.

# TODO:  Move inside some larger library, perhaps called ParkerLevy

def ReadNet(fileName):
    # open file
    file = open(fileName, 'r')

    # read number of nodes
    line = file.readline()
    nNode = scanf.scanf("%d", line)[0]

    # read nodes
    nodeL = []
    for nodeNum in range(nNode):
        line = file.readline()
        node = scanf.scanf("%f, %f", line)
        nodeL.append(node)

    # read number of links
    line = file.readline()
    nLink = scanf.scanf("%d", line)[0]

    # read links
    linkL = []
    for linkNum in range(nLink):
        line = file.readline()
        link = scanf.scanf("%d, %d", line)
        linkL.append(link)

    file.close()

    return (nodeL, linkL)


def WriteNet(net, fileName):
    # parse arguments
    nodeLoc,links = net
    nNode = len(nodeLoc)
    nLink = len(links)

    # open file
    file = open(fileName, 'w')

    # write nodes
    file.write(str(nNode) + '\n')
    for point in nodeLoc:
        file.write(str(point[0]) + ", " + str(point[1]) + "\n")

    # write links
    file.write(str(nLink) + '\n')
    for link in links:
        file.write(str(link[0]) + ", " + str(link[1]) + "\n")

    # close file
    file.close()

# TODO:  Add flag for distinguishing between directional and non-directional networks