#!/bin/bash
#SBATCH --time=00:10:00
#SBATCH --mem=4GB
echo $HOST
cd /data/pak007/CABLE-2.0_EucFACE/offline/out_EucFACE/PM/future/

cd ./AMBVAR
#ifort -o process_hr process_hr.f90
./process_hr
cat ../H1header.csv H1CABLEUCAMBVAR.csv > tmp.csv
mv tmp.csv H1CABLEUCAMBVAR.csv
#ifort -o process_day process_day.f90
./process_day
cat ../D1header.csv D1CABLEUCAMBVAR.csv > tmp.csv
mv tmp.csv D1CABLEUCAMBVAR.csv

cd ../AMBAVG
#ifort -o process_hr process_hr.f90
./process_hr
cat ../H1header.csv H1CABLEUCAMBAVG.csv > tmp.csv
mv tmp.csv H1CABLEUCAMBAVG.csv
#ifort -o process_day process_day.f90
./process_day
cat ../D1header.csv D1CABLEUCAMBAVG.csv > tmp.csv
mv tmp.csv D1CABLEUCAMBAVG.csv

cd ../ELEAVG
#ifort -o process_hr process_hr.f90
./process_hr
cat ../H1header.csv H1CABLEUCELEAVG.csv > tmp.csv
mv tmp.csv H1CABLEUCELEAVG.csv
#ifort -o process_day process_day.f90
./process_day
cat ../D1header.csv D1CABLEUCELEAVG.csv > tmp.csv
mv tmp.csv D1CABLEUCELEAVG.csv

cd ../ELEVAR
#ifort -o process_hr process_hr.f90
./process_hr
cat ../H1header.csv H1CABLEUCELEVAR.csv > tmp.csv
mv tmp.csv H1CABLEUCELEVAR.csv
#ifort -o process_day process_day.f90
./process_day
cat ../D1header.csv D1CABLEUCELEVAR.csv > tmp.csv
mv tmp.csv D1CABLEUCELEVAR.csv


