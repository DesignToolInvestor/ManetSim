#
# r a n d _ q u a l . p y
#

from math import sqrt
from matplotlib import pyplot as plot
from random import uniform

from LocMath import RandLog
from PlotFit import PlotFitLogLog

if __name__ == "__main__":
  # constants
  minNSamp = 50
  maxNSamp = 5_000

  nSamp = 300

  # select sizes
  sizeL = [round(RandLog(minNSamp,maxNSamp)) for _ in range(nSamp)]

  # compute results
  maxDev = []
  rmsDev = []

  for size in sizeL:
    samp = [uniform(0, 1) for _ in range(size)]
    sampSort = sorted(samp)

    quant = [(k + 0.5) / size for k in range(size)]
    dev = [s - q for (s, q) in zip(sampSort, quant)]

    temp = max(abs(d) for d in dev)
    maxDev.append(temp)

    temp = sqrt(sum(d*d for d in dev) / size)
    rmsDev.append(temp)

  # plot deveation
  fig,ax = plot.subplots(2, figsize=(6.5, 9))

  # do max deveation
  PlotFitLogLog(sizeL,maxDev, axis=ax[0])

  ax[0].legend()
  ax[0].set_ylabel('Maximum Deviation')

  # do RMS deveation
  PlotFitLogLog(sizeL,rmsDev, axis=ax[1])

  ax[1].legend()
  ax[1].set_xlabel('Sample Size')
  ax[1].set_ylabel('RMS Deviation')

  plot.savefig('rand_qual.png')
