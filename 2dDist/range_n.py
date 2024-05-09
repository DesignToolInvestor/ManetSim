#
# r a n g e _ n . p y
#

# system packages
from matplotlib import pyplot as plot

# local files and library files
import Dist
from LocUtil import Grid1, SetSeed, UnZip
from Map import LogRatio
from Sinc import SincFit

##############################################
# plot results
def Plot():
  plot.subplots(figsize=(9, 6.5))

  # true CDF
  xL = Grid1(0, 2, nPlotPoint)
  cdf = [dist.Cdf(x) for x in xL]
  plot.plot(xL, cdf, c="Blue", label="Ture CDF")

  # samples
  quant = [(k + 0.5) / nSamp for k in range(nSamp)]
  plot.plot(sorted(sampVal), quant, '.', c="Maroon", label="Samples", zorder=1)

  # estimated CDF
  xL = [2 * (k + 0.5) / nPlotPoint for k in range(nPlotPoint)]
  interp = fit.Interp(xL)
  plot.plot(xL, interp, c="Green", label="Est. CDF", zorder=-1)

  sinPoint = fit.SincPoint()
  plot.plot(*UnZip(sinPoint), 'o', c="Green", ms=8, zorder=0)

  # annotate
  plot.xlabel("X")
  plot.ylabel("Quantile")
  plot.legend()

  text = (f'Seed = {seed}\n'
          f'{nSamp} samples\n'
          f'{fit.nSinc} sinc-points\n'
          f'Z shift = {fit.z0:.2f}\n'
          f'h = {fit.h:.3f}')
  plot.text(1.2, 0.4, text)

  plot.savefig(f'Data/ExampB/dist_fit_b_{seed}_{nSamp}_{nSinc}.png')

##############################################
if __name__ == "__main__":
  # constants
  nSamp = 100

  nPlotPoint = 100
  givenSeed = 397
  seedDig = 3

  nSincRange = (3,20)

  dist = Dist.ExampB()

  ##############################################
  # compute samples
  seed = SetSeed(givenSeed, digits=seedDig)
  if givenSeed is None:
    print(f'seed = {seed}')

  sampVal = [dist.Sample() for _ in range(nSamp)]

  # generate graphs
  for nSinc in range(*nSincRange):
    mapProb = LogRatio((0,2))
    fit = SincFit(sampVal, mapProb, (1,1), (0,0), nSinc)

    Plot()
