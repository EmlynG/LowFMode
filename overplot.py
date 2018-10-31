from __future__ import print_function

import sys
import os
import re
import numpy as np
import subprocess
from matplotlib import pyplot as plt
inputpath = os.path.join(os.path.realpath('..'),'INPUT/')
print("Initialising")
fig, ax = plt.subplots()
n=0
for filenum in ['INPUT/0.txt','INPUT/1.txt','INPUT/2.txt']:
	os.rename(filenum, 'INPUT/equilibrium.map')
	subprocess.call(["csphoenix"])
	os.rename('INPUT/equilibrium.map', filenum)
	n_variable = 8
	n_multiplier = n_variable * 8
	omegafile = 'OUTPUT/omega_csp'
	omega_min = -2.0
	omega_max = 2.0
	gamma_min = -0.1
	gamma_max = 0.1
	with open(omegafile, 'r') as f:
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
					f.close()	

	plt.scatter(r, omega, s=0.5, marker='x', label='flow='+str(n))
	n=n+1
	inner = 0.0
	outer = 1.0
## NAME THE OUTPUT FILES						
	plt.xlim([np.min(r),np.max(r)])
	plt.xlabel('s')
	plt.ylim([omega_min,omega_max])
	plt.ylabel('$\omega / \omega_{A0}$')
	ax.legend()
	plt.title('Continuous Spectrum Frequency')
	plt.figure()
plt.show()
#inner = 0.0
#outer = 1.0
## NAME THE OUTPUT FILES						
#plt.xlim([np.min(r),np.max(r)])
#plt.xlabel('s')
#plt.ylim([omega_min,omega_max])
#plt.ylabel('$\omega / \omega_{A0}$')
#ax.legend()
#plt.title('Continuous Spectrum Frequency')
#plt.savefig("/SecondDisk/PHOENIX_RUNS/NSTX/OVERPLOTnumeric012.png")
#print("Frequency continuum plot done") 
