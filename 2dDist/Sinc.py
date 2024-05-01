#
# S i n c . p y
#

from collections import namedtuple

Map = namedtuple('Map', ['For', 'Inv'])

def StripFit(x,y):
  return None


def FindShift(lowX,highX, mapFor):
  shift = 0

  for i in range(5):
    lowZ = mapFor(lowX)
    highZ = mapFor(highX)

    mid = (lowZ + highZ) / 2
