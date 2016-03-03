#!/bin/bash
#SBATCH --time=03:30:00
#SBATCH --mem=4GB
echo $HOST
cd /data/pak007/CABLE-2.0_EucFACE/offline/
cp ./out_EucFACE/runoff/spin/restart_899.nc  ./restart_in.nc
#cp ./out_EucFACE/PM/spin/cable.nml .

cp cable_driver.F90_spin cable_driver.F90
cp cable_input.F90_1750-2011_soil7 cable_input.F90
./build.ksh

decade=90
while [ $decade -le 119 ]
do
  runcount=`expr $decade \* 10`
  runstop=`expr $runcount + 9`
  while [ $runcount -le `expr $runstop` ]
  do
    ./cable > log.txt
    mv log_cable.txt  out_EucFACE/PM/spin/log_cable${runcount}.txt
    mv log.txt        out_EucFACE/PM/spin/log${runcount}.txt
    mv out_cable.nc   out_EucFACE/PM/spin/out_cable${runcount}.nc
    cp -p restart_out.nc  restart_in.nc
    mv restart_out.nc out_EucFACE/PM/spin/restart_${runcount}.nc
    runcount=`expr $runcount + 1`
  done
  mv out_EucFACE/PM/spin/* /datastore/cmar/pak007/CABLE-2.0_EucFACE/out_EucFACE/PM/spin/.
  decade=`expr $decade + 1`
done

