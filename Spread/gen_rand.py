#
# gen_rand.py
#
# TODO:  Change the name of this file to be more meaningful.
#
# This program generates a random planer network of uniform density over a circular area.
#
# Call this as
#   main <file_name> -n=<n> -r=<max_radius> -rho=<density> -seed=<seed>

# system libraries
import argparse
import math
import random

# local libraries
import LocMath
#import LocUtil
import Net


def ParseArgs():
    parser = argparse.ArgumentParser(
        prog='RandNetCirc',
        description='This program will generate a random network over a circular area.'
    )

    parser.add_argument('fileName', type=str)
    parser.add_argument('-n', type=int)
    parser.add_argument('-r', type=float)
    parser.add_argument('-rho', type=float)
    parser.add_argument('-dir', type=bool, default=False)
    parser.add_argument('-seed', type=int)

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

    else:
        raise Exception("Under specification of parameters")

    return [args.fileName, n, r, rho, args.dir, args.seed]
    
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    SEED_LIM = 100_000

    fileBase,n,r,rho,dir,seed = ParseArgs()
    print('n = %d, r = %f, rho = %f' % (n, r, rho))

    seed = SetSeed(seed)
    print('seed = %d' % seed)

    random.seed(seed)
    nodeLoc = RandNodeCirc(n, r)

    if dir:
        links = FindDirLinksSlow(nodeLoc)
    else:
        links = FindBiLinksSlow(nodeLoc)

    net = (nodeLoc,links)
    Net.WriteNet(net, dir, fileBase + '_' + str(seed) + '.net')

# TODO:  Figure out how to make this work
if __name__ == '__test__':
    print("This is the test script !!!")