# GDAY simulations

Author:
Martin De Kauwe

Date:
Sat Jul 25 20:12:23 2015 +1000

## Overview ##
All the code, pre- and post- processing scripts required to remake the GDAY sims
for the EucFACE paper.

- Source files are from the EucFACE_simulation branch, but can also be found in the github repository. I tagged a version.
- tag: v1.0-eucface_sim
- commit: f78102d9c4857e2a2f03fafed8f19f531fbeb599

## To recreate runs ##

###### Compile GDAY executable ######

```bash
cd src
make #obviously assumes you have a C compiler installed
```
###### Re-create the meteorological forcing files ######

```bash
cd met_data
python generate_FORCING_files.py
```
###### Re-run the simulations ######
```bash
cd simulations
python eucface_spinup_to_equilibrium.py
python eucface_simulations.py
```

The outputs directory will then contain the four CSV files with the relevant model runs (ambient/elevated, fixed/variable)

## Dependancies ##

To compile GDAY you will need a C compiler, any will do, GDAY itself has no furhter dependancies.

Just for the record the version used in these runs was:

```bash
$ gcc --version
Configured with: --prefix=/Applications/Xcode.app/Contents/Developer/usr --with-gxx-include-dir=/usr/include/c++/4.2.1
Apple LLVM version 6.1.0 (clang-602.0.49) (based on LLVM 3.6.0svn)
Target: x86_64-apple-darwin14.4.0
Thread model: posix
```

The post-processing scripts depend on a few general python libraries:

- Numpy (version: 1.9.2)
- Matplotlib (version: 1.4.3)
- Pandas (version: 0.16.0).

These simulations could easily be recreated without these libraries, i.e. as no plots are made, the matplotlib call is superfluous. The Pandas one is just to read a CSV file, so this could be replaced by some trivial file parsing code. The numpy code uses the the random generator to shuffle years.
