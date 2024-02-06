#
# f r a c _ c h r o m . p y
#

# This script computes the fractional chromatic number of a graph.

# TODO: why can't I import parser.add_argument as add_argument
import argparse
import cvxpy

from LocMath import PowerSet, RealToFrac
from LocUtil import Sub

#######################################
def ParseArgs():
    parser = argparse.ArgumentParser(
        prog='frac_chrom.py',
        description='This program will compute the fractional chromatic number of a graph.'
    )

    parser.add_argument('fileName', type=str)

    args = parser.parse_args()

    return args.fileName


if __name__ == "__main__":
    # parse args
    fileName = ParseArgs()

    # read graph
    with open(fileName, 'r') as file:
        first, *rest = file.readlines()

    nNode = int(first)
    linkL = [eval(line) for line in rest]
    print(f'link = {linkL}')

    # power set of nodes
    indepSet = []
    powerSet = PowerSet(nNode)

    for set in powerSet:
        if (0 < len(set)):
            setLen = len(set)

            i0 = 0
            done = False
            while (i0 < setLen) and not done:
                i1 = i0 + 1

                while (i1 < setLen) and not done:
                    link = (set[i0], set[i1])
                    if link in linkL:
                        done = True
                    i1 += 1

                i0 += 1
                
            if not done:
                indepSet.append(set)

    print(indepSet)

    # create constraint
    nIndep = len(indepSet)
    # TODO:  change to a vector
    indepVar = [cvxpy.Variable() for _ in range(nIndep)]

    const = []
    for node in range(nNode):
        index = [i for i in range(nIndep) if node in indepSet[i]]
        print(f'index = {index}')
        const.append(sum(Sub(indepVar,index)) >= 1)

    for var in indepVar:
        const.append(var >= 0)

    goal = cvxpy.Minimize(sum(indepVar))

    prob = cvxpy.Problem(goal, const)
    prob.solve(solver=cvxpy.ECOS)

    if (prob.status != cvxpy.OPTIMAL):
        raise Exception("solver failure", prob.status)

    result = [RealToFrac(float(var.value)) for var in indepVar]
    print(result)