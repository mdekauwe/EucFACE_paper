#!/bin/bash

# There is a trailing comma at the end of the outputs (but not in the header)
# This will mess up the read_csv function, so remove it.


for F in D1*.csv;
do
    sed 's%,$%%' $F > tmp
    mv tmp $F
done

#for F in H1*.csv;
#do
#    sed 's%,$%%'  $F > tmp
#    mv tmp $F
#done
