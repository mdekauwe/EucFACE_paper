#!/bin/bash

for F in `ls *.csv`; do
    sed 's/"//g' $F > x
    mv x $F
done
