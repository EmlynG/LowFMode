import sys
import numpy as np
import os
import re
import matplotlib.pyplot as plt

filename = sys.argv[1]
with open(filename, 'rt') as f:
	dim = str(sys.argv[2])
	EV = 0	
	if sys.argv[3]:	
		EV = int(sys.argv[3])	
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
		plt.plot(np.linspace(inner, outer, num=len(var[N])), var[N], label='M='+str(N+startingharmonic), marker=".", markersize=3, ls="")
	plt.xlabel('S')
	plt.ylabel('{}'.format(dim))
	plt.title('Re {} component for eigenvalue {}'.format(dim, EV))
	plt.legend(loc='best')
	plt.autoscale(enable=True, axis="y", tight = False)
	#plt.ylim(-0.0005, 0.0015)
	plt.show()

