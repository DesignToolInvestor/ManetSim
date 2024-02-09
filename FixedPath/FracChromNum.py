#
# F r a c C h r o m N u m . p y
#

# This library computes the fractional chromatic number of a graph, given a set of independent
# links

import cvxpy
from LocMath import RealToFrac
from LocUtil import Sub

def FracChromNum(nNode, indSubSet):
    # create constraint
    nIndep = len(indSubSet)

    # TODO:  change to a vector
    indepVar = [cvxpy.Variable() for _ in range(nIndep)]

    const = []
    for node in range(nNode):
        index = [i for i in range(nIndep) if node in indSubSet[i]]
        const.append(sum(Sub(indepVar,index)) >= 1)

    for var in indepVar:
        const.append(var >= 0)

    goal = cvxpy.Minimize(sum(indepVar))

    prob = cvxpy.Problem(goal, const)
    prob.solve(solver=cvxpy.ECOS)

    if (prob.status != cvxpy.OPTIMAL):
        raise Exception("solver failure", prob.status)

    result = [float(var.value) for var in indepVar]

    return result