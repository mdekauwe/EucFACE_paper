# CABLE simulations

Author:
Bernard Pak

## Overview ##

The CABLE code is based on my branch at revision 2164. The codes I/O had been
modified to read in the supplied met forcing directly and output the required
text files for EucFACE submission. Further hacking to the code aims at
overwriting some default parameters with the EucFACE supplied parameters
although some of these were done in the input parameter files when possible
(veg_params_cable_MK3L_v2.txt_EucFACE, pftlookup_csiro_v16_17tiles.csv_EucFACE).

During analysis of the first submission, a bug was found pointing to the
incomplete implementation of the Lai&Ktaul method. A fix had been added to this
code. Please note that this fix may not be exactly the same when finally ported
to the trunk version later on.

Also please note that the Penman Monteith Method was used throughout this
exercise and, when not specified by EucFACE, the other soil parameters follow
that of soil 7.

************************************

CABLE has gone open-sourced since April 2015. To register and download the
codes please visit https://trac.nci.org.au/trac/cable/wiki/CableRegistration

************************************

The sub-directories core and offline contains the actual codes (the global
online interface has been excluded from this submission) with compilation
done by the script
	offline/build.ksh
which has flexibility to work on new platforms.
The sub-directory inputFiles contains the input files including the namelists
and restart files. However, the EucFACE supplied inputs are not included.
The sub-directory scripts contains the run scripts that run the experiment
during the spinning stage, the historical period and the future scenarios.
There are also post-processing scripts here to make the output as required
by EucFACE submission.

To run the scripts, beware to modify the head-directory first.

Please note that CABLE is mainly tested on UNIX/LINUX systems using
Intel Fortran compilers.
