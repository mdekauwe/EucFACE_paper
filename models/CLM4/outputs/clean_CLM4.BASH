#!/bin/bash

for F in `ls *.csv`; do
  sed 's/\*\*\*\*\*\*\*\*\*\*\*\*/-9999.000000/g' $F > tmp
  mv tmp $F
done

for F in `ls *.csv`; do
    sed 's/ //g' $F > tmp
    mv tmp $F
done