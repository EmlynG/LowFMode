from __future__ import print_function

import sys
import os
import re
import numpy as np
import subprocess
from matplotlib import pyplot as plt

class PHOENIX:
	def __init__(self, saveloc, inputfile = None, omegafile = None, eigenfile = None):
		## Initialisation of class attributes (just a handy place to define file locations for use later)
		
		## Must define the directory to save plots to
		self.saveloc = str(saveloc)

		## Other file locations assume working in the base directory for PHOENIX, but can also define if needed)
		self.inputfile = os.path.join(os.getcwd(),'INPUT/phoenix.inp')
		if inputfile is not None:
			self.inputfile = inputfile
		self.omegafile = os.path.join(os.getcwd(),'OUTPUT/omega_csp')
		if omegafile is not None:
			self.omegafile = omegafile
		self.eigenfile = os.path.join(os.getcwd(),'OUTPUT/eigenvector.dat')
		if eigenfile is not None:
			self.eigenfile = eigenfile

	def run(self):
		subprocess.call(["csphoenix"])
		subprocess.call(["phoenix"])

	def plot_freq(self, omegamin=None, omegamax=None, gammamin=None, gammamax=None, overplot=False, show=False):
		
		## Plots frequency continuum with target frequency location

		# Plot the csphoneix continuum
		# 30/07/2018 by Zhisong Qu
		#
		# Inputs:
		#    csp_file  : the csp spectrum file name
		#    omega_min : the min omega to plot (default=-2.0)
		#    omega_max :     max               (default= 2.0)
		#    overplot  : True for component of overplot function (default=False)
		#    show      : display plot if True, save if False (default= False)

		## Define these y limits for the plot if needed

		# Number of variables (don't change)
		n_variable = 8
		# Number of output frequencies (don't change)
		n_multiplier = n_variable * 8
		filename = self.omegafile
		if omegamin is None:
		    omega_min = -2.0
		else:
		    omega_min = omegamin
		if omegamax is None:
		    omega_max = 2.0
		else:
		    omega_max = omegamax
		
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
		## Dont want separate plots if it is overplotting
		if overplot is False:		
			fig, ax = plt.subplots()
		plt.scatter(r, omega, s=1, marker='x')
		with open(self.inputfile, 'r') as inpfile:
				filecontents = inpfile.read()
				target = re.findall('\([^A]+\)',filecontents)[0]
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
		## Show if show is true, save if show is False and overplot is False
		if show is True:
			plt.show()
		elif overplot is False:
			plt.savefig(self.saveloc+"FREQCONTINUUM.png")


	def plot_freq_notarget(self,omegamin=None, omegamax=None, gammamin=None, gammamax=None, overplot=False, show=False, name = None):

		## Plots frequency continuum without target frequency location

		# Plot the csphoneix continuum
		# 30/07/2018 by Zhisong Qu
		#
		# Inputs:
		#    csp_file  : the csp spectrum file name
		#    omega_min : the min omega to plot (default=-2.0)
		#    omega_max :     max               (default= 2.0)
		#    overplot  : True for component of overplot function (default=False)
		#    show      : display plot if True, save if False (default= False)

		# Number of variables (don't change)
		n_variable = 8
		# Number of output frequencies (don't change)
		n_multiplier = n_variable * 8
		filename = self.omegafile
		if omegamin is None:
		    omega_min = -2.0
		else:
		    omega_min = omegamin
		if omegamax is None:
		    omega_max = 2.0
		else:
		    omega_max = omegamax
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
		if overplot is False:
			fig, ax = plt.subplots()		
			plt.scatter(r, omega, s=1, marker='x')
		elif overplot is True:
			plt.scatter(r, omega, s=1, marker='x', label=name)
		plt.xlim([np.min(r),np.max(r)])
		plt.xlabel('s')
		plt.ylim([omega_min,omega_max])
		plt.ylabel('$\omega / \omega_{A0}$')
		plt.title('Continuous Spectrum Frequency')
		if show is True:
			plt.show()
		elif overplot is False:
			plt.savefig(self.saveloc+"FREQCONTINUUM_notarget.png")

	def plot_gr(self,omegamin=None, omegamax=None, gammamin=None, gammamax=None, show=False):

		# Plot the csphoneix continuum
		# 30/07/2018 by Zhisong Qu
		#
		# Inputs:
		#    csp_file  : the csp spectrum file name
		#    gamma_min : the min gamma to plot (default=-0.1)
		#    gamma_max :     max               (default= 0.1)
		#    show      : display plot if True, save if False (default= False)


		# Number of variables (don't change)
		n_variable = 8
		# Number of output frequencies (don't change)
		n_multiplier = n_variable * 8
		filename = self.omegafile
		if gammamin is None:
		    gamma_min = -0.1
		else:
		    gamma_min = gammamin
		if gammamax is None:
		    gamma_max = 0.1
		else:
		    gamma_max = gammamax
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
		plt.scatter(r, gamma, s=1, marker='x')
		plt.xlim([np.min(r),np.max(r)])
		plt.xlabel('s')
		plt.ylim([gamma_min,gamma_max])
		plt.ylabel('$\gamma / \omega_{A0}$')
		plt.title('Continuous Spectrum Growth Rate')
		if show is True:
			plt.show()
		else:
			plt.savefig(self.saveloc+"GRCONTINUUM.png")

	def plot_eigen(self, value='v1', eigenvalue=None, show=False):
		
		# Plot phoenix eigenvector components (real)
		# 30/10/2018 by Emlyn Graham
		#
		# Inputs:
		#    value      : chosen component to plot (choose from ['p','v1','v2','v3','T','A1','A2','A3']
		#						, default 'v1')
		#    eigenvalue : eigenvalue number (choose from 0-14, default=0)
		#    show       : display plot if True, save if False (default= False)

		if value=='v1':
			dim = 'v1'
		else:
			dim = str(value)
		if eigenvalue is None:
			EV=0
		else:
			EV=eigenvalue
		filename = self.eigenfile
		with open(filename, 'rt') as f:	
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
			var = [[NEV_list[EV][i][M][dim_list.index(dim)][0] for i in range(0, len(NEV_list[EV]))] for M in range(0,MANZ,1)]
			fig, ax = plt.subplots()
			inputfile = os.path.join(os.getcwd(),'INPUT/phoenix.inp')
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
			for N in range(0,len(var)):	
				plt.plot(np.linspace(inner, outer, num=len(var[N])), var[N], label='M='+str(N+startingharmonic-np.floor((len(var)-1)/2)), marker=".", markersize=3, ls="")
			plt.xlabel('S')
			plt.ylabel('{}'.format(dim))
			plt.title('Re {} - EV {}'.format(dim, EV))
			plt.legend(loc='best')
			plt.autoscale(enable=True, axis="y", tight = False)
			if show is True:
				plt.show()
			else:
				plt.savefig(self.saveloc+dim+"_eig"+str(EV)+".png")
		
	def plot_eigen_im(self, value='v1', eigenvalue=None, show=False):
		# Plot phoenix eigenvector components (im)
		# 30/10/2018 by Emlyn Graham
		#
		# Inputs:
		#    value      : chosen component to plot (choose from ['p','v1','v2','v3','T','A1','A2','A3']
		#						, default 'v1')
		#    eigenvalue : eigenvalue number (choose from 0-14, default=0)
		#    show       : display plot if True, save if False (default= False)
		if value=='v1':
			dim = 'v1'
		else:
			dim = str(value)
		if eigenvalue is None:
			EV=0
		else:
			EV=eigenvalue
		filename = self.eigenfile
		with open(filename, 'rt') as f:	
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
			var = [[NEV_list[EV][i][M][dim_list.index(dim)][1] for i in range(0, len(NEV_list[EV]))] for M in range(0,MANZ,1)]
			fig, ax = plt.subplots()
			inputfile = os.path.join(os.getcwd(),'INPUT/phoenix.inp')
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
			for N in range(0,len(var)):	
				plt.plot(np.linspace(inner, outer, num=len(var[N])), var[N], label='M='+str(N+startingharmonic-np.floor((len(var)-1)/2)), marker=".", markersize=3, ls="")
			plt.xlabel('S')
			plt.ylabel('{}'.format(dim))
			plt.title('Im {} - EV {}'.format(dim, EV))
			plt.legend(loc='best')
			plt.autoscale(enable=True, axis="y", tight = False)
			if show is True:
				plt.show()
			else:
				plt.savefig(self.saveloc+dim+"_eig"+str(EV)+"_im.png")
		

	def overplot(self, equilibriumlist, plotname=None, show=False):
		# Plot phoenix eigenvector components (im)
		# 30/10/2018 by Emlyn Graham
		#
		# Inputs:
		#    equilibriumlist : list of equilibrium mapping files for PHOENIX
		#    plotname        : name of plot if saving (needs to be defined if saving)
		#    show            : display plot if True, save if False (default = False)
		#
		# Equilibrium mapping files need to be located in 'INPUT/' in PHOENIX directory
		print("Initialising")
		fig, ax = plt.subplots()
		## Taking turns to plot each
		for filename in equilibriumlist:
			## Rename the equilibrium file before running CSPHOENIX
			os.rename('INPUT/'+filename, 'INPUT/equilibrium.map')
			subprocess.call(["csphoenix"])
			os.rename('INPUT/equilibrium.map', 'INPUT/'+filename)
			## Add plot to the main plot
			self.plot_freq_notarget(overplot=True, name=filename)
		print("Done overplot!")
		plt.legend(loc='upper right')
		if plotname is not None:
			plt.savefig(self.saveloc+str(plotname)+".png")
		elif show is True:
			plt.show()

	def scan(self, grlist, freqlist):
		print("Initialising")

		## Looping through frequency and growth rate options to plot results
		savelocORIGINAL = self.saveloc
		subprocess.call(["csphoenix"])
		self.plot_freq_notarget()
		self.plot_gr()
		for freq1 in freqlist:
			freq = round(freq1, 3)
			for gr1 in grlist:
				gr = round(gr1, 3)
				self.saveloc = savelocORIGINAL +"GR"+str(round(gr,3))+"FREQ"+str(round(freq,3))
				with open(self.inputfile, 'r+') as inpfile:
					print("Reading old input file")

					## Reads input file and changes target value
					## PHOENIX changes the sign of the frequency input for some reason
					## so this is altered and files named correctly

					filecontents = inpfile.read()
					##target = re.findall('\([^A]+\)',filecontents)[0]
					newtarget = "("+str(gr)+"D+0, "+str(-freq)+"D+0)"
					inpfile.seek(0)
					inpfile.write(re.sub('\([^A]+\)', newtarget, filecontents, 1))
					print("Writing new input file")
					inpfile.truncate()
					inpfile.close()
			
					## Call csphoenix and phoenix to produce outputs

					subprocess.call(["phoenix"])
					print("Continuum plots done") 
					plt.close("all")
					dim_list = ['p', 'v1', 'v2', 'v3', 'T', 'A1', 'A2', 'A3']
					for dim in dim_list:
						evnum = 1
						EVs = os.path.join(os.getcwd(),'OUTPUT/eigenvalues.dat')
						with open(EVs, 'r') as evdata:
							for i, l in enumerate(evdata):
								pass
							evnum = i+1
							evdata.close()
						for EV in list(range(evnum)):
							try:
								self.plot_eigen(value=dim,eigenvalue=EV)
								plt.close("all")			
							except IndexError:
								pass
							try:
								self.plot_eigen_im(value=dim,eigenvalue=EV)
								plt.close("all")
							except IndexError:
								pass
							plt.close("all")
					print("Eigenvector plots done")
		self.saveloc = savelocORIGINAL
		print("DONE!")


#############################################################################
