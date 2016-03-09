#!/usr/bin/env python

import os, sys, csv
from optparse import OptionParser

parser = OptionParser();

parser.add_option("--caseidprefix", dest="mycaseid", default="", \
                  help="Unique identifier to include as a prefix to the case name")
parser.add_option("--site", dest="site", default='', \
                  help = '6-character FLUXNET code to run (required)')
parser.add_option("--sitegroup", dest="sitegroup", default="AmeriFlux", \
                  help = "site group to use (default AmeriFlux)")
parser.add_option("--machine", dest="machine", default = 'generic_linux_pgi', \
                  help = "machine to use (default = generic_linux_pgi)")
parser.add_option("--csmdir", dest="csmdir", default='..', \
                  help = "base CESM directory (default = ../)")
parser.add_option("--ccsm_input", dest="ccsm_input", \
                  default='../../ccsm_inputdata', \
                  help = "input data directory for CESM (required)")
parser.add_option("--srcmods_loc", dest="srcmods_loc", default='../models/lnd/clm/src/SourceMods/', \
                  help = 'Copy sourcemods from this location (default = ../models/lnd/clm/src/SourceMods/')
parser.add_option("--nyears_final_spinup", dest="nyears_final_spinup", default='1000', \
                  help="base no. of years for final spinup")
parser.add_option("--clean_build", action="store_true", default=False, \
                  help="Perform a clean build")
parser.add_option("--hist_mfilt", dest="hist_mfilt", default="365", \
                  help = 'number of output timesteps per file (transient only)')
parser.add_option("--hist_nhtfreq", dest="hist_nhtfreq", default="-24", \
                  help = 'output file timestep (transient only)')
parser.add_option("--parm_file", dest="parm_file", default="", \
                  help = 'parameter file to use')
parser.add_option("--no_fire", dest="no_fire", default=True, \
                  action="store_true", help='Turn off fire algorithms')
parser.add_option("--regional", action="store_true", \
                   dest="regional", default=False, \
                   help="Flag for regional run (2x2 or greater)")
parser.add_option("--np", dest="np", default=1, \
                  help = 'number of processors')
parser.add_option("--tstep", dest="tstep", default=0.5, \
                  help = 'CLM timestep (hours)')
parser.add_option("--co2_file", dest="co2_file", default="fco2_datm_1765-2007_c100614.nc", \
                  help = 'CLM timestep (days) CO2 file stem, not full filename, site name and file extension added automatically to the end of the filename')
parser.add_option("--nyears_ad_spinup", dest="ny_ad", default=600, \
                  help = 'number of years to run ad_spinup')
parser.add_option("--metdir", dest="metdir", default="none", \
                  help = 'subdirectory for met data forcing')

(options, args) = parser.parse_args()

site       = options.site
ccsm_input = options.ccsm_input
mycaseid   = options.mycaseid
srcmods    = options.srcmods_loc

#get start and year of input meteorology from site data file
fname = './ccsm_utils/Tools/lnd/clm/PTCLM/PTCLM_sitedata/'+ \
                options.sitegroup+'_sitedata.txt'
AFdatareader = csv.reader(open(fname, "rb"))
for row in AFdatareader:
    if row[0] == site:
        startyear = int(row[6])
        endyear   = int(row[7])
ncycle   = endyear-startyear+1   #number of years in met cycle
translen = endyear-1850+1        #length of transient run

for i in range(0,ncycle+1):  #figure out length of final spinup run
    fsplen = int(options.nyears_final_spinup)+i
    if ((fsplen+translen) % ncycle == 0):
        break

#get align_year for transient run
year_align = (startyear-1850) % ncycle

basecmd = 'python call_PTCLM_eucface.py --site '+site+' --ccsm_input '+ \
          os.path.abspath(ccsm_input)+' --rmold --no_submit'
if (srcmods != ''):
    srcmods    = os.path.abspath(srcmods)
#    basecmd = basecmd+' --srcmods_loc '+srcmods
if (mycaseid != ''):
    basecmd = basecmd+' --caseidprefix '+mycaseid
if (options.parm_file != ''):
    basecmd = basecmd+' --parm_file '+options.parm_file
if (options.no_fire):
    basecmd = basecmd+' --no_fire '
if (options.clean_build):
    basecmd = basecmd+' --clean_build '
if (options.regional):
    basecmd = basecmd+' --regional '
#if (options.metdir !='none'):
#    basecmd = basecmd+' --metdir '+options.metdir
basecmd = basecmd + ' --np '+str(options.np)
basecmd = basecmd + ' --tstep '+str(options.tstep)
#basecmd = basecmd + ' --co2_file '+options.co2_file


#build commands
#AD spinup
cmd_adsp = basecmd+' --ad_spinup --nyears_ad_spinup '+str(options.ny_ad)+' --srcmods_loc '+srcmods
#exit spinup
cmd_exsp = basecmd+' --exit_spinup --nyears_ad_spinup '+str(options.ny_ad)+' --srcmods_loc '+srcmods
#final spinup
if mycaseid !='':
     basecase=mycaseid+'_'+site+'_I1850CN'
else:
     basecase=site+'_I1850CN'

cmd_fnsp = basecmd+' --finidat_case '+basecase+'_exit_spinup '+ \
           '--finidat_year '+str(int(options.ny_ad)+2)+' --run_units nyears --run_n '+ \
           str(fsplen)+' --srcmods_loc '+srcmods

#transient
#srcmods    = os.path.abspath('../models/lnd/clm/src/SourceMods_LTtrans/')

cmd_trns = basecmd+' --finidat_case '+basecase+ \
           ' --finidat_year '+str(fsplen+1)+' --run_units nyears' \
           +' --run_n '+str(translen)+' --align_year '+ \
           str(year_align+1850)+' --compset I20TRCN --hist_nhtfreq '+ \
           options.hist_nhtfreq+' --hist_mfilt '+options.hist_mfilt + \
	   ' --co2_file '+options.co2_file+'_'+site+'_control.nc'+ \
           ' --srcmods_loc '+srcmods         

#transient eCO2
cmd_trns2 = basecmd+' --finidat_case '+basecase+ \
           ' --finidat_year '+str(fsplen+1)+' --run_units nyears' \
           +' --run_n '+str(translen)+' --align_year '+ \
           str(year_align+1850)+' --compset I20TRCN --hist_nhtfreq '+ \
           options.hist_nhtfreq+' --hist_mfilt '+options.hist_mfilt + \
	   ' --co2_file '+options.co2_file+'_'+site+'.nc --eCO2_run'+ \
           ' --srcmods_loc '+srcmods

#transient average weather
cmd_trns3 = basecmd+' --finidat_case '+basecase+ \
           ' --finidat_year '+str(fsplen+1)+' --run_units nyears' \
           +' --run_n '+str(translen)+' --align_year '+ \
           str(year_align+1850)+' --compset I20TRCN --hist_nhtfreq '+ \
           options.hist_nhtfreq+' --hist_mfilt '+options.hist_mfilt + \
	   ' --co2_file '+options.co2_file+'_'+site+'_control.nc'+ \
           ' --srcmods_loc '+srcmods+' --metdir 1x1pt_'+site+'_AVG/ --avgweather_run'

#transient eCO2 avg weather
cmd_trns4 = basecmd+' --finidat_case '+basecase+ \
           ' --finidat_year '+str(fsplen+1)+' --run_units nyears' \
           +' --run_n '+str(translen)+' --align_year '+ \
           str(year_align+1850)+' --compset I20TRCN --hist_nhtfreq '+ \
           options.hist_nhtfreq+' --hist_mfilt '+options.hist_mfilt + \
	   ' --co2_file '+options.co2_file+'_'+site+'.nc --eCO2_run'+ \
           ' --srcmods_loc '+srcmods+' --metdir 1x1pt_'+site+'_AVG/ --avgweather_run'


#set site environment variable
os.environ['SITE']=site

input = open('./PTCLM_files/site_fullrun_template_4trans.pbs')
output = open('./PTCLM_files/site_fullrun_temp.pbs','w')
#make site-specific pbs script
for s in input:
    if mycaseid != '':
        output.write(s.replace("#SITE#",mycaseid+"_"+site))
    else:
        output.write(s.replace("#SITE#",site))        
input.close()
output.close()

input = open('./PTCLM_files/site_fullrun_temp.pbs')
#output = open('./PTCLM_files/site_fullrun.pbs','w')
if mycaseid != '':
    run_script = 'site_fullrun_'+mycaseid+'_'+site+'.pbs'
else:
    run_script = 'site_fullrun_'+site+'.pbs'

output = open('./PTCLM_files/'+run_script,'w')

for s in input:
        output.write(s.replace("#SCRIPTS#",os.path.abspath('.')))        
input.close()
output.close()
os.system('rm ./PTCLM_files/site_fullrun_temp.pbs')



#build cases
os.system(cmd_adsp)
os.system(cmd_exsp)
os.system(cmd_fnsp)
os.system(cmd_trns)
os.system(cmd_trns2)
os.system(cmd_trns3)
os.system(cmd_trns4)

#modify ndep filename in namelist .xml
cmd_mod_ndep = './ndep_mod_EucFACE.b'
os.system(cmd_mod_ndep)

#submit
os.chdir('PTCLM_files')
os.system('qsub '+run_script)

