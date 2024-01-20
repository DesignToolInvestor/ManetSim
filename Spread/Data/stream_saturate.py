#
# s t r e a m _ s a t u r a t e . p y
#

# This script will increase the number of streams passed the point of saturating aggregate flow.

# system packages
import math
import random
from datetime import datetime

import LocMath
# local libraries
import LocUtil
import MakeNet
import MaxFlow
import NetPath

if __name__ == '__main__':
    # constants
    NUM_NET = 4
    N_NODE = 200
    NUM_ESCILATION = 4
    MAX_NUM_STREAM = 15
    
    RHO = 2.0
    RAD = math.sqrt(N_NODE / RHO / math.pi)

    NUM_DIG_SEED = 3

    # start time
    progStartTime = datetime.now()

    # parse args
    fileName = "stream_saturate.log"
    log = []

    for netNum in range(NUM_NET):
        # make network
        netSeed = LocUtil.SetSeed()
        net = MakeNet.RandNetCirc(N_NODE, RAD, dir=True)

        subNet = NetPath.DomCompSubNet(net)
        nodeLoc,link = subNet
        nSubNet = len(nodeLoc)

        for escNum in range(NUM_ESCILATION):
            streamSeed = LocUtil.SetSeed()

            temp = random.sample(range(nSubNet), 2 * MAX_NUM_STREAM)
            stream = [[temp[2 * k], temp[2 * k + 1]] for k in range(MAX_NUM_STREAM)]

            streamEnd = LocUtil.Index(nodeLoc, stream)
            streamDist = list(map(lambda vec: LocMath.Dist(vec[0],vec[1]), streamEnd))

            for numStream in range(1, MAX_NUM_STREAM + 1):
                startTime = datetime.now()
                maxFlow = MaxFlow.MaxFlowRate(subNet, stream[:numStream])
                endTime = datetime.now()

                totalTime = (endTime - startTime).total_seconds()

                maxFlowFrac = LocMath.RealToFrac(maxFlow)
                maxFlowAdjust = maxFlowFrac.numerator / maxFlowFrac.denominator
                agFlow = maxFlow * sum(streamDist[:numStream])

                info = \
                    [[N_NODE, RAD, netSeed, streamSeed],
                     [numStream, maxFlowFrac, agFlow],
                     totalTime]
                log.append(info)

    with open(fileName, 'a') as file:
        for info in log:
            fracStr = str(info[1][1])
            line = f'[{info[0]}, [{info[1][0]}, {fracStr}, {info[1][2]}], {info[2]}]\n'
            file.write(line)

    # Report total time
    progStopTime = datetime.now()
    print(f'Total time: {progStopTime - progStartTime}')