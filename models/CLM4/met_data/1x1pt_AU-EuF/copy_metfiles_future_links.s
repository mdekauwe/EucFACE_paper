#!/bin/bash

new_folder=''

#initial year of met data to start copying 
iyear=1949

#sequence of years to copy
for year in $(seq 1750 1948);do

 if [ $year -gt 1849 ]; then
  echo $year $iyear

  for m in $(seq 12);do

   if [ ${m} -lt 10 ];then
    if [ -e ./${new_folder}/${year}-0${m}.nc ]; then
     rm ./${new_folder}/${year}-0${m}.nc	
    fi
   cp ./${new_folder}/${iyear}-0${m}.nc ./${new_folder}/${year}-0${m}.nc
   fi

   if [ ${m} -gt 9 ];then
    if [ -e ./${new_folder}/${year}-${m}.nc ]; then
     rm ./${new_folder}/${year}-${m}.nc
    fi
    cp ./${new_folder}/${iyear}-${m}.nc ./${new_folder}/${year}-${m}.nc
   fi

  done
 fi

 iyear=$(($iyear+1))
 if [ $iyear -eq 2009 ]; then
  iyear=1949    
 fi 

done 

#add final three years 2009-2011
iyear=1949
for year in $(seq 2009 2011);do

  for m in $(seq 12);do

   if [ ${m} -lt 10 ];then
    if [ -e ./${new_folder}/${year}-0${m}.nc ]; then
     rm ./${new_folder}/${year}-0${m}.nc	
    fi
   cp ./${new_folder}/${iyear}-0${m}.nc ./${new_folder}/${year}-0${m}.nc
   fi

   if [ ${m} -gt 9 ];then
    if [ -e ./${new_folder}/${year}-${m}.nc ]; then
     rm ./${new_folder}/${year}-${m}.nc
    fi
    cp ./${new_folder}/${iyear}-${m}.nc ./${new_folder}/${year}-${m}.nc
   fi

  done

 iyear=$(($iyear+1))
 if [ $iyear -eq 2009 ]; then
  iyear=1949    
 fi 

done 

