#!/bin/bash

#this file modifies the namelist <CASEDIRECTORY>/Buildconf/clm.buildnml.csh
#replacing the global N deposition data with the point data

#The Ndepos data file was originall taken from, cereated by Xiaojuan Yang:
# /home/xyk/DownloadedCCSMData/ccsm_inputdata/lnd/clm2/ndepdata/fndep_clm_simyr1849-2006_1x1pt_AU-EuF.nc

DIRSTEM='/home/alp/models/'
RUNDIR='clm4_ornl/scripts/'
SITE=AU-EuF
CASES=( I1850CN_ad_spinup I1850CN_exit_spinup I1850CN I20TRCN I20TRCN_eCO2 I20TRCN_avg I20TRCN_eCO2_avg )

NDEPDIR1=$DIRSTEM'ccsm_inputdata/lnd/clm2/ndepdata/fndep_clm_simyr1849-2006_1x1pt_AU-EuF.nc'
NDEPDIR2=$DIRSTEM'ccsm_inputdata/lnd/clm2/ndepdata/fndep_clm_simyr1849-2023_1x1pt_AU-EuF_fromXYK.nc'

for c in ${CASES[*]}; do
 
DIR=$DIRSTEM$RUNDIR$SITE'_'$c'/Buildconf/'

echo $c'/Buildconf/clm.buildnml.csh modification:: new Ndeposition file'
echo $NDEPDIR1
echo

cp $DIR'clm.buildnml.csh' $DIR'clm.buildnml.csh.premod'
sed -i s@$NDEPDIR1@$NDEPDIR2@ $DIR'clm.buildnml.csh'
sed -i s@'= 2005'@'= 2023'@   $DIR'clm.buildnml.csh'
diff $DIR'clm.buildnml.csh.premod' $DIR'clm.buildnml.csh'

done

