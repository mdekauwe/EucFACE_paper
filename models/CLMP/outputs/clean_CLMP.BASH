#!/bin/bash

for F in `ls *.csv`; do
    gawk '$1=$1' $F > x
    sed 's/ //g' x > $F
    rm x
done
