#!/bin/bash

for F in `ls *.csv`; do
    sed 's/\*\*\*\*\*\*\*\*\*\*\*\*/-9999.000000/g' $F  > x
    sed 's/Inf/-9999.000000/g' x > $F
done
