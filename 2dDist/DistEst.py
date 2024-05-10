#
# D i s t E s t . p y
#


# TODO:  Create a group version of this code that is much faster for a group of points
# Not the most compact code, but is fast
def SampCdf2(samp, point):
  p0,p1 = point

  count = 0
  for (s0,s1) in samp:
    if (s0 <= p0) and (s1 <= p1):
      count += 1

  return count / len(samp)
