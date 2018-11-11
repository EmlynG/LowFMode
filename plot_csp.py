# Plot the csphoneix continuum
# 30/07/2018 by Zhisong Qu
#
# Usage:
#    python plot_csp.py csp_file omega_min omega_max gamma_min gamma_max
# Inputs:
#    csp_file  : the csp spectrum file name
#    omega_min : the min omega to plot (default=-2.0)
#    omega_max :     max               (default= 2.0)
#    gamma_min : the min gamma to plot (default=-0.1)
#    gamma_max :     max               (default= 0.1)

from __future__ import print_function

import sys
import os
import re

import numpy as np
from matplotlib import pyplot as plt

# Number of variables (don't change)
n_variable = 8
# Number of output frequencies (don't change)
n_multiplier = n_variable * 8

if len(sys.argv) < 2:
    filename = 'omega_csp'
else:
    filename = sys.argv[1]
if len(sys.argv) < 3:
    omega_min = -2.0
else:
    omega_min = float(sys.argv[2])
if len(sys.argv) < 4:
    omega_max = 2.0
else:
    omega_max = float(sys.argv[3])
if len(sys.argv) < 5:
    gamma_min = -0.1
else:
    gamma_min = float(sys.argv[4])
if len(sys.argv) < 6:
    gamma_max = 0.1
else:
    gamma_max = float(sys.argv[5])


with open(filename, 'r') as f:
    line = f.readline()
    [m, nr] = map(int, line.split())
    print('M  = ', m)
    print('NR = ', nr)

    n_output = m * n_multiplier * nr
    r = np.zeros(n_output)
    q = np.zeros(n_output)
    gamma = np.zeros(n_output)
    omega = np.zeros(n_output)
    
    i = 0
    for line in f:
        [rf, qf, omegaf, gammaf] = map(float, line.split())
        #print(rf, qf, gammaf, omegaf)
        r[i] = rf
        q[i] = qf
        gamma[i] = gammaf
        omega[i] = omegaf
        i = i + 1
        
fig, ax = plt.subplots()
plt.scatter(r, omega, s=1, marker='x')
if len(sys.argv) < 2:
		inputfile = os.path.join(os.path.realpath('..'),'INPUT/phoenix.inp')
else:
		inputfile = os.path.join(os.path.split(os.path.split(filename)[0])[0],'INPUT/phoenix.inp')
with open(inputfile, 'r') as inpfile:
		filecontents = inpfile.read()
		target = re.findall('\([^A]+\)',filecontents)[0]
		#target = re.search('\([^A]+\)',filecontents)
		#print(target.group())
		val, power = (target[1:-1].split(',')[1]).split('D')
		val, power = float(str(val).strip()), float(str(power).strip())
		freq = val*pow(10.0,power)
		plt.plot([np.min(r),np.max(r)],[-freq,-freq],"r--")
		plt.text(0.1, 0.05, '-- Target', ha='center', va='center', transform=ax.transAxes, fontsize=8, color = 'r')
plt.xlim([np.min(r),np.max(r)])
plt.xlabel('s')
plt.ylim([omega_min,omega_max])
plt.ylabel('$\omega / \omega_{A0}$')
plt.title('Continuous Spectrum Frequency')
#plt.show()
    
plt.figure()
plt.scatter(r, gamma, s=1, marker='x')
plt.xlim([np.min(r),np.max(r)])
plt.xlabel('s')
plt.ylim([gamma_min,gamma_max])
plt.ylabel('$\gamma / \omega_{A0}$')
plt.title('Continuous Spectrum Growth Rate')
plt.show()
