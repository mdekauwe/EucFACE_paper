############################
#
# readme for CLM output 
# Anthony Walker
# Sept 2013
#
############################

Output files for the CO2 simulations and AVG VAR climate at EucFACE
############################

Files created according to the EucFACE protocol 'EucFACE_output_protocol.docx'

The CLM output varies from the EucFACE protocol as follows:
- 1 additional variable in col 81: potential GPP prior to N downregulation
- the conductance outputs (cols 77-79) are 24hr averages not daytime averages
- APAR is in mol m-2 d-1

I'm somewhat suspicious of the conductance outputs (cols 77-79) but haven't as yet had a chance to check them properly.    


Notes
###########################

protocol        'EucFACE_modelling_protocol.doc'
metdata file    'EucFACE_forcing_1949-2008_ALMA_corrected.nc' 'EucFACE_forcing_2012-2023_AMBAVG_ALMA.nc' 'EucFACE_forcing_2012-2023_AMBVAR_ALMA.nc'
parameter file  'EucFACE_Params_V2.pdf' and Ball-Berry stomatal conductance parameter from 'EucFACE_stomatal_conductance_params.txt' 

Soil sand contant 80%

Modified CLM rooting distribution so that >96% of the roots are above 2.29m deep.

Fixed outputs - PAR, T/EC, soil water is now plant available water (mm above wilting point)
              - APAR and potential GPP also fixed

N deposition is now taken from the correct driving data.
     
Fixed allocation to be 1:1:1 leaf:fine root:wood (inc. coarse root)

Corrected CO2 driving data, there is still a small error where the CO2 increase is delayed by 1.5 days. This doesn't seem to be a problem in the input file, 
I think it's something to do with the way CLM reads the input file, let me know if it's a problem and I'll try to fix it.



