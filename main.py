#
# main.py
#
# TODO:  Change the name of this file to be more meaningful.
#
# This program generates a random planer network of uniform density over a circular area.
#
# Call this as
#   main <num_node> <max_range> <file_name>

import math
import random
import sys

def RandNodeCirc(n, maxRad) -> list[[float,float]]:
    result = []
    for i in range(n):
        angle = random.random() * 2 * math.pi
        radQ = random.random()
        rad = math.sqrt(radQ * maxRad*maxRad)
        x = rad * math.cos(angle)
        y = rad * math.sin(angle)
        result.append([x,y])
    return result


def PrintList(nodeLoc):
    for point in nodeLoc:
        print(point[0], ", ", point[1])


def Dist(node1,node2):
    return math.sqrt(node1[1]*node1[1] + node2[1]*node2[1])


# Links will be in order sorted by x-index and then y-index
def FindLinks(nodeLoc):
    n = len(nodeLoc)

    link = []
    for k in range(n):
        for j in range(k+1,n):
            if Dist(nodeLoc[k],nodeLoc[j]) < 1:
                link.append([k,j])

    return link

def SaveNet(nodeLoc, links, filename):
    with open(filename, 'w') as file:
        nNode = len(nodeLoc)
        file.write(str(nNode) + '\n')

        for point in nodeLoc:
            file.write(str(point[0]) + ", " + str(point[1]) + "\n")

        nLink = len(links)
        file.write(str(nLink) + '\n')

        for link in links:
            file.write(str(link[0]) + ", " + str(link[1]) + "\n")

        file.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("This is main.")

    # TODO:  Switch to using the argparse module (or is that package)
    n = int(sys.argv[1])
    maxRad = float(sys.argv[2])
    fileName = sys.argv[3]

    random.seed(0)
    nodeLoc = RandNodeCirc(n, maxRad)
    link = FindLinks(nodeLoc)

    SaveNet(nodeLoc, link, fileName)

# TODO:  Figure out how to make this work
if __name__ == '__test__':
    print("This is the test script !!!")