# Circles.py
#
# Ray-tracing MC to check laser/bob/photo-transistor 
#                         mis-alignment scenarios/tolerances
#
import random
import math
import matplotlib.pyplot as plot
import numpy as np
from myrandom import *

# Initialize the random number generator using specified seed
SEED = 203
random.seed(SEED)

NTRIES = 100000     # Number of photons to simulate

# In millimeters.
MEANX = 0.0
MEANY = 0.0
RMSX  = 1.0          # Gaussian beam rms width in x 
RMSY  = 1.0          # Gaussian beam rms width in y
RMSXZ = 1.0e-3       # Beam divergence in x-z plane 
RMSYZ = 1.0e-3       # Beam divergence in y-z plane

# Photo-detector position
XPD = 0.0
YPD = 0.0

# Pendulum bob geometry
RBOB = 25.4/2.0  # 1 inch diameter
LBOB = 500.0     # 0.5 m
# Assume for now center of bob according to an angular displacement of D/2L
THETAB = RBOB/LBOB
DTH = [ -0.0005, -0.0004, -0.0003, -0.0002, -0.0001, 0.0, 0.0001, 0.0002, 0.0003, 0.0004, 0.0005 ]
THETABOB = THETAB - 0.0002
XBOB = LBOB*math.sin(THETABOB)
YBOB = LBOB*(1.0-math.cos(THETABOB))

print('XBOB, YBOB = ',XBOB,YBOB)

nsuccess0 = 0
nsuccess1 = 0
nsuccess2 = 0

# Generate uniform random numbers
for i in range(NTRIES):
# Generate laser photon  at z = 0
    x0 = NormalVariate(MEANX, RMSX)  # this function is in myrandom.py
    y0 = NormalVariate(MEANY, RMSY)  # this function is in myrandom.py
# Beam divergence
    dxdz = NormalVariate(0.0, RMSXZ)
    dydz = NormalVariate(0.0, RMSYZ)
# Extrapolate photon to z = 0.5 m (plane of bob motion)
    zbob = 0.50*1000.0
    xb = x0 + dxdz*zbob
    yb = y0 + dydz*zbob
# Further extrapolate to photo-transistor plane at z = 1.0 m
    zpt = 1.0*1000.0 
    xp = x0 + dxdz*zpt
    yp = y0 + dydz*zpt
    if i<100:
       print(i)
       print('Beam ',x0,y0)
       print('Bob  ',xb,yb)
       print('PT   ',xp,yp)
       print(' ')
# Does the photon miss the bob?
    rsqb = (xb - XBOB)**2 + (yb - YBOB)**2
    if rsqb > RBOB*RBOB:
       nsuccess1 = nsuccess1 + 1
# Keep track of number of photons hitting the photo-detector
# (ignoring position of the bob)
    rsqp = (xp - XPD)**2 + (yp - YPD)**2
    if rsqp < 0.11/3.14:
       nsuccess0 = nsuccess0 + 1
       if rsqb > RBOB*RBOB:          # for those missing the bob
          nsuccess2 = nsuccess2 + 1

print('Ntries       = ',NTRIES)
print('Nsuccesses 0 = ',nsuccess0)
print('Nsuccesses 1 = ',nsuccess1)
print('Nsuccesses 2 = ',nsuccess2)
p0 = nsuccess0/NTRIES
q0 = 1.0-p0
error0 = math.sqrt(p0*q0/NTRIES)
print('PT laser beam acceptance                = ',p0,'+-',error0)

p1 = nsuccess1/NTRIES
q1 = 1.0-p1
error1 = math.sqrt(p1*q1/NTRIES)
print('Bob shadow laser beam acceptance        = ',q1,'+-',error1)
print('Bob non-shadow laser  acceptance        = ',p1,'+-',error1)

p2 = nsuccess2/NTRIES
q2 = 1.0-p2
error2 = math.sqrt(p2*q2/NTRIES)
print('Detected fraction (Bob non-shadow & PT) = ',p2,'+-',error2)

p3 = nsuccess2/nsuccess0
q3 = 1.0-p3
error3 = math.sqrt(p3*q3/nsuccess0)
print('Shadow efficiency                       = ',q3,'+-',error3)
print('Non-shadow efficiency                   = ',p3,'+-',error3)

