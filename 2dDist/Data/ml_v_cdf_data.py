#
# D a t a / m l _ v _ c d f _ d a t a . p y
#

import numpy as np
from sympy import lambdify, log
from scipy.optimize import fsolve, curve_fit

import DistA as dist

from LocMath import RandLog
from LocUtil import SetSeed
from Log import Log
from StopWatch import StopWatch


#######################################################
def MaxLikeDistA(samp):
  termSym = log(dist.pdfSym).diff(dist.aSym).simplify()
  termF = lambdify((dist.xSym, dist.aSym), termSym)

  f = lambda a,samp: sum(termF(x,a) for x in samp)[0]

  result = fsolve(f,1, args=list(samp))

  return result[0]


def CdfFitDistA(samp):
  n = len(samp)
  quant = tuple((k + 0.5) / n for k in range(n))
  param_, _ = curve_fit(dist.CdfNum, samp, quant)

  return param_[0]

#######################################################
if __name__ == "__main__":
  # constants
  minN = 30
  maxN = 30_000

  maxSamp = 300 - 185

  aTrue = 0.3
  fileName = 'DistA_0.3.log'

  runTime = 2*60*60
  logInterval = 30
  
  seedDig = 5

  # setup
  dataLog = Log(fileName, logInterval)

  totalTime = StopWatch()
  taskTime = StopWatch()

  # generate data
  totalTime.Start()
  nSamp = 0

  while (totalTime.Seconds() < runTime) and (nSamp < maxSamp):
    n = round(RandLog(minN,maxN))
    seed = SetSeed(None,seedDig)

    samp = tuple(sorted(dist.GenSamp(aTrue) for _ in range(n)))
    sampNp = np.array(samp)

    taskTime.Reset().Start()
    aMle = MaxLikeDistA(samp)
    timeMle = taskTime.Stop()

    taskTime.Reset().Start()
    aCdf = CdfFitDistA(samp)
    timeCdf = taskTime.Stop()

    info = [[n, seed, aTrue], [aMle, timeMle], [aCdf, timeCdf]]
    dataLog.Log(info)

    nSamp += 1

    print(f'{totalTime.Delta()}:  {n}, {timeMle:.2f}, {timeCdf:.2f}')

  # clean up
  dataLog.Flush()
