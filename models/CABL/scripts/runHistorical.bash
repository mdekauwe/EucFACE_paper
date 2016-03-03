#!/bin/bash
#SBATCH --time=01:30:00
#SBATCH --mem=4GB
echo $HOST
cd /data/pak007/CABLE-2.0_EucFACE/offline/
cp ./out_EucFACE/PM/spin/restart_1199.nc  ./restart_in.nc
cp ./out_EucFACE/PM/historical/cable.nml .

yrstart=1750
yrend=1751
cp cable_driver.F90_$yrstart-$yrend  cable_driver.F90
./build.ksh
./cable > out_EucFACE/PM/historical/log.txt_$yrstart-$yrend
mv log_cable.txt out_EucFACE/PM/historical/log_cable.txt_$yrstart-$yrend
mv out_cable.nc out_EucFACE/PM/historical/out_cable.nc_$yrstart-$yrend
cp restart_out.nc ./restart_in.nc
mv restart_out.nc out_EucFACE/PM/historical/restart_out.nc_$yrstart-$yrend

yrstart=1752
yrend=1771
runcount=1
while [ $runcount -le 13 ]
do
  cp cable_driver.F90_$yrstart-$yrend cable_driver.F90
  ./build.ksh
  ./cable > out_EucFACE/PM/historical/log.txt_$yrstart-$yrend
  mv log_cable.txt out_EucFACE/PM/historical/log_cable.txt_$yrstart-$yrend
  mv out_cable.nc out_EucFACE/PM/historical/out_cable.nc_$yrstart-$yrend
  cp restart_out.nc ./restart_in.nc
  mv restart_out.nc out_EucFACE/PM/historical/restart_out.nc_$yrstart-$yrend
  runcount=`expr $runcount + 1`
  yrstart=`expr $yrstart + 20`
  yrend=`expr $yrend + 20`
done

