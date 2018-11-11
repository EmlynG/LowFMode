from __future__ import print_function

import sys
import os
import re
import numpy as np
import subprocess
from matplotlib import pyplot as plt
#inputfile = os.path.join(os.path.realpath('..'),'INPUT/phoenixORIG.inp')
saveloc = "/SecondDisk/PHOENIX_RUNS/NSTX/SPLINE_TARGET_SCAN/"
print("Initialising")
fileout = os.path.join(os.getcwd(),'INPUT/phoenix.inp')
#freqlist = list(np.arange(0.260, 0.4, 0.01))+list(np.arange(-0.4, -0.260, 0.01))
freqlist = list(np.arange(-0.4, -0.260, 0.01))
grlist = list(np.arange(0.05, 0.1, 0.05))+list(np.arange(-0.1, -0.05, 0.05))
#freqlist = [0.27]
#grlist = [0.02]
for freq1 in freqlist:
	freq = round(freq1, 3)
	for gr1 in grlist:
		gr = round(gr1, 3)	
		with open(fileout, 'r+') as outputfile:
			print("Reading old input file")
			filecontents = outputfile.read()
			##target = re.findall('\([^A]+\)',filecontents)[0]
			newtarget = "("+str(gr)+"D+0, "+str(-freq)+"D+0)"
			outputfile.seek(0)
			outputfile.write(re.sub('\([^A]+\)', newtarget, filecontents, 1))
			print("Writing new input file")
			outputfile.truncate()
			outputfile.close()
			
			subprocess.call(["csphoenix"])
			subprocess.call(["phoenix"])
			#sys.stdout.write("csphoenix")
			#sys.stdout.write("phoenix")	

			# Number of variables (don't change)
			n_variable = 8
			# Number of output frequencies (don't change)
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
				
			fig, ax = plt.subplots()
			plt.scatter(r, omega, s=1, marker='x')
			if len(sys.argv) < 2:
				inputfile = os.path.join(os.getcwd(),'INPUT/phoenix.inp')
			else:
				inputfile = os.path.join(os.path.split(os.path.split(filename)[0])[0],'INPUT/phoenix.inp')
			inner = 0.0
			outer = 1.0
			startingharmonic = 1
			with open(inputfile, 'r') as inpfile:
				filecontents = inpfile.read()
				rfour = re.findall("(?<==)[^A]+(?=NTOR)", filecontents)[0]
				rfourval, rfourpower = re.findall("[^DE]+",rfour)
				rfourval, rfourpower = float(str(rfourval).strip()), float(str(rfourpower).strip())
				startingharmonic = int(rfourval*10**rfourpower)
				nvalue = re.findall("(?<==)[^ADE]+(?=MANZ)", filecontents)[0]
				nval = float(str(nvalue).strip())
				if nval >= 0:
					nvalue = 1
				elif nval < 0:
					nvalue = -1
				innerlim = re.findall("(?<==)[^A]+(?=OUTER_WALL)", filecontents)[0]
				innerlimval, innerlimpower = re.findall("[^DE]+",innerlim)
				innerlimval, innerlimpower = float(str(innerlimval).strip()), float(str(innerlimpower).strip())
				inner = innerlimval*10**innerlimpower
				outerlim = re.findall("(?<==)[^A]+(?=MESH_ACCUMULATION)", filecontents)[0]
				outerlimval, outerlimpower = re.findall("[^DE]+",outerlim)
				outerlimval, outerlimpower = float(str(outerlimval).strip()), float(str(outerlimpower).strip())
				outer = outerlimval*10**outerlimpower
				target = re.findall('\([^A]+\)',filecontents)[0]
				val, power = (target[1:-1].split(',')[1]).split('D')
				val, power = float(str(val).strip()), float(str(power).strip())
				freq = val*pow(10.0,power)
				plt.plot([np.min(r),np.max(r)],[nvalue*freq,nvalue*freq],"r--")
				plt.text(0.1, 0.05, '-- Target', ha='center', va='center', transform=ax.transAxes, fontsize=8, color = 'r')
				inpfile.close()
			## NAME THE OUTPUT FILES
			prefix = "ROT2_N"+str(nval)+"_M1_GR"+str(round(gr,3))+"FREQ"+str(round(-freq,3))							
			plt.xlim([np.min(r),np.max(r)])
			plt.xlabel('s')
			plt.ylim([omega_min,omega_max])
			plt.ylabel('$\omega / \omega_{A0}$')
			plt.title('Continuous Spectrum Frequency')
			#plt.show()
			plt.savefig(saveloc+"FREQCONT"+prefix+".png")
			print("Frequency continuum plot done")    
			plt.figure()
			plt.scatter(r, gamma, s=1, marker='x')
			plt.xlim([np.min(r),np.max(r)])
			plt.xlabel('s')
			plt.ylim([gamma_min,gamma_max])
			plt.ylabel('$\gamma / \omega_{A0}$')
			plt.title('Continuous Spectrum Growth Rate')
			
			plt.savefig(saveloc+"GRCONT"+prefix+".png")
			print("Growth rate continuum plot done") 
			#plt.show()
			plt.close("all")
			with open("OUTPUT/eigenvector.dat", 'rt') as f:
					dim_list = ['p', 'v1', 'v2', 'v3', 'T', 'A1', 'A2', 'A3']
					dataset = [[str(entry).strip() for entry in line.split()] for line in f.readlines()]
					[NEV, NR, MANZ, MDIF] = [int(str(entry).strip()) for entry in dataset[0]]
					dataset.pop(0);
					NEV_list = [dataset[i:i+NR] for i in range(0, len(dataset), NR)]
					NEV_list = [[[NRx[i:i+16] for i in range(0, len(NRx), 16)] for NRx in N] for N in NEV_list]
					NEV_list = [[[[entry[i:i+2] for i in range(0, len(entry), 2)] for entry in NRx] for NRx in N] for N in NEV_list]
					NEV_list = [[[[[float(x) for x in re_im] for re_im in dims] for dims in M] for M in N] for N in NEV_list]
					# Now we have a dataset of the form [re,im] for each [p,v1,v2,...] for each [1,...,MANZ] for each [1,...,NR] for each [1,...,NEV]
					# As a nested list
					for dim in dim_list:
						evnum = 1
						EVs = os.path.join(os.getcwd(),'OUTPUT/eigenvalues.dat')
						with open(EVs, 'r') as evdata:
							for i, l in enumerate(evdata):
								pass
							evnum = i+1
						for EV in list(range(evnum)):
							try:
								var = [[NEV_list[EV][i][M][dim_list.index(dim)][0] for i in range(0, len(NEV_list[EV]))] for M in range(0,MANZ,1)]
								fig, ax = plt.subplots()
								for N in range(0,len(var)):	
									plt.plot(np.linspace(inner, outer, num=len(var[N])), var[N], label='M='+str(N+startingharmonic-np.floor((len(var)-1)/2)), marker=".", markersize=3, ls="")
								plt.xlabel('S')
								plt.ylabel('{}'.format(dim))
								plt.title('{} Re component for eigenvalue {}'.format(dim, EV))
								plt.legend(loc='best')
								plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
								plt.autoscale(enable=True, axis="y", tight = False)
								#plt.ylim(-0.0005, 0.0015)
								plt.savefig(saveloc+"EIGV_"+str(EV)+"DIM_"+str(dim)+"_"+prefix+"re.png")
								#plt.show()
								plt.close("all")
								print("EV " + str(EV) + " " + str(dim)+" re plot done")
							except IndexError:
								pass
							try:
								var = [[NEV_list[EV][i][M][dim_list.index(dim)][1] for i in range(0, len(NEV_list[EV]))] for M in range(0,MANZ,1)]
								fig, ax = plt.subplots()
								for N in range(0,len(var)):	
									plt.plot(np.linspace(inner, outer, num=len(var[N])), var[N], label='M='+str(N+startingharmonic-np.floor((len(var)-1)/2)), marker=".", markersize=3, ls="")
								plt.xlabel('S')
								plt.ylabel('{}'.format(dim))
								plt.title('Im {} component for eigenvalue {}'.format(dim, EV))
								plt.legend(loc='best')
								plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
								plt.autoscale(enable=True, axis="y", tight = False)
								#plt.ylim(-0.0005, 0.0015)
								plt.savefig(saveloc+"EIGV_"+str(EV)+"DIM_"+str(dim)+"_"+prefix+"im.png")
								#plt.show()
								plt.close("all")
								print("EV " + str(EV) + " " + str(dim)+" im plot done")
							except IndexError:
								pass
						plt.close("all")
						evdata.close()
					plt.close("all")
					print("Eigenvector plots done") 
					f.close()
			outputfile.close()




print("DONE!")
							
