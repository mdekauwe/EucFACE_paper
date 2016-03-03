#!/usr/bin/env python

"""
Compile all of the model outputs into one large readable pandas dataframe,
then pickle this for future use

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (07.11.2013)"
__email__ = "mdekauwe@gmail.com"

import sys
import os
import glob
import pandas
import numpy as np
import cPickle as pickle
import datetime as dt
import matplotlib.pyplot as plt
import calendar

def date_converter(*args):
    s = str(int(float(args[0]))) + " " + str(int(float(args[1])))
    return dt.datetime.strptime(s, '%Y %j')

outdir = "data"
if not os.path.exists(outdir):
    os.makedirs(outdir)

df_list = []
key_list = []
fdir = os.getcwd()
model_list = os.walk(fdir).next()[1]


model_list = ["CABL","CLMP","CLM4","GDAY","LPJW","LPJX","OCNX","SDVM"]
delimiters = [",",",",",",",",",",",",",",","]
delimiters = dict(zip(model_list, delimiters))
header_junk = [7,0,0,3,2,2,0,0]
header_skip = dict(zip(model_list, header_junk))

for model in model_list:
    for fname in glob.glob(os.path.join(fdir, model + "/D*.csv")):

        fd = os.path.basename(fname).split(".")[0]
        (model, treatment, exp) = fd[2:6], fd[9:12], fd[12:]

        df = pandas.read_csv(fname, parse_dates=[[0,1]],
                             skiprows=header_skip[model],
                             index_col=0, sep=delimiters[model],
                             keep_date_col=True, date_parser=date_converter,
                             skipinitialspace=True)
        # added the skipinitialspace as CABLE has a whitespace before first column

        # remove empty column in SDVM data, should catch same issue in
        # other models output
        df = df.dropna(axis=1, how="all") #drop only if ALL columns are NaN

        # otherwise can't do boolean on mixed-type frames
        df = df.astype(np.float32)

        # need to convert the year from object to slice via it.
        df['YEAR'] = df.YEAR.astype(int)
        df['DOY'] = df.DOY.astype(int)

        # apply uniform mask as data varies...
        df[df < -800.0] = np.nan

        # Add correction index for the S.Hemisphere. Assuming year begins 1st of
        # June.
        SYEAR = []
        SDOY = []
        for index, row in df.iterrows():

            if calendar.isleap(row['YEAR']):
                half_yr = 183
                offset = 182
            else:
                half_yr = 182
                offset = 181

            # models without leap years
            if model == "CLMP" or model =="CLM4":
                half_yr = 182
                offset = 181

            if row['DOY'] < half_yr:
                SYEAR.append(int(row['YEAR']-1))
                SDOY.append(int(row['DOY']+offset))
            else:
                SYEAR.append(int(row['YEAR']))
                SDOY.append(int(row['DOY']-offset))
        df['SYEAR'] = SYEAR
        df['SDOY'] = SDOY

        df_list.append(df)

        # allows us to select by m, s or t
        key_list.append((model,treatment,exp))
df = pandas.concat(df_list, axis=1, keys=key_list,
                   names=["model","treatment","exp"])

# http://pandas.pydata.org/pandas-docs/dev/indexing.html#the-need-for-sortedness-with-multiindex
df = df.sortlevel(0, axis=1)
df.to_pickle(os.path.join(outdir, "models_output.pkl"))
