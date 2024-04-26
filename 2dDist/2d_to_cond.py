#
# 2 d _ t o _ c o n d . p y
#

from scipy import e, lambertw

from random import uniform

# This produces a sample in the Gamma distribution where shape=2 and rate=1.
# That is PDF = x * exp(-x)
def Gama2_1():
  cdf = uniform(0,1)
  val = -lambertw((cdf - 1)/e) - 1

def Sample():
  x = uniform(0,20)
  y =


if __name__ == "__main__":
  # constants
  nSample = 2_000

  # synthetic data
