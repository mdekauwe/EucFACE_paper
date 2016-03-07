# OCN simulations

Author:
Soenke Zaehle

## Overview ##
Final code, results, inputs and run-scripts for the OCN EucFACE runs on MPI
BGI's server, under

~/kluus/SZ/EucFACE_final_Aug22/

which contains the following subdirectories:

Code_Rev156  Inputs  Postprocessing  Processed  Results Runcontrol

The EucFACE runs were conducted using version 156 of the code on Subversion.
(Sidenote: I named this version 155 in my files, but the name ended up being
156 on Subversion since Martina submitted code to SVN between my versions 154
and 156). Model runs were generated allowing shading death to occur, and using
CI* to calculate photosynthesis. Postprocessing was conducted
using 'pp_eucface.f90', followed by 'convert_to_annual_EucFACE3.R'

The final results submitted on Aug 22 used the CI function, as can be seen in
'runs2postprocess.txt', which has not been modified since Aug 22 2014
(10 mins before the final output was created). Later model runs were not
postprocessed. I've copied over the CI .nc output files from rev155ci to
~/SZ/EucFACE_final_Aug22/Results
