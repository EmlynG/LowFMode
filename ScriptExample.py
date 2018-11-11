## Class for PHOENIX with inbuilt plotting and scripting functions
## 11/11/2018 by Emlyn Graham (continuum plotting by Zhisong Qu)
##
## Usage:
##    python scriptname.py
##    or usable through the python interpreter interactively
## How to use:
##    - Import the PHOENIX class from PHOENIXscripts
##	from PHOENIXscripts import PHOENIX
##
##    - Create an instance of the class, giving it a location to save files
##	It assumes you are running from the phoenix directory
##	Optionally can define the location of the input, csp and eigenvector files also
##	PHOENIX(savelocation, inputfilelocation = None, omegafilelocation = None, eigenvectorfilelocation = None)
##
##
##    - Run plotting, scanning scripts as needed:
##	These include:
##
##		Run phoenix and csphoenix:
##		.run()
##		Need to do before plotting eigenvectors and gr/freq spectra
##
##		Frequency spectrum with/without target line:
##		.plot_freq(omegamin=None, omegamax=None, gammamin=None, gammamax=None, overplot=False, show=False)
##		.plot_freq_notarget(omegamin=None, omegamax=None, gammamin=None, gammamax=None, overplot=False, show=False)
##		Show: If True, displays plot, if False it saves the plot
##		Don't worry about the other inputs
##
##		Growth rate spectrum:
##		.plot_gr(omegamin=None, omegamax=None, gammamin=None, gammamax=None, show=False)
##
##		Plot eigenvector real/imaginary components:
##		.plot_eigen(value='v1', eigenvalue=None, show=False)
##		.plot_eigen_im(value='v1', eigenvalue=None, show=False)
##		Value is the component to plot out of ['p','v1','v2','v3','T','A1','A2','A3']
##		Eigenvalue is the integer numbered eigenvalue usually 0-14
##
##		Overplot frequency spectrum plots for different equilibria:
##		.overplot(list_of_equilibrium_filenames, saved_plot_name)
##		List of equilibrium files located in the INPUT folder in PHOENIX
##		and define a name for the plot to save
##
##		Target scan:
##		.scan(growth_rate_list,frequency_list)
##		Inputs are two lists, growth rates and frequencies to scan through
##



## Example:

from PHOENIXscripts import PHOENIX

example = PHOENIX('/SecondDisk/PHOENIX_RUNS/test/')

example.run()

example.plot_freq(show=True)

example.plot_freq_notarget(show=False)

example.plot_gr()

example.plot_eigen('v1', 2, show=False)

example.plot_eigen_im('v1', 2, show=True)

example.overplot(['NSTX1001','NSTXFITbase','NSTXbase'], 'testoverplot')

growthrates = [0.01,0.015,0.02]
frequencies = [0.25,0.26,0.27]
example.scan(growthrates,frequencies)
