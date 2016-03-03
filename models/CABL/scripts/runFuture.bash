#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH --mem=4GB
echo $HOST
cd /data/pak007/CABLE-2.0_EucFACE/offline/
cp ./out_EucFACE/PM/historical/restart_out.nc_1992-2011  ./restart_in.nc

cp cable_driver.F90_2012-2023  cable_driver.F90
cp cable_input.F90_2012-2023_soil7   cable_input.F90
./build.ksh

cp ./out_EucFACE/PM/future/AMBVAR/cable.nml .
./cable > out_EucFACE/PM/future/AMBVAR/log.txt
mv log_cable.txt  out_EucFACE/PM/future/AMBVAR/.
mv out_cable.nc   out_EucFACE/PM/future/AMBVAR/.
mv restart_out.nc out_EucFACE/PM/future/AMBVAR/.
mv D1CABLEUC_prelim.csv out_EucFACE/PM/future/AMBVAR/.
mv H1CABLEUC_30min.csv  out_EucFACE/PM/future/AMBVAR/.
mv litterInput.csv      out_EucFACE/PM/future/AMBVAR/.
mv sumgbh.txt           out_EucFACE/PM/future/AMBVAR/.

cp ./out_EucFACE/PM/future/AMBAVG/cable.nml .
./cable > out_EucFACE/PM/future/AMBAVG/log.txt
mv log_cable.txt  out_EucFACE/PM/future/AMBAVG/.
mv out_cable.nc   out_EucFACE/PM/future/AMBAVG/.
mv restart_out.nc out_EucFACE/PM/future/AMBAVG/.
mv D1CABLEUC_prelim.csv out_EucFACE/PM/future/AMBAVG/.
mv H1CABLEUC_30min.csv  out_EucFACE/PM/future/AMBAVG/.
mv litterInput.csv      out_EucFACE/PM/future/AMBAVG/.
mv sumgbh.txt           out_EucFACE/PM/future/AMBAVG/.

cp ./out_EucFACE/PM/future/ELEAVG/cable.nml .
./cable > out_EucFACE/PM/future/ELEAVG/log.txt
mv log_cable.txt  out_EucFACE/PM/future/ELEAVG/.
mv out_cable.nc   out_EucFACE/PM/future/ELEAVG/.
mv restart_out.nc out_EucFACE/PM/future/ELEAVG/.
mv D1CABLEUC_prelim.csv out_EucFACE/PM/future/ELEAVG/.
mv H1CABLEUC_30min.csv  out_EucFACE/PM/future/ELEAVG/.
mv litterInput.csv      out_EucFACE/PM/future/ELEAVG/.
mv sumgbh.txt           out_EucFACE/PM/future/ELEAVG/.

cp ./out_EucFACE/PM/future/ELEVAR/cable.nml .
./cable > out_EucFACE/PM/future/ELEVAR/log.txt
mv log_cable.txt  out_EucFACE/PM/future/ELEVAR/.
mv out_cable.nc   out_EucFACE/PM/future/ELEVAR/.
mv restart_out.nc out_EucFACE/PM/future/ELEVAR/.
mv D1CABLEUC_prelim.csv out_EucFACE/PM/future/ELEVAR/.
mv H1CABLEUC_30min.csv  out_EucFACE/PM/future/ELEVAR/.
mv litterInput.csv      out_EucFACE/PM/future/ELEVAR/.
mv sumgbh.txt           out_EucFACE/PM/future/ELEVAR/.

