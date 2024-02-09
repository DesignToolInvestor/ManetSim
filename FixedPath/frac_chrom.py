#
# f r a c _ c h r o m . p y
#

# This script computes the fractional chromatic number of a graph.

# TODO: why can't I import parser.add_argument as add_argument
import argparse
import cvxpy

from LocMath import PowerSet, RealToFrac
from LocUtil import Sub
from IndependSlow import IndSubSet
from FracChromNum import FracChromNum

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
    # TODO:  fix lack of code reuse
    with open(fileName, 'r') as file:
        first, *rest = file.readlines()

    nNode = int(first)
    linkL = [eval(line) for line in rest]
    print(f'link = {linkL}')

    # power set of nodes
    indSubSet = IndSubSet(nNode, linkL)
    result = FracChromNum(nNode, indSubSet)

    nResult = len(result)
    print(f'[', end='')
    for i in range(nResult - 1):
        print(f'({i}, {result[i].numerator}/{result[i].denominator})', end='')
    print(f'({i}, {result[nResult].numerator}/{result[nResult].denominator})]')

    printRes = [f'({i}, {frac.numerator}/{frac.denominator}))'
                for (i,frac) in enumerate(result) if frac != 0]

    print(sum(result))