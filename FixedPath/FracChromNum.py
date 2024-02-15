#
# F r a c C h r o m N u m . p y
#

# This library computes the fractional chromatic number of a graph, given a set of independent
# links

import cvxpy
from LocUtil import Sub

def FracChromNum(subSetGraph):
    # parse arguments
    nNode,subSet = subSetGraph
    nSubSet = len(subSet)

    # TODO:  change to a vector
    subSetWeight = [cvxpy.Variable() for _ in range(nSubSet)]

    const = []
    for node in range(nNode):
        index = [i for i in range(nSubSet) if node in subSet[i]]
        const.append(sum(Sub(subSetWeight,index)) >= 1)

    for var in subSetWeight:
        const.append(var >= 0)

    goal = cvxpy.Minimize(sum(subSetWeight))

    prob = cvxpy.Problem(goal, const)
    prob.solve(solver=cvxpy.ECOS)

    if (prob.status != cvxpy.OPTIMAL):
        raise Exception("solver failure", prob.status)

    result = [float(var.value) for var in subSetWeight]

    return result