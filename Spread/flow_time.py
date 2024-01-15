#
# flow_time.py
#

# system packages
import math
import random
from datetime import time

# local libraries
import LocMath
import LocUtil
import MakeNet
import MaxFlow
import Net

if __name__ == "__main__":
    # constants
    FILE_NAME = "flow_time.txt"

    MIN_NUM_NODE = 10
    MAX_NUM_NODE = 60
    NUM_NET = 10
    NUM_STREAM = 2

    SEED = 0

    # generate number of nodes in each network
    numNode = [math.round(LocMath.RandLog(MIN_NUM_NODE, MAX_NUM_NODE)) for k in range(NUM_NET)]

    # generate each network
    rho = 2
    timeInfo = []
    for n in numNode:
        seed = LocUtil.SetSeed(SEED)
        r = math.sqrt(n * rho / math.pi)
        
        net = MakeNet.RandCircNet(n, r)
        subNet = Net.ConectSubNet(net)

        temp = random.choice(2*NUM_STREAM)
        stream = [[temp[2*k], temp[2*k + 1]] for k in range(NUM_STREAM)]
        
        startTime = time.time()
        maxFlow = MaxFlow.MaxFlow(subNet, stream)
        endTime = time.time()
        
        info = [n,r,seed, stream, endTime - startTime]
        timeInfo.append()

    # write the data to the a file for graphing
    file = open(FILE_NAME, 'w')
    for info in timeInfo:
        file.write(f'{info}')
    file.close()