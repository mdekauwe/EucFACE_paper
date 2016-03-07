#!/bin/bash

for F in `ls *.csv`; do
    OFNAME=$(echo $F | sed 's/5/1/')
    sed 's/\*\*\*\*\*\*\*\*\*\*\*\*/-9999.000000/g' $F | sed 's/ //g' > $OFNAME
    rm $F
done
