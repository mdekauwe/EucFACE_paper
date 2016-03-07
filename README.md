# Using models to guide field experiments: a priori predictions for the CO<sub>2</sub> response of a nutrient- and water-limited native Eucalypt woodland.

[Belinda E. Medlyn](https://bmedlyn.wordpress.com/),
[Martin G. De Kauwe](https://mdekauwe.github.io/),
[Soenke Zaehle](https://www.bgc-jena.mpg.de/bgi/index.php/People/SoenkeZaehle),
[Anthony Walker](https://climatechangescience.ornl.gov/content/anthony-p-walker),
[Remko A. Duursma](http://www.remkoduursma.com/)
Kristina Luus,
[Michael M. Mishurov](http://web.nateko.lu.se/Personal/Michael.Mischurow/),
Bernard Pak,
[Ben Smith](http://web.nateko.lu.se/personal/benjamin.smith/frames.html),
Ying-Ping Wang,
Kristine Crous,
John G. Drake,
T. E. Gimeno,
C. A. Macdonald,
[R. J. Norby](http://web.ornl.gov/~rjn/),
S. A. Power,
M. Tjoelker,
D. S. Ellsworth.

*Global Change Biology*, 2016, in press.


## Overview ##

Repository containing all the model code (where possible) and associated scripts required to reproduce simulations our Global Change Biology paper.

A DOI will appear here soon...

## Meteorolgical data ##
The [met_data](met_data) folder contains all the raw data given to modellers to run the 4 experiments used carried out in the paper. Note this directory has some large files in it (>50 meg).

## Model code ##
For some models it is not possible to share code due to ownership issues, e.g. O-CN. In these cases, models have set up their own repositories and the relevant model sub-directories contains README files which point to these stored repositories.

## Model checking scripts ##
The top-level scripts directory contains the model checking scripts (check_model_output.py; check_model_output_AVG.py) to make sure post-processed outputs are sensible. There is also a script (generate_pickled_model_output.py) to generate a big ([pandas](http://pandas.pydata.org/)) dataframe and then turn this into a binary object to allow easy access of all of the model output inside a script. Note the checking script require this binary object to be built first.

## Model outputs ##
Model outpus are each of the model/outputs sub-directories, e.g. [GDAY](models/GDAY/outputs).

## Contacts
- Belinda Medlyn: B.Medlyn at westernsydney.edu.au
- Martin De Kauwe: mdekauwe at gmail.com
