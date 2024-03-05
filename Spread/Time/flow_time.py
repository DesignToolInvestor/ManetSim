#
# f l o w _ t i m e . p y
#

# system packages
import math
import random
from datetime import datetime

# local libraries
import LocMath
import LocUtil
import MakeNet
import MaxFlow
import Component

###############################
if __name__ == "__main__":
    # constants
    FILE_NAME = "flow_time.log"

    MIN_NUM_NODE = 30
    MAX_NUM_NODE = 1_000
    NUM_NET = 100
    NUM_STREAM = 2

    SEED = 2

    # generate number of nodes in each network
    numNode = [round(LocMath.RandLog(MIN_NUM_NODE, MAX_NUM_NODE)) for k in range(NUM_NET)]
    print(sorted(numNode))

    # generate each network
    rho = 2
    timeInfo = []
    for n in numNode:
        seed = LocUtil.SetSeed(SEED)
        r = math.sqrt(n / rho / math.pi)
        
        net = MakeNet.RandNetCirc(n, r, dir=True)

        # get dominant component as sub-network
        subNet = NetPath.DomCompSubNet(net)
        nSubNet = len(subNet[0])

        # pick end points
        temp = random.sample(range(nSubNet), 2*NUM_STREAM)
        stream = [[temp[2*k], temp[2*k + 1]] for k in range(NUM_STREAM)]
        
        startTime = datetime.now()
        maxFlow = MaxFlow.MaxFlowRate(subNet, stream)
        endTime = datetime.now()
        
        info = [n,r,seed, stream, (endTime - startTime).total_seconds()]
        timeInfo.append(info)

    # write the data to the a file for graphing
    file = open(FILE_NAME, 'a')
    for info in timeInfo:
        file.write(f'{info}\n')
    file.close()