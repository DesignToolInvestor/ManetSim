#
# N u m P a t h . p y
#

from NetPath import MakeNetPath
from LocUtil import SetSeed
from Cost import NetR

def CompAllPaths(net, start, ent):
  numHop = 1



if __name__ == "__main__":
  # constants
  masterSeed = None
  seedDig = 3

  nNode = 30
  rho = 2

  seed = SetSeed(masterSeed, seedDig)

  # make network and path
  netR = NetR(nNode, rho)
  net = MakeRandNet(nNode, netR)

  # pick end points
  domComp,*rest = Comp(net)
  endPoints = rand.sample(domComp, 2)

  # Find all loop-free paths
  allPaths = CompAllPaths(net, *endPoints)