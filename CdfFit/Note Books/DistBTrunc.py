#
# D i s t B T r u n c . p y
#

# This file

#######################  generated code beyond this point  #######################

from math import cos, exp, pi, sin
from scipy.optimize import fsolve

def CdfZTrunc(lev):
  leftZ = fsolve(lambda z: -162*pi**2*exp(5*z)/5 + lev, -1.6140406574982338)[0]
  rightZ = fsolve(lambda z: -16*exp(-3*z) + lev, 1.6917246050779937)[0]
  return (leftZ,rightZ)

def NullZ(z):
  result = (4*exp(2*z) + 27*pi**2)*exp(4*z)/(4*exp(6*z) + 3*(8 + 9*pi**2)*exp(4*z) + 4)
  return result

def ResZ(z):
  result = (2*pi*(1 - cos(3*pi*exp(z)/(exp(z) + 1)))*(exp(z) + 1)**3*(4*exp(6*z) + (24 + 27*pi**2)*exp(4*z) + 4)/3 + pi**3*(exp(z) + 1)**3*(-36*exp(2*z) - 243*pi**2)*exp(4*z)/9 - 4*(exp(z) + 1)**3*(4*exp(6*z) + (24 + 27*pi**2)*exp(4*z) + 4)*sin(3*pi*exp(z)/(exp(z) + 1))/9 - 2*pi**2*(exp(z) + 1)**2*(4*exp(6*z) + (24 + 27*pi**2)*exp(4*z) + 4)*exp(z)*sin(3*pi*exp(z)/(exp(z) + 1)) + 4*pi*(exp(z) + 1)**2*(4*exp(6*z) + (24 + 27*pi**2)*exp(4*z) + 4)*exp(z)*cos(3*pi*exp(z)/(exp(z) + 1))/3 + 2*pi**2*(exp(z) + 1)*(4*exp(6*z) + (24 + 27*pi**2)*exp(4*z) + 4)*exp(2*z)*sin(3*pi*exp(z)/(exp(z) + 1)) + 3*pi**3*(exp(z) + 1)*(4*exp(6*z) + (24 + 27*pi**2)*exp(4*z) + 4)*exp(2*z) + pi**3*(-72*exp(6*z) + (-486*pi**2 - 432)*exp(4*z) - 72)*exp(3*z)/9)/(pi**3*(exp(z) + 1)**3*(4*exp(6*z) + 3*(8 + 9*pi**2)*exp(4*z) + 4))
  return result
