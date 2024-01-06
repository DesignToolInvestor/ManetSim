#
# GenRand.py
#
# TODO:  Change the name of this file to be more meaningful.
#
# This program generates a random planer network of uniform density over a circular area.
#
# Call this as
#   main <file_name> -n=<n> -r=<max_radius> -rho=<density>

# system libraries
import argparse
import math
import random

# local libraries
import LocMath
import Net

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


# Links will be in order sorted by x-index and then y-index
def FindLinks(nodeLoc):
    n = len(nodeLoc)

    link = []
    for k in range(n):
        for j in range(k+1,n):
            if localmath.Dist(nodeLoc[k],nodeLoc[j]) < 1:
                link.append([k,j])

    return link


def ParseArgs():
    parser = argparse.ArgumentParser(
        prog='RandNetCirc',
        description='This program will generate a random network over a circular area.'
    )

    parser.add_argument('fileName', type=str)
    parser.add_argument('-n', type=int)
    parser.add_argument('-r', type=float)
    parser.add_argument('-rho', type=float)

    args = parser.parse_args()

    if (args.n != None) and (args.r != None) and (args.rho != None):
        raise Exception("Over specification of parameters")

    if (args.n != None) and (args.r != None):
        n = args.n
        r = args.r
        rho = math.pi * Sqr(r) / n

    elif (args.n != None) and (args.rho != None):
        n = args.n
        rho = args.rho

        area = n / rho
        r = math.sqrt(area / math.pi)

    elif (args.r != None) and (args.rho != None):
        r = args.r
        rho = args.rho

        area = math.pi * Sqr(r)
        n = math.round(area * rho)

        area = n / rho
        r = math.sqrt(area / math.pi)

    return [args.fileName, n, r, rho]
    
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fileName, n, r, rho = ParseArgs()
    print('n = %d, r = %f, rho = %f\n' % (n, r, rho))

    random.seed(0)
    nodeLoc = RandNodeCirc(n, r)
    link = FindLinks(nodeLoc)

    net = (nodeLoc,link)
    Net.WriteNet(net, fileName)

# TODO:  Figure out how to make this work
if __name__ == '__test__':
    print("This is the test script !!!")