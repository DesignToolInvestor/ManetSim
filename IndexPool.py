#
# I n d e x P o o l . p y
#
# This is an abstract data type that maintains a pool of "active" elements that are a subset of the
# n-elements.  The elements are referenced by their elemId from 0 to n-1.
#
# When popping elements from the pool an arbitrary element its chosen (i.e., not necessary the last one
# added, though there is a tendency to pop elements that were added more recently before popping elements
# there were added earlier).  This lack of order of the popping makes all the operations O(1), the memory
# needed for the elemId is O(n) rather than O(m) (where m is the number of active elements).  This is simular
# to the trade made by hashing algorithms.  But the extra memory overhead is significantly less than for
# hashing.  In addition, the locality of reference is much better for this algorithm than for hashing.  In
# fact the cashing affects should be better for this algorithm than for either the O(ln(n)) approach or the
# hashing approach.  Nevertheless, for some parameters, workload and machines, when m << n, this might be
# slower than the O(ln(n)) method because of memory affects (e.g., cacheing and paging). 

class IndexPool:
    def __init__(self, indexSize, initFull = False):
        self.indexSize = indexSize
        if initFull:
            self.poolIndex = [k for k in range(indexSize)]
            self.pool = self.poolIndex.copy()
        else:
            self.poolIndex = [-1 for k in range(indexSize)]
            self.pool = []

    def Push(self, elemId):
        if (self.poolIndex[elemId] == -1):
            self.poolIndex[elemId] = len(self.pool)
            self.pool.append(elemId)

    def Drop(self, elemId):
        if (self.poolIndex[elemId] != -1):
            poolSize = len(self.pool)
            poolPos = self.poolIndex[elemId]

            poolEnd = self.pool.pop()
            if (poolPos != (poolSize - 1)):
                self.pool[poolPos] = poolEnd
                self.poolIndex[poolEnd] = poolPos
            self.poolIndex[elemId] = -1

    def Pop(self) -> int:
        if len(self.pool) == 0:
            return None
        else:
            elemId = self.pool.pop()
            self.poolIndex[elemId] = -1
            return elemId

    def Len(self) -> int:
        return len(self.pool)

    def Active(self, index) -> bool:
        return (self.poolIndex[index] >= 0)