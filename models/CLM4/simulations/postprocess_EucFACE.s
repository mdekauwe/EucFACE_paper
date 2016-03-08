#!/bin/bash

#script to postprocess all EucFACE simulations
RUN_DIR='/home/alp/models/clm4_ornl/run/'

SITE=( 'AU-EuF' )
SITE_S=( 'EUC' )

RUN=( 'N' 'N_eCO2' 'N_avg' 'N_eCO2_avg' )
RUNC=( 'AMBVAR' 'ELEVAR' 'AMBAVG' 'ELEAVG' )

YMD=`date +%y%m%d`

OUTDIR=EucFACE

#run post-processing script
netcdf_compile.s CLM_Euc_NCEASout
./CLM_Euc_NCEASout

#copy all processed files across to output directory 
mkdir ./$OUTDIR/$YMD
rm    ./$OUTDIR/*.csv
rm    ./$OUTDIR/$YMD/*.csv

s=0
for i in ${SITE[*]};do
 
 c=0
 for r in ${RUN[*]};do
  echo ${SITE_S[$s]} ${RUN[$c]}
  SIM=$i'_I20TRC'$r
  SIM_DIR=$RUN_DIR/$SIM/'run'/
  echo $SIM_DIR
  cd $SIM_DIR
  FNAME='D1CLM4'${SITE_S[$s]}${RUNC[$c]}'.csv'
  cp ./$FNAME ../../$OUTDIR
 
 let c++
 cd ../../
 done

let s++
done

#remove trailing comma from .csv files
cd ./$OUTDIR/
#for i in D1CLM4*.csv; do LF=$(gawk -F"," 'END{print NF-1}' $i); cut -d "," -f 1-$LF $i > x; mv x $i; done
for i in D1CLM4*.csv; do sed -i s'/.$//' $i; done
cp ./*.csv ./$YMD/
cd ../../




