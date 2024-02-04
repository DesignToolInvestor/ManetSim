#
# P a t h H e a p . p y
#

from LocUtil import Swap

# TODO:  get rid of pathParent ... not needed is stored by the caller
class PathHeap:
    def __init__(self, nNode):
        self.active = []
        self.toActive = [-1 for i in range(nNode)]
    
    def Push(self, nodeId, cost, pathParent):
        self.active.append((nodeId, cost, pathParent))
        index = len(self.active) - 1
        self.toActive[nodeId] = index

        self._bubble(index)
    
    def Pop(self):
        if (len(self.active) == 1):
            elem = self.active.pop()
            self.toActive[elem[0]] = -1

            return elem

        else:
            lowElem = self.active[0]
            highElem = self.active.pop()
            self.active[0] = highElem

            self.toActive[highElem[0]] = 0
            self.toActive[lowElem[0]] = -1

            self._bubble(0)
        
            return lowElem
    
    def Peak(self, nodeId):
        if self.toActive[nodeId] == -1:
            return None
        else:
            return self.active[self.toActive[nodeId]]
    
    def ChangeCost(self, nodeId, newCost, newParent):
        index = self.toActive[nodeId]
        
        if index < 0:
            raise Exception("Can't change cost on non-active node")
        else:
            id,oldCost,_ = self.active[index]
            newElem = (id, newCost, newParent)
            self.active[index] = newElem
            self._bubble(index)

    # Naming complexity is too great in the method.  The conventions are:
    #   index:  is the the index into the active array
    #   id:  is the node index.
    #   pathParent:  is the parent in the shortest path
    #   parent:  is the parent in the heap
    #   child:  is the child in the heap
    #   pIndex:  is used for parent index (in the heap)
    #   cIndex:  is used for child index (in the heap)
    def _bubble(self, index):
        id,cost,pathParent = self.active[index]

        moved = False
        # the lowest elem has no parent
        if 0 < index:
            pIndex = self._parent_index(index)
            pId,pCost,pPathParent = self.active[pIndex]

            if cost < pCost:
                moved = True
                self._swap(pIndex, index)
                self._bubble_down(pIndex)

        if not moved:
            cIndex0,cIndex1 = self._child_index(index)
            nActive = len(self.active)

            if cIndex0 < nActive:
                if nActive == cIndex1:
                    minCIndex = cIndex0
                else:
                    if self.active[cIndex0][1] < self.active[cIndex1][1]:
                        minCIndex = cIndex0
                    else:
                        minCIndex = cIndex1

                cId,cCost,cPathParent = self.active[minCIndex]
                if cCost < cost:
                    self._swap(minCIndex, index)
                    self._bubble_up(minCIndex)

    def _swap(self, index0, index1):
        id0, _, _ = self.active[index0]
        id1, _, _ = self.active[index1]

        Swap(self.active, index0, index1)
        Swap(self.toActive, id0, id1)

    def _bubble_down(self, index):
        done = False
        while not done:
            pIndex = self._parent_index(index)
            if pIndex < 0:
                done = True
            else:
                _, cost, _ = self.active[index]
                _, pCost, _ = self.active[pIndex]

                if pCost <= cost:
                    done = True
                else:
                    self._swap(pIndex, index)
                    index = pIndex


    def _bubble_up(self, index):
        nActive = len(self.active)

        done = False
        while not done:
            c0, c1 = self._child_index(index)

            if nActive <= c0:
                done = True
            else:
                if nActive == c1:
                    minCIndex = c0
                    _, minCCost, _ = self.active[minCIndex]
                else:
                    _, cost0, _ = self.active[c0]
                    _, cost1, _ = self.active[c1]

                    if cost0 < cost1:
                        minCIndex = c0
                        minCCost = cost0
                    else:
                        minCIndex = c1
                        minCCost = cost1

                _, cost, _ = self.active[index]
                if minCCost < cost:
                    self._swap(minCIndex, index)
                    index = minCIndex
                else:
                    done = True

    def _parent_index(self, index):
        return ((index - 1) // 2)

    def _child_index(self, index):
        return (2*index + 1, 2*index + 2)


