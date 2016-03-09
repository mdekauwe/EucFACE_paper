#!/bin/bash

./copy_metfiles.s ''

./copy_metfiles_future.s ''
./copy_metfiles_future.s 1x1pt_AU-EuF_AVG

#./conv_CDF_to_CLM
./conv_ALMA_to_CLM

./copy_metfiles_future_links.s
./retimestamp

cp -t ../1x1pt_AU-EuF_AVG/1x1pt_AU-EuF/ {1850..2011}*.nc


