#
# p l o t _ n h o p . p y
#

# This script will plot the number of hops vs the distance

from matplotlib import pyplot as plot

from LocUtil import UnZip


if __name__ == "__main__":
  # constants
  logFile = 'test.log'

  # read data
  with open(logFile, 'r') as file:
    lines = file.readlines()

  info = [eval(line) for line in lines]

  _,_,pathInfo = UnZip(info)
  nHop,dist = UnZip(pathInfo)

  # plot result
  fig,ax = plot.subplots()

  plot.plot(dist,nHop, '*', markersize=3)

  plot.xlabel('Distance (units of R)')
  plot.ylabel('Num. of Hops')


  plot.show()