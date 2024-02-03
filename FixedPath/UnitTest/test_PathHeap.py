#
# test_PathHeap.py
#

from unittest import TestCase
import random

from PathHeap import PathHeap
from LocUtil import Index, SetSeed, UnZip

################################################
def MakeToActive(active, nNode):
    result = [-1 for _ in range(nNode)]
    for k in range(len(active)):
        id_, _, _ = active[k]
        result[id_] = k

    return result

################################################
# TODO:  move inside the TestPathHap class ... without creating a new test that is this method
def CheckPathHeap(self, pathHeap, active, priTab):
    if active == []:
        self.assertEqual(pathHeap.active, [])
    else:
        id,pri,_ = UnZip(pathHeap.active)
        self.assertEqual({*id}, {*active})
        self.assertEqual(pri, Index(priTab,id))

    self.assertEqual(MakeToActive(pathHeap.active, len(pathHeap.toActive)), pathHeap.toActive)


################################################
class TestPathHeap(TestCase):
    def test_OverAll(self):
        # constants
        seed = None
        nNode = 15

        # set up
        unVisited = [k for k in range(nNode)]
        active = []
        retired = []
        pri = [float('nan') for k in range(nNode)]

        pathHeap = PathHeap(nNode)

        # do loop adding, changing priority, and popping
        seed = SetSeed(seed)

        while len(retired) < nNode:
            # add one unvisited node
            if len(unVisited) > 0:
                unVistedIndex = random.randint(0, len(unVisited) - 1)
                addId = unVisited[unVistedIndex]

                unVisited.pop(unVistedIndex)
                active.append(addId)

                newPri = random.random()
                pri[addId] = newPri

                pathHeap.Push(addId,newPri,-1)
                CheckPathHeap(self, pathHeap, active, pri)

            # do change on one active node
            if random.random() < 0.5:  # change priority
                activeIndex = random.randint(0, len(active) - 1)
                nodeId = active[activeIndex]

                newPri = random.random()
                pri[nodeId] = newPri

                pathHeap.ChangeCost(nodeId, newPri)

            else: # pop lowest priority node
                minPriIndex = 0
                minPri = pri[active[0]]
                for index in range(1, len(active)):
                    if pri[active[index]] < minPri:
                        minPriIndex = index
                        minPri = pri[active[index]]

                minNodeId = active[minPriIndex]
                retired.append(minNodeId)
                active.pop(minPriIndex)

                pathHeap.Pop()
                CheckPathHeap(self, pathHeap, active, pri)

            print(f'unvisited: {unVisited}, active: {active}')

    def test__buble(self):
        class PathHeapBub(PathHeap):
            def __init__(self, nNode, up, down):
                super().__init__(nNode)
                self.up = up
                self.down = down

            def _bubble_up(self, index):
                if not self.up:
                    raise Exception("Bubbled up when it shouldn't have")

            def _bubble_down(self, index):
                if not self.down:
                    raise Exception("Bubbled down when it shouldn't have")

        # constants
        nNode = 10

        # test case of no change
        h0 = PathHeapBub(nNode,False,False)
        h0.active = [(4,3,-1),(2,4,-1),(7,5,-1),(6,6,-1),(0,8,-1),(9,9,-1)]
        h0.toActive = MakeToActive(h0.active, nNode)
        h0._bubble(1)
        self.assertEqual([(4,3,-1),(2,4,-1),(7,5,-1),(6,6,-1),(0,8,-1),(9,9,-1)], h0.active)
        self.assertEqual(MakeToActive(h0.active, nNode), h0.toActive)

        # test case of up with 2 children
        h1 = PathHeapBub(nNode,True,False)
        h1.active = [(4,3,-1), (0,8,-1), (7,5,-1), (6,6,-1), (2,4,-1), (9,9,-1)]
        h1.toActive = MakeToActive(h1.active, nNode)
        h1._bubble(1)
        self.assertEqual([(4,3,-1), (2,4,-1), (7,5,-1), (6,6,-1), (0,8,-1), (9,9,-1)], h1.active)
        self.assertEqual(MakeToActive(h1.active, nNode), h1.toActive)

        # test case of up with 1 child
        h2 = PathHeapBub(nNode,True,False)
        h2.active = [(4,3,-1), (2,4,-1), (9,9,-1), (6,6,-1), (0,8,-1), (7,5,-1)]
        h2.toActive = MakeToActive(h2.active, nNode)
        h2._bubble(2)
        self.assertEqual([(4,3,-1), (2,4,-1), (7,5,-1), (6,6,-1), (0,8,-1), (9,9,-1)], h2.active)
        self.assertEqual(MakeToActive(h2.active, nNode), h2.toActive)

        # test case for down
        h3 = PathHeapBub(nNode,False,True)
        h3.active = [(7,5,-1), (2,4,-1),(4,3,-1), (6,6,-1), (0,8,-1), (9,9,-1)]
        h3.toActive = MakeToActive(h3.active, nNode)
        h3._bubble(2)
        self.assertEqual([(4,3,-1), (2,4,-1), (7,5,-1), (6,6,-1), (0,8,-1), (9,9,-1)], h3.active)
        self.assertEqual(MakeToActive(h3.active, nNode), h3.toActive)

    def test__buble_down(self):
        ph = PathHeap(10)
        ph.active = [(4,3,-1), (0,4,-1), (6,7,-1), (7,9,-1), (2,6,-1), (8,1,-1)]
        ph.toActive = MakeToActive(ph.active, 10)
        ph._bubble_down(5)
        self.assertEqual([(8,1,-1), (0,4,-1), (4,3,-1), (7,9,-1), (2,6,-1), (6,7,-1)], ph.active)
        self.assertEqual(MakeToActive(ph.active, 10), ph.toActive)


    def test__buble_up(self):
        ph = PathHeap(10)
        ph.active = [(6,7,-1), (0,4,-1), (8,1,-1), (7,9,-1), (2,6,-1), (4,3,-1)]
        ph.toActive = MakeToActive(ph.active, 10)
        ph._bubble_up(0)
        self.assertEqual([(8,1,-1), (0,4,-1), (4,3,-1), (7,9,-1), (2,6,-1), (6,7,-1)], ph.active)
        self.assertEqual(MakeToActive(ph.active, 10), ph.toActive)

    def test__child_index(self):
        pathHeap = PathHeap(10)
        childIndex = [pathHeap._child_index(k) for k in range(7)]
        self.assertEqual([(1,2), (3,4), (5,6), (7,8), (9,10), (11,12), (13,14)], childIndex)

    def test__parent_index(self):
        pathHeap = PathHeap(10)
        parentIndex = [pathHeap._parent_index(k) for k in range(15)]
        self.assertEqual([-1,0,0,1,1,2,2,3,3,4,4,5,5,6,6], parentIndex)