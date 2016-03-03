# Using models to guide field experiments: a priori predictions for the CO<sub>2</sub> response of a nutrient- and water-limited native Eucalypt woodland.

Medlyn, B. E., De Kauwe, M. G., Zaehle, S., Walker, A. P., Duursma, R. A., Luus, K., Mishurov, M., Pak, B., Smith, B., Wang, Y.-P., Yang, X., Crous, K., Drake, J. E., Gimeno, T. E., Macdonald, C. A., Norby, R. J., Power, S. A., Tjoelker, M. G., Ellsworth, D. S. *Global Change Biology*, 2016, in press.

[![DOI](https://zenodo.org/badge/15813/mdekauwe/EucFACE_Baseline_paper.svg)](https://zenodo.org/badge/latestdoi/15813/mdekauwe/EucFACE_Baseline_paper)

## Overview ##

Repository containing all the model code (where possible) and associated scripts required to reproduce simulations our Global Change Biology paper.

A DOI will appear here soon...

## Model code ##
For some models it is not possible to share code due to ownership issues, e.g. O-CN. In these cases, models have set up their own repositories and the relevant model sub-directories contains README files which point to these stored repositories.

## Model checking scripts ##
The top-level scripts directory contains the model checking scripts (check_model_output.py; check_model_output_AVG.py) to make sure post-processed outputs are sensible. There is also a script (generate_pickled_model_output.py) to generate a big ([pandas](http://pandas.pydata.org/)) dataframe and then turn this into a binary object to allow easy access of all of the model output inside a script. Not the checking script require this binary object to be built first.


## Contacts
- Belinda Medlyn: B.Medlyn at uws.edu.au
- Martin De Kauwe: mdekauwe at gmail.com
