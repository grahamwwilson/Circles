#
# Basic plotting program based on 
# https://github.com/grahamwwilson/fits-516
# 
from matplotlib import pyplot as plt
import numpy as np
from pylab import *
from scipy import stats
from iminuit import Minuit
from iminuit.util import describe, make_func_code
from pprint import pprint

# Read data from file into numpy array format
file1='ResultsFile_Aligned.dat'
x_data, y_data, y_err = genfromtxt(file1, usecols=(0,1,2),unpack=True)

file2='ResultsFile_MisalignedVN.dat'
x_data2, y_data2, y_err2 = genfromtxt(file2, usecols=(0,1,2),unpack=True)

file3='ResultsFile_MisalignedVP.dat'
x_data3, y_data3, y_err3 = genfromtxt(file3, usecols=(0,1,2),unpack=True)

# Change to mrad 
x_data = 1000.0*x_data
x_data2 = 1000.0*x_data2
x_data3 = 1000.0*x_data3

# Add some plotting customization
SMALL_SIZE = 20
MEDIUM_SIZE = 26
BIGGER_SIZE = 32
plt.rc('font', size=MEDIUM_SIZE)         # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

# Plot the data with assigned errors
plt.figure(1)    

errorbar(x_data2,y_data2,color='red',linewidth=2, label=r'Mis-Aligned PT, $\Delta y=-2.5$mm')
errorbar(x_data2,y_data2,y_err2,fmt="o",color='red',solid_capstyle='projecting',capsize=0,markersize=4)

errorbar(x_data,y_data,color='blue',linewidth=2, label="Aligned PT")
errorbar(x_data,y_data,y_err,fmt="o",color='blue',solid_capstyle='projecting',capsize=0,markersize=4)

errorbar(x_data3,y_data3,color='green',linewidth=2, label=r'Mis-Aligned PT, $\Delta y=2.5$mm')
errorbar(x_data3,y_data3,y_err3,fmt="o",color='green',solid_capstyle='projecting',capsize=0,markersize=4)

title('Laser Acceptance')
xlabel(r'$\Delta \theta$ [mrad]')
ylabel('Relative Detection Efficiency')
plt.grid(True)
plt.legend()
plt.text(-0.50,0.60,r'$\sigma_{x,y} = $1 mm')
plt.text(-0.50,0.52,r'$\sigma_{x^{\prime},y^{\prime}} =  $1 mrad')
plt.text(0.25,0.3,r'D=2.5cm')
plt.text(0.25,0.22,r'L=2.5m')
plt.text(0.25,0.14,r'$\theta_{0} = 5.0$ mrad') 
plt.show()
