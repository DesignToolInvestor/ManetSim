#
# s t r e a m _ s a t u r a t e . p y
#

# This script will increase the number of streams passed the point of saturating aggregate flow.

# system packages
import random
from datetime import datetime

# local libraries
import LocMath
import LocUtil
import Log
import MakeNet
import MaxFlow
import NetPath

if __name__ == '__main__':
    # constants
    NUM_NET = 8
    N_NODE = 200
    ESC_PER_NET = 8
    MAX_NUM_STREAM = 16
    
    RHO = 4.0
    R = MakeNet.R(N_NODE, RHO)

    DELAY = 3 * 60

    NUM_DIG_SEED = 3

    # start time
    progStartTime = datetime.now()

    # parse args
    fileName = "test.log"
    log = Log.Log(fileName, DELAY)

    for netNum in range(NUM_NET):
        # make network
        netSeed = LocUtil.SetSeed()
        net = MakeNet.RandNetCirc(N_NODE, R, dir=True)

        subNet = NetPath.DomCompSubNet(net)
        nodeLoc,link = subNet
        nSubNet = len(nodeLoc)

        for escalation in range(ESC_PER_NET):
            streamSeed = LocUtil.SetSeed()

            temp = random.sample(range(nSubNet), 2 * MAX_NUM_STREAM)
            stream = [[temp[2 * k], temp[2 * k + 1]] for k in range(MAX_NUM_STREAM)]

            streamEnd = LocUtil.Index(nodeLoc, stream)
            streamDist = list(map(lambda vec: LocMath.Dist(vec[0],vec[1]), streamEnd))

            for numStream in range(1, MAX_NUM_STREAM + 1):
                startTime = datetime.now()
                try:
                    maxFlow = MaxFlow.MaxFlowRate(subNet, stream[:numStream])

                    endTime = datetime.now()
                    totalTime = (endTime - startTime).total_seconds()

                    maxFlowFrac = LocMath.RealToFrac(maxFlow)
                    maxFlowAdjust = maxFlowFrac.numerator / maxFlowFrac.denominator
                    agFlow = maxFlow * sum(streamDist[:numStream])

                    info = \
                        [[N_NODE, R, netSeed],
                         [numStream, streamSeed, str(maxFlowFrac), agFlow],
                         totalTime]
                    log.Log(info)

                    print(f'{netNum}, {escalation}, {numStream}, {datetime.now() - progStartTime}')

                except:
                    print(f"{netNum}, {escalation}, {numStream}: Couldn't Solve")