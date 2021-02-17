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

NTRIES = 1000000     # Number of photons to simulate

print(' ')
print('Ray-tracing Monte Carlo with ',NTRIES,'test photons')
print(' ')

# All units in meters.
MEANX = 0.0
MEANY = 0.0
RMSX  = 1.0e-3          # Gaussian beam rms width in x [m]
RMSY  = 1.0e-3          # Gaussian beam rms width in y [m]
RMSXZ = 1.0e-3          # Beam divergence in x-z plane [rad]
RMSYZ = 1.0e-3          # Beam divergence in y-z plane [rad]

# Photo-detector position
XPD = 0.0
YPD = -2.5e-3

# Pendulum bob geometry
DBOB = 25.0e-3
RBOB = 0.5*DBOB  # approx 1 inch diameter
LBOB = 2.5       # length in meters
# Assume for now center of bob according to an angular displacement of D/2L
THETAB = RBOB/LBOB
DTH = [ -0.0005, -0.00045, -0.0004, -0.00035, -0.0003, -0.00025, -0.0002, -0.00015, -0.0001, -0.00005, 0.0,
         0.00005, 0.0001, 0.00015, 0.0002, 0.00025, 0.0003, 0.00035, 0.0004, 0.00045, 0.0005 ]
nbins = len(DTH)
print('Number of bins = ',nbins)

bobpos=[]
counters=[]
for x in range(nbins):
    THETABOB = THETAB + DTH[x]
    XBOB = LBOB*math.sin(THETABOB)
    YBOB = LBOB*(1.0-math.cos(THETABOB))
    bobpos.append([XBOB,YBOB,THETABOB])
    counters.append([0,0])
print('bobpos',bobpos)
print('counters',counters)

nsuccess = 0

# Generate uniform random numbers
for i in range(NTRIES):
# Generate laser photon  at z = 0
    x0 = NormalVariate(MEANX, RMSX)  # this function is in myrandom.py
    y0 = NormalVariate(MEANY, RMSY)  # this function is in myrandom.py
# Beam divergence
    dxdz = NormalVariate(0.0, RMSXZ)
    dydz = NormalVariate(0.0, RMSYZ)
# Extrapolate photon to z = 0.5 m (plane of bob motion)
    zbob = 0.50
    xb = x0 + dxdz*zbob
    yb = y0 + dydz*zbob
# Further extrapolate to photo-transistor plane at z = 1.0 m
    zpt = 1.0 
    xp = x0 + dxdz*zpt
    yp = y0 + dydz*zpt
    if i<10:
       print(i)
       print('Beam ',x0,y0)
       print('Bob  ',xb,yb)
       print('PT   ',xp,yp)
       print(' ')
# First independent of the bob position evaluate how many 
# generated photons intercept the photo-detector
# Keep track of number of photons hitting the photo-detector
# (ignoring position of the bob)
    lpd = False
    rsqp = (xp - XPD)**2 + (yp - YPD)**2
    if rsqp < 0.11e-6/3.14:          # Current PT has area of 0.11 mm^2 
       lpd = True
       nsuccess = nsuccess + 1

# Now loop through the bob positions
    for x in range(nbins):
        pos = bobpos[x]
#        print('Pos ',x,pos[0],pos[1])
        rsqb = (xb - pos[0])**2 + (yb - pos[1])**2
        lShadow = False
        if rsqb < RBOB*RBOB:
           lShadow = True
# Update appropriate counters
           counterx = counters[x]
# Independent of lpd increment the first counter for Shadow
           counterx[0] = counterx[0] + 1
           if lpd:
              counterx[1] = counterx[1] + 1
           counters[x] = counterx

print('Ntries       = ',NTRIES)
print('Nsuccesses   = ',nsuccess)
p0 = nsuccess/NTRIES
q0 = 1.0-p0
error0 = math.sqrt(p0*q0/NTRIES)
print('PT laser beam acceptance                = ',p0,'+-',error0)
print('counters',counters)

resultsfile = open("ResultsFile.dat", "w")
print('#  dtheta [rad],   non-shadow efficiency,    error',file=resultsfile) 
for x in range(nbins):
    print(' ')
    print('DTH = ',DTH[x])
    counterx = counters[x]
    print('Counter ',counterx)
    p1 = counterx[0]/NTRIES
    q1 = 1.0-p1
    error1 = math.sqrt(p1*q1/NTRIES)
    print('Bob shadow laser beam acceptance        = ',p1,'+-',error1)
    print('Bob non-shadow laser  acceptance        = ',q1,'+-',error1)

    p2 = counterx[1]/NTRIES
    q2 = 1.0-p2
    error2 = math.sqrt(p2*q2/NTRIES)
    print('Detected fraction (Bob shadow & PT)     = ',p2,'+-',error2)

    p3 = counterx[1]/nsuccess
    q3 = 1.0-p3
    error3 = math.sqrt(p3*q3/nsuccess)
    print('Shadow efficiency                       = ',p3,'+-',error3)
    print('Non-shadow efficiency                   = ',q3,'+-',error3)

    print(DTH[x],q3,error3,file=resultsfile)
resultsfile.close()

