#
# S a t L o g . p y
#

# This "library" is designed to read and write log files associated with saturation tests.

from typing import NamedTuple
from fractions import Fraction as Frac

#######################################
class SatLogEnt(NamedTuple):
    # fields
    nNode: int
    rho: float
    netSeed: int

    nStream: int
    strSeed: int
    flowRate: Frac
    totDist: float

    time: float

    # accessor methods
    def AgFlow(self):
        return self.flowRate * self.totDist


#######################################
# A1 Format:  [[nNode, rho, netSeed], [nStream, streamSeeed, rateFrac, topLen], time]
def ConvA1(info):
    netInfo,streamInfo,runInfo = info
    result = SatLogEnt(*netInfo,*streamInfo,runInfo)

    return result


def ReadSatLog(fileName):
    with open(fileName, 'r') as file:
        first, *rest = file.readlines()

        match first.strip():
            case 'A1': convert = ConvA1
            case _: raise Exception('Format not recognized')

        result = []
        for line in rest:
            if not line.startswith('#'):
                result.append(convert(eval(line)))

    return result