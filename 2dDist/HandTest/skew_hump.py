#
# s k e w _ h u m p . p y
#

from math import exp
from matplotlib import pyplot as plot

from Dist import SkewHump
from LocUtil import Grid1


if __name__ == "__main__":
  nPoint = 101

  dist = SkewHump()

  # plot PDF
  plot.subplots(figsize=(9, 6.5))

  kList = [exp(k) for k in range(-3,4)]
  xL = Grid1(0, 1, nPoint)

  for k in kList:
    yL = [dist.Pdf(x, k) for x in xL]
    plot.plot(xL,yL)

  plot.xlabel('x')
  plot.ylabel('PDF')

  plot.savefig('skew_hump_pdf.png')

  # plot CDF
  plot.subplots(figsize=(9, 6.5))

  for k in kList:
    yL = [dist.Cdf(x, k) for x in xL]
    plot.plot(xL,yL)

  plot.xlabel('x')
  plot.ylabel('CDF')

  plot.savefig('skew_hump_cdf.png')