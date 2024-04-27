#
# r a n d _ q u a l . p y
#

from matplotlib import pyplot as plot
from random import uniform

from LocUtil import LogGrid1


if __name__ == "__main__":
  # constants
  minNSamp = 50
  maxNSamp = 5_000

  # plot deveation
  samp = [uniform(0,1) for _ in range(nSamp)]
  sampSort = sorted(samp)

  quant = [(k + 0.5) / nSamp for k in range(nSamp)]
  dev = [s - q for (s,q) in zip(sampSort,quant)]

  # graph deveation
  plot.plot(sampSort,dev, '*', c="maroon", zorder=1)

  plot.show()
