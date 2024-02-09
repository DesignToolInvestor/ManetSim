#
# c o n s t r a i n t _ t i m e . p y
#

# This program is to test the speed at which independent subset can be constructed from a link
# graph.

# system files
import argparse
from scanf import scanf
from os import listdir

# local files
from FracChromNum import FracChromNum
from Graph import ReadGraph
from LocMath import RealToFrac
from Log import Log
from StopWatch import StopWatch

# different algorithms for independent subsets
from IndependPrune import IndSubSet
# from IndependSlow import IndSubSet

#######################################
def ParseArgs():
    parser = argparse.ArgumentParser(
        prog='constraint_time',
        description='This script will read the files in a directory and time the setup and solver'
    )

    parser.add_argument('folder', type=str)
    args = parser.parse_args()

    return args.folder

########################################
if __name__ == "__main__":
    # constants
    nameFormat = "shortest_%d_%f_%d_%d.graph"

    maxN = 30
    expectedRho = 2.0

    snirDb = 0
    gamma = 2

    # parse arguments
    folder = ParseArgs()

    # read directory
    fileNameL = listdir(folder)
    scanL = [scanf(nameFormat, fileName) for fileName in fileNameL]
    fileTab = [(name,info) for (name,info) in zip(fileNameL, scanL) if info != None]

    # fileTab = [['shortest_300_2.0_30047_8.graph', (300,2.0,30047,8)]]

    nFile = len(fileTab)

    # do for each file
    log = Log("slow.log", 60)
    for name,(netSize,rho,seed,pathLen) in fileTab:
        assert(rho == expectedRho)

        if pathLen <= maxN:
            # read interference graph
            graph = ReadGraph(f'{folder}/{name}')
            nNode,_ = graph
            print(f'pathLen = {pathLen}, nNode = {nNode}')

            # compute independent subsets
            constTimer = StopWatch(running=True)
            indSubSet = IndSubSet(graph)
            constSec = constTimer.Stop()

            indSubSet.sort(key=lambda elem: (len(elem), elem))

            # # solve for the chromatic number
            solveTimer = StopWatch(running=True)
            result = FracChromNum(nNode, indSubSet)
            solveSec = solveTimer.Stop()

            chromNum = RealToFrac(sum(result))

            # log the results
            line = (f'[[{netSize}, {rho}, {seed}], '
                    f'[{nNode}, {len(indSubSet)}, {constSec}], '
                    f'[{chromNum}, {solveSec}]]')
            log.Log(line)

    log.Flush()
