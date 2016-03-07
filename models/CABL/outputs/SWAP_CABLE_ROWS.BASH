#!/bin/bash

# The CABLE header is written in a really tricky way to read as the units come
# after the column headers, making it hard to just skip them


for F in D1*.csv;
do
    SWAP_LINES_DAILY.PL $F > tmp
    mv tmp $F
done

#for F in H1*.csv;
#do
#    SWAP_LINES_HOURLY.PL $F > tmp
#    mv tmp $F
#done
