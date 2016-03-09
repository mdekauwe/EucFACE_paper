#!/usr/bin/env python

import os, sys
from optparse import OptionParser
import Scientific.IO.NetCDF
from Scientific.IO import NetCDF
#from Numeric import *


#DMR 3/30/11
#call_PTCLM.py does the following:
#  1. executes official version of PTCLM with options specified below
#      Latest verson of PTCLM creates grid, surf, ndep and aerdep data
#      with site-level information and performs a create_newcase.
#      It makes several modifications to the env_conf and env_run xml
#      files.  It does NOT configure, build or submit - that is done by
#      this wrapper.
#      note:  PTCLM.py is in ./scripts/ccsm_utils/Tools/lnd/clm/PTCLM
#      site-level information is also in that location.
#  2. configure case
#  3. build (compile) CESM with clean_build first if requested
#  4. apply patch for transient CO2 if transient run
#  5. apply user-specified output options to namelist
#  6. apply user-specified PBS and submit information
#  7. submit job to PBS queue if requested.
#
#  For reproducibility, a copy of the current call_PTCLM.py is saved
#  to the newly created case directory.  This is for informational
#  purposes only - the script should not be executed from within
#  the case directory.
#
#-------------------Parse options-----------------------------------------------

parser = OptionParser()

parser.add_option("--caseidprefix", dest="mycaseid", default="", \
                  help="Unique identifier to include as a prefix to the case name")
parser.add_option("--site", dest="site", default='', \
                  help = '6-character FLUXNET code to run (required)')
parser.add_option("--sitegroup", dest="sitegroup", default="AmeriFlux", \
                  help = "site group to use (default AmeriFlux)")
parser.add_option("--coldstart", dest="coldstart", default=False, \
                  help = "set cold start (mutually exclusive w/finidat)", \
                  action="store_true")
parser.add_option("--compset", dest="compset", default='I1850CN', \
                  help = "component set to use (required)")
parser.add_option("--ad_spinup", action="store_true", \
                  dest="ad_spinup", default=False, \
                  help = 'Run accelerated decomposition spinup')
parser.add_option("--exit_spinup", action="store_true", \
                  dest="exit_spinup", default=False, \
                  help = 'Run exit spinup')
parser.add_option("--eCO2_run", action="store_true", \
                  dest="eCO2_run", default=False, \
                  help = 'Run eCO2 transient run')
parser.add_option("--eCO2_grad_run", action="store_true", \
                  dest="eCO2_grad_run", default=False, \
                  help = 'Run long-term eCO2 gradual change transient run')
parser.add_option("--eCO2_step_run", action="store_true", \
                  dest="eCO2_step_run", default=False, \
                  help = 'Run long-term eCO2 step change transient run')
parser.add_option("--avgweather_run", action="store_true", \
                  dest="avgweather_run", default=False, \
                  help = 'Run average weather transient run. Avg weather data directory must be specified')
parser.add_option("--nfert_run", action="store_true", \
                  dest="nfert_run", default=False, \
                  help = 'Nfertilisation simulation. need two sorcemod directories <SorceMods_Nfert> which contains sorce mods but NOT the N fertilisation mod and the sourcemod directory specified as an argument to <site_fullrun_2CO2byN.py>. The second source mod directory should have the same mods as the first EXCEPT in <CNNDynamicsMod.F90> which should have the N deposition routine modified to add fertiliser accordingly')
parser.add_option("--machine", dest="machine", default = 'generic_linux_pgi', \
                  help = "machine to use (default = generic_linux_pgi)")
parser.add_option("--csmdir", dest="csmdir", default='..', \
                  help = "base CESM directory (default = ../)")
parser.add_option("--ccsm_input", dest="ccsm_input", \
                  default='../../ccsm_inputdata', \
                  help = "input data directory for CESM (required)")
parser.add_option("--finidat_case", dest="finidat_case", default='', \
                  help = "case containing initial data file to use" \
                  +" (should be in your run directory)")
parser.add_option("--finidat_year", dest="finidat_year", default=-1, \
                  help = "model year of initial data file (default is" \
                  +" last available)")
parser.add_option("--run_units", dest="run_units", default='', \
                  help = "run length units (ndays, nyears)")
parser.add_option("--run_n", dest="run_n", default=1, \
                  help = "run length (in run units)")
parser.add_option("--rmold", dest="rmold", default=False, action="store_true", \
                  help = 'Remove old case directory with same name' \
                  +" before proceeding")
parser.add_option("--srcmods_loc", dest="srcmods_loc", default='', \
                  help = 'Copy sourcemods from this location')
parser.add_option("--parm_file", dest="parm_file", default='',
                  help = 'file for parameter modifications')
parser.add_option("--hist_mfilt", dest="hist_mfilt", default=-1, \
                  help = 'number of output timesteps per file')
parser.add_option("--hist_nhtfreq", dest="hist_nhtfreq", default=-999, \
                  help = 'output file timestep')
parser.add_option("--hist_vars", dest="hist_vars", default='', \
                  help = 'use hist_vars file')
parser.add_option("--queue", dest="queue", default='esd08q', \
                  help = 'PBS submission queue')
parser.add_option("--clean_build", dest="clean_build", default=False, \
                  help = 'Perform clean build before building', \
                  action="store_true")
parser.add_option("--no_config", dest="no_config", default=False, \
                  help = 'do NOT configure case', action="store_true")
parser.add_option("--no_build", dest="no_build", default=False, \
                  help = 'do NOT build CESM', action="store_true")
parser.add_option("--no_submit", dest="no_submit", default=False, \
                  help = 'do NOT submit CESM to queue', action="store_true")
parser.add_option("--no_fire", dest="no_fire", action="store_true", \
                  default=False, help="Turn off fire algorightms")
parser.add_option("--align_year", dest="align_year", default="1850", \
                  help = 'Alignment year (transient run only)')
parser.add_option("--regional", action="store_true", \
                   dest="regional", default=False, \
                   help="Flag for regional run (2x2 or greater)")
parser.add_option("--np", dest="np", default=1, \
                  help = 'number of processors')
parser.add_option("--tstep", dest="tstep", default=0.5, \
                  help = 'CLM timestep (hours)')
parser.add_option("--co2_file", dest="co2_file", default="fco2_datm_1765-2007_c100614.nc", \
                  help = 'CLM timestep (hours)')
parser.add_option("--nyears_ad_spinup", dest="ny_ad", default=600, \
                  help = 'number of years to run ad_spinup')
parser.add_option("--metdir", dest="metdir", default="none", \
                  help = 'subdirectory for met data forcing')
parser.add_option("--nopointdata", action="store_true", \
                  dest="nopointdata", help="Do NOT make point data (use data already created)", \
                  default=False)
parser.add_option("--croot", dest="mycasesroot", default="./", \
                    help="Directory where the case would be created")
parser.add_option("--rroot", dest="myrunroot", default="./", \
                    help="Directory where the run would be created")
parser.add_option("--cleanlogs",dest="cleanlogs", help=\
                   "Removes temporary and log files that are created",\
                   default=False,action="store_true")
parser.add_option("--numxpts", dest="mynumxpts", default="", \
                    help="Number of points in Longitude-direction")
parser.add_option("--numypts", dest="mynumypts", default="", \
                    help="Number of points in Latitude-direction")
parser.add_option("--sitee", dest="mysitee", default="", \
                    help="Site eastern edge")
parser.add_option("--sitew", dest="mysitew", default="", \
                    help="Site wastern edge")
parser.add_option("--siten", dest="mysiten", default="", \
                    help="Site northern edge")
parser.add_option("--sites", dest="mysites", default="", \
                    help="Site southern edge")
(options, args) = parser.parse_args()

#-------------------------------------------------------------------------------


#check for valid csm directory
if (os.path.exists(options.csmdir) == False):
    print('Error:  invalid CESM directory')
    sys.exit()
else:
    csmdir=os.path.abspath(options.csmdir)

#check for valid input data directory
if (options.ccsm_input == '' or (os.path.exists(options.ccsm_input) \
                                 == False)):
    print('Error:  invalid input data directory')
    sys.exit()
else:
    options.ccsm_input = os.path.abspath(options.ccsm_input)

#check for valid compset
compset = options.compset
if (compset != 'I1850CN' and compset != 'I2000CN' and compset != 'I20TRCN'):
    print('Error:  please enter valid option for compset')
    print('        (I1850CN, I2000CN, I20TRCN)')
    sys.exit()

#check consistency of options
if (options.ad_spinup and options.exit_spinup):
    print('Error:  Cannot specify both ad_spinup and exit_spinup')
    sys.exit()
    
if (compset == 'I20TRCN'):
    #ignore spinup option if transient compset
    if (options.ad_spinup or options.exit_spinup):
      print('Spinup options not available for transient compset.')
      sys.exit()
    #finidat is required for transient compset
    if (options.finidat_case == ''):
        print('Error:  must provide initial data file for I20TRCN compset')
        sys.exit()

#get full path of finidat file
finidat=''
finidat_year=int(options.finidat_year)
if (options.exit_spinup):
    if (options.mycaseid != ''):
        options.finidat_case = options.mycaseid+'_'+options.site+ \
                               '_I1850CN_ad_spinup'
    else:
        options.finidat_case = options.site+'_I1850CN_ad_spinup'
    finidat_year = int(options.ny_ad)+1
if (options.finidat_case != ''):
    finidat_yst = str(finidat_year)
    if (finidat_year >= 100 and finidat_year < 1000):
        finidat_yst = '0'+str(finidat_year)
    if (finidat_year >= 10 and finidat_year < 100):
        finidat_yst = '00'+str(finidat_year)
    if (finidat_year < 10):
        finidat_yst = '000'+str(finidat_year)
    finidat = csmdir+'/run/'+options.finidat_case+'/run/'+ \
              options.finidat_case+'.clm2.r.'+finidat_yst+ \
              '-01-01-00000.nc'

#construct default casename
casename    = options.site+"_"+compset
if (options.mycaseid != ""):
    casename = options.mycaseid+'_'+casename
if (options.ad_spinup):
    casename = casename+'_ad_spinup'
if (options.exit_spinup):
    casename = casename+'_exit_spinup'
if (options.eCO2_run):
    casename = casename+'_eCO2'
if (options.eCO2_grad_run):
    casename = casename+'_eCO2_grad'
if (options.eCO2_step_run):
    casename = casename+'_eCO2_step'
if (options.avgweather_run):
    casename = casename+'_avg'
if (options.nfert_run):
    casename = casename+'_Nfert'

PTCLMdir = csmdir+'/scripts/ccsm_utils/Tools/lnd/clm/PTCLM'

if (options.mycasesroot != "./"):
    casedir=options.mycasesroot+"/"+casename
else:
    casedir=csmdir+"/scripts/"+casename

#build PTCLM command line options
cmd = './PTCLM.py '+"-s "+options.site+" --sitegroup "+options.sitegroup \
      +" -c "+compset+" --ndepgrid --aerdepgrid"
cmd = cmd+" -m "+options.machine+' -d '+options.ccsm_input
if (options.ad_spinup):
    cmd = cmd+" --ad_spinup"
    cmd = cmd+" --nyears_ad_spinup "+str(options.ny_ad)
if (options.exit_spinup):
    cmd = cmd+" --exit_spinup"
    cmd = cmd+" --nyears_ad_spinup "+str(options.ny_ad)
if (options.eCO2_run):
    cmd = cmd+" --eCO2_run"
if (options.eCO2_grad_run):
    cmd = cmd+" --eCO2_grad_run"
if (options.eCO2_step_run):
    cmd = cmd+" --eCO2_step_run"
if (options.avgweather_run):
    cmd = cmd+" --avgweather_run"
if (options.nfert_run):
    cmd = cmd+" --nfert_run"
if (options.run_units != ''):
    cmd = cmd+" --run_units "+options.run_units
    cmd = cmd+" --run_n "+str(options.run_n)
if (finidat != '' and options.exit_spinup == False):
    cmd = cmd+" --finidat "+finidat
if (options.regional):
    cmd = cmd+' --regional'
if (options.rmold):
    cmd = cmd+' --rmold'
else:
#    if (os.path.exists('./'+casename)):
    if (os.path.exists(casedir)):
        print('Warning:  Case directory exists and --rmold not specified')
        var = raw_input('proceed (p), remove old (r), or exit (x)? ')
        if var[0] == 'r':
            cmd = cmd+' --rmold'
        if var[0] == 'x':
            sys.exit()       
if (options.mycaseid != ''):
    cmd = cmd+' --caseidprefix '+options.mycaseid
if (options.coldstart):
    cmd = cmd+' --coldstart'
if (options.nopointdata):
    cmd = cmd+' --nopointdata'
if (options.mycasesroot != "./"):
    cmd = cmd+" --croot="+options.mycasesroot
if (options.myrunroot != "./"):
    cmd = cmd+" --rroot="+options.myrunroot
if (options.cleanlogs):
    cmd = cmd+" --cleanlogs"
if (options.mynumxpts != ''):
    cmd = cmd+" --numxpts="+options.mynumxpts
if (options.mynumypts != ''):
    cmd = cmd+" --numypts="+options.mynumypts
if (options.mysitee != ''):
    cmd = cmd+" --sitee="+options.mysitee
if (options.mysitew != ''):
    cmd = cmd+" --sitew="+options.mysitew
if (options.mysites != ''):
    cmd = cmd+" --sites="+options.mysites
if (options.mysiten != ''):
    cmd = cmd+" --siten="+options.mysiten

os.chdir(PTCLMdir)  
#execute PTCLM
print(cmd)
os.system(cmd)

#go to newly created case directory
if (options.mycasesroot == "./" ):
    print('options.mycasesroot '+options.mycasesroot)
    print('casedir '+casedir)
    os.chdir(csmdir+"/scripts/"+casename)
else:
    os.chdir(casedir)

#change some xml values
if (options.tstep != 0.5):
    os.system('./xmlchange -file env_conf.xml -id ' \
              +'ATM_NCPL -val '+str(int(24/float(options.tstep))))

#adds capability to run with transient CO2
if (compset == 'I20TRCN'):
    os.system('./xmlchange -file env_conf.xml -id ' \
              +'CCSM_BGC -val CO2A')
    os.system('./xmlchange -file env_conf.xml -id ' \
              +'CLM_CO2_TYPE -val diagnostic')

os.system('./xmlchange -file env_conf.xml -id ' \
          +'CCSM_CO2_PPMV -val 276.84')


#if running regional with > 1 processor
if (int(options.np) > 1):
    os.system('./xmlchange -file env_mach_pes.xml -id ' \
              +'NTASKS_LND -val '+options.np)
    os.system('./xmlchange -file env_conf.xml -id ' \
              +'USE_MPISERIAL -val FALSE')

#if cold start default to 1000 year run
if (options.coldstart and options.run_units == ''):
    os.system('./xmlchange -file env_run.xml -id ' \
              +'STOP_OPTION -val nyears')
    os.system('./xmlchange -file env_run.xml -id ' \
              +'STOP_N -val 1000')
    os.system('./xmlchange -file env_run.xml -id ' \
              +'REST_OPTION -val nyears')
    os.system('./xmlchange -file env_run.xml -id ' \
              +'REST_N -val 1000')

#configure case
if (options.no_config == False):
    os.system('./configure -case')
else:
    print("Warning:  No case configure performed.  PTCLM will not " \
          +"make any requested modifications to env_*.xml files.  Exiting.")
    sys.exit()

#copy sourcemods
os.chdir('..')
if (options.srcmods_loc != ''):
    if (os.path.exists(options.srcmods_loc) == False):
        print('Invalid srcmods directory.  Exiting')
        sys.exit()
    options.srcmods_loc = os.path.abspath(options.srcmods_loc)
    os.system('cp -r '+options.srcmods_loc+'/* ./'+casename+ \
              '/SourceMods')
if(options.mycasesroot == './' ):
    os.chdir(csmdir+"/scripts/"+casename)
else:
    os.chdir(casedir)

#clm build exe modifications
input  = open("./Buildconf/clm.buildexe.csh")
output = open("./Buildconf/clm.buildexetemp.csh",'w')
for s in input:
    if (options.no_fire and s[0:11] == 'set clmdefs'):
        output.write(s[:-2]+' -DNOFIRE" \n')
    else:
        output.write(s)
input.close()
output.close()
os.system("mv ./Buildconf/clm.buildexetemp.csh "+ \
          "./Buildconf/clm.buildexe.csh")
os.system("chmod u+x ./Buildconf/clm.buildexe.csh")

#clean build if requested
if (options.clean_build):
    os.system('./'+casename+'.'+options.machine+'.'+'clean_build')
#compile cesm
if (options.no_build == False):
    os.system('./'+casename+'.'+options.machine+'.'+'build')

#copy rpointers and restart files to current run directory
if (finidat != ''):
    os.system('cp '+csmdir+'/run/'+options.finidat_case+'/run/'+ \
              options.finidat_case+'.*'+finidat_yst+'* '+csmdir+ \
              '/run/' +casename+'/run/')
    os.system('cp '+csmdir+'/run/'+options.finidat_case+'/run/'+ \
              'rpointer.* '+csmdir+'/run/'+casename+'/run/')
              
#parameter (pft-phys) modifications if desired
os.chdir('..')
if (options.parm_file != ''):
    pftfile = NetCDF.NetCDFFile(options.ccsm_input+'/lnd/clm2/pftdata/' \
                                +'pft-physiology.c110425.'+ \
                                options.mycaseid+options.site+'.nc',"a")
    input   = open(os.path.abspath(options.parm_file))
    for s in input:
        if s[0:1] != '#':
            values = s.split()
            temp = pftfile.variables[values[0]]
            temp_data = temp.getValue()
            print('old vals:')
            print(temp_data)
            temp_data[int(values[1])] = float(values[2])
            print('new vals:')
            print(temp_data)
            temp.assignValue(temp_data)
    input.close()
    pftfile.close()
if (options.mycasesroot == './'):
    os.chdir(csmdir+"/scripts/"+casename)
else:
    os.chdir(casedir)
    
#transient CO2 patch for transient run (datm buildnml mods)
if (compset == "I20TRCN"):
    os.system('cp '+PTCLMdir+'/tower_transient_co2_patch.py .')
    os.system('python tower_transient_co2_patch.py --site '+ \
              options.site+' --align_year '+options.align_year \
              +' --sitegroup '+options.sitegroup+' --ccsm_input '+ \
              options.ccsm_input+' --co2_file '+options.co2_file)
    os.system('chmod a+x ./Buildconf/datm.buildnml.csh')

#make case-specific surface data file
mysimyr=1850
if (compset == 'I2000CN'):
    mysimyr=2000
os.system('cp '+options.ccsm_input+'/lnd/clm2/surfdata/' \
          +'surfdata_1x1pt_'+options.site+'_simyr'+str(mysimyr)+'.nc ' \
          +options.ccsm_input+'/lnd/clm2/surfdata/surfdata_1x1pt_'+ \
          casename+'_simyr'+str(mysimyr)+'.nc')
os.system('chmod u+w '+options.ccsm_input+'/lnd/clm2/surfdata/surfdata_' \
          +'1x1pt_'+casename+'_simyr'+str(mysimyr)+'.nc')
if (compset == 'I20TRCN'):
    os.system('cp '+options.ccsm_input+'/lnd/clm2/surfdata/' \
          +'surfdata.pftdyn_1x1pt_'+options.site+'_simyr*.nc ' \
          +options.ccsm_input+'/lnd/clm2/surfdata/surfdata.pftdyn_1x1pt_'+ \
          casename+'.nc')
    os.system('chmod u+w '+options.ccsm_input+'/lnd/clm2/surfdata/surfdata' \
          +'.pftdyn_1x1pt_'+casename+'.nc')

#clm namelist modifications
input  = open("./Buildconf/clm.buildnml.csh")
output = open("./Buildconf/clm.buildnmltemp.csh",'w')
#write requested output timesteps/freq
line=0
line2=0
for s in input:
    if (options.hist_mfilt != -1 and s[0:11] == ' hist_mfilt'):
        output.write(" hist_mfilt             = "+ \
                     str(options.hist_mfilt)+"\n")
    elif (options.hist_nhtfreq != -999 and s[0:12] == ' hist_nhtfrq'):
        output.write(" hist_nhtfrq            = "+ \
                     str(options.hist_nhtfreq)+"\n")
    elif (options.hist_vars != '' and line == 27):
        output.write(" hist_empty_htapes      = .true.\n")
        #read hist_vars file
        hvars_file = open('../'+options.hist_vars)
        myline = " hist_fincl1            = "
        for s2 in hvars_file:
            if line2 ==0:
                myline = myline+"'"+s2.strip()+"'"
            else:
                myline = myline+",'"+s2.strip()+"'"
            line2=line2+1
        output.write(myline+"\n")
        hvars_file.close()
    elif (s[0:7] == ' nrevsn' and options.exit_spinup):
        output.write(" nrevsn       = '"+finidat+"'\n")
    elif (s[0:8] == ' fsurdat'):
        output.write(" fsurdat                = '"+options.ccsm_input+ \
                     "/lnd/clm2/surfdata/surfdata_1x1pt_"+casename+ \
                     "_simyr"+str(mysimyr)+".nc'\n")
    elif (s[0:8] == ' fpftdyn'):
        output.write(" fpftdyn                = '"+options.ccsm_input+ \
                     "/lnd/clm2/surfdata/surfdata.pftdyn_1x1pt_"+ \
                     casename+".nc'\n")
    else:
        output.write(s)
    line=line+1
output.close()
input.close()
os.system("mv ./Buildconf/clm.buildnmltemp.csh ./Buildconf/clm.buildnml.csh")
os.system("chmod a+x ./Buildconf/clm.buildnml.csh")

#datm namelist modifications
input  = open("./Buildconf/datm.buildnml.csh")
output = open("./Buildconf/datm.buildnmltemp.csh",'w')
#cycle all streams
for s in input:
    output.write(s.replace("'extend'","'cycle'"))
output.close()
input.close()
input  = open("./Buildconf/datm.buildnmltemp.csh")
output = open("./Buildconf/datm.buildnml.csh",'w')
#met data subdirectory
for s in input:
    if (options.metdir != 'none'):
        output.write(s.replace('/CLM1PT_data/','/CLM1PT_data/'+options.metdir+'/'))
    else:
        output.write(s)
output.close()
input.close()

os.system("chmod a+x ./Buildconf/datm.buildnml.csh")


#make necessary modificaitons to run script for OIC
if (options.machine == "generic_linux_pgi"):
    input  = open("./"+casename+"."+options.machine+".run")
    output = open("./"+casename+"temp.run",'w')
    for s in input:
        if s[6:8]  == '-N':
            output.write("#PBS -N "+casename+"\n")
        elif s[9:14] == 'batch':
            output.write("#PBS -q "+options.queue+"\n")
        elif s[0:4] == 'cd /':                 
            #output.write("cd "+csmdir+'/scripts/'+casename+"\n")
            os.chdir(casedir)
        elif s[0:14] =="##PBS -l nodes":
            output.write("#PBS -l nodes="+str((int(options.np)-1)/8+1)+ \
                         ":ppn="+str(min(int(options.np),8))+"\n")  
        elif s[9:17] == 'walltime':
            output.write("#PBS -l walltime=48:00:00\n") 
        elif s[0:5] == '##PBS':
            output.write(s.replace("##PBS","#PBS"))
        elif s[0:7] == '   exit':
            output.write('   #exit 2')
        elif s[0:10] == '   #mpirun':
             output.write("   mpirun -np "+str(options.np)+" --hostfile $PBS_NODEFILE ./ccsm.exe >&! ccsm.log.$LID\n")
        elif s[0:5] == 'sleep':
            output.write("sleep 5\n")
        else:
            output.write(s)
    output.close()
    input.close()
    os.system("mv "+casename+"temp.run "+casename+"."+options.machine+".run")

#submit job if requested
if (options.no_submit == False):
    os.system("qsub "+casename+"."+options.machine+".run")

#copy call_PTCLM.py to case directory
#os.chdir('..')
#os.system("cp "+cmd+" ./"+casename+'/call_PTCLM_'+casename+'.cmd')
