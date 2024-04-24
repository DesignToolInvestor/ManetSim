#
# n u m _ h o p . p y
#

# This script will create a log the number of hops as a function of distance for use in
# estimating the distribution.

# system packages
from math import ceil
from random import sample

# local files
from LocUtil import SetSeed, Sub
from LocMath import Dist
from MakeNet import NetR, RandNetCirc
from Component import Component
from BestPath import BestPath
from Log import Log

if __name__ == "__main__":
  # constants
  rho = 2

  nNode = 500

  minNSamp = 2_000
  pathPerNet = 22
  nNet = ceil(minNSamp/pathPerNet)

  numSeedDig = 5

  outFile = 'test.log'
  logDelay = 15

  # set up loop
  netR = NetR(nNode, rho)

  log = Log(outFile, logDelay)

  # do main loop
  for _ in range(nNet):
    netSeed = SetSeed(digits=numSeedDig)
    net = RandNetCirc(nNode, netR)
    nodeLoc,link = net

    # TODO:  fix to work for for arbitrary cost functions
    linkCost = [Dist(nodeLoc[n0], nodeLoc[n1]) for (n0,n1) in link]

    domComp,*rest = Component(net)
    nDomComp = len(domComp)

    for _ in range(pathPerNet):
      pathSeed = SetSeed(digits=numSeedDig)

      endNode = sample(domComp, 2)
      endLoc = Sub(nodeLoc, endNode)
      dist = Dist(*endLoc)

      path = BestPath(net, endNode, linkCost)
      nHop = len(path) - 1

      info = [[nNode, rho, netSeed], endNode, [nHop, dist]]
      log.Log(info)


  log.Flush()
