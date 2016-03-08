#!/bin/bash

year_s=2000
new_folder=${1}/1x1pt_AU-EuF
cp_folder=../1x1pt_US-ORF/2000

#for year in $(seq 1992 2011);do
for year in $(seq 1949 2008);do
echo $year

for m in $(seq 12);do

if [ ${m} -lt 10 ];then	
cp ${cp_folder}-0${m}.nc ../${new_folder}/${year}-0${m}.nc
fi

if [ ${m} -gt 9 ];then
cp ${cp_folder}-${m}.nc ../${new_folder}/${year}-${m}.nc
fi


done

done 
