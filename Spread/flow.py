#
# f l o w . p y
#
# This program solves the capacity problem for a fixed number of flows on a given network.
#
# The problem formulation is to randomly pick end-point for the specified number of flows and then
# set up the optimization problem to be solved via a separate program.
#
# TODO:  Document the arguments

# system packages
import argparse
import random
import scanf

# local packages
import Net
import MaxFlow
import LocMath


def RandEnds(nNode, nPair):
    result = []
    for k in range(nPair):
        pair = [random.randint(0, nNode), random.randint(0, nNode)]
        while (pair[0] == pair[1]):
            pair = [random.randint(0, nNode), random.randint(0, nNode)]
        result.append(pair)

    return result


#######################################
def ParseArgs():
    parser = argparse.ArgumentParser(
        prog='stream',
        description='This program will compute the path of the optimal stream'
    )

    parser.add_argument('fileName', type=str)
    parser.add_argument('-n', type=int)
    parser.add_argument('-stream', type=str)
    parser.add_argument('-seed', type=int)

    args = parser.parse_args()
    if (args.n == None) and (args.stream == None):
        raise Exception('Must either specify the number of flows (to be picked randomly) or the flows')
    elif (args.n != None) and (args.stream != None):
        raise Exception("Can't specify both the number of random flows and the flows")

    return [args.fileName, args.n, args.stream, args.seed]


#######################################
if __name__ == '__main__':
    # parse command line
    fileName,n,flowStr,seed = ParseArgs()

    # read network
    net,direct = Net.ReadNet(fileName)
    if not direct:
        raise Exception("The network must be directional.")
    nodes,links = net
    nNode = len(nodes)

    # deal with flows
    if n != None:
        assert(flowStr == None)
        seed = SetSeed(seed)

        # TODO:  Do choose without replacement
        stream = []
        for k in range(n):
            source = random.randint(0, nNode - 1)
            sink = random.randint(0, nNode - 1)
            stream[k].append([source, sink])

    else:
        assert(flowStr != None)

        flowStrList = flowStr.split("),")
        stream = list(map(lambda str: scanf.scanf("(%d,%d", str), flowStrList))

    maxRate = MaxFlow.MaxFlowRate(net, stream)
    print(f'Maximum Flow Rate = {maxRate}')
    print(f'Fracional Value = {LocMath.RealToFrac(maxRate)}')