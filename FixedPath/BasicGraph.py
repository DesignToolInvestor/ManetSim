#
# B a s i c G r a p h . p y
#

import cvxpy
from LocUtil import Sub

def FracPack(graph):
    nNode,link = graph

    nodeWeightL = [cvxpy.Variable() for _ in range(nNode)]
    
    constraint = []
    for n0,n1 in link:
        constraint.append(nodeWeightL[n0] + nodeWeightL[n1] <= 1)
    
    for edgeWeight in nodeWeightL:
        constraint.append(0 <= edgeWeight)
    
    goal = cvxpy.Maximize(sum(nodeWeightL))
    prob = cvxpy.Problem(goal, constraint)
    prob.solve(solver=cvxpy.ECOS)

    if (prob.status != cvxpy.OPTIMAL):
        raise Exception("solver failure", prob.status)

    result = [float(var.value) for var in nodeWeightL]

    return result


def FracCover(graph):
    nNode, link = graph
    nLink = len(link)

    edgeWeightL = [cvxpy.Variable() for _ in range(nLink)]

    constraint = []
    for node in range(nNode):
        index = [i for i in range(nLink) if node in link[i]]
        constraint.append(sum(Sub(edgeWeightL, index)) >= 1)

    for edgeWeight in edgeWeightL:
        constraint.append(0 <= edgeWeight)

    goal = cvxpy.Minimize(sum(edgeWeightL))
    prob = cvxpy.Problem(goal, constraint)
    prob.solve(solver=cvxpy.ECOS)

    if (prob.status != cvxpy.OPTIMAL):
        raise Exception("solver failure", prob.status)

    result = [float(var.value) for var in edgeWeightL]

    return result