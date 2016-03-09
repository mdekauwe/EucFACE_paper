program make300yearmetdata

!this program takes a pre-existing set of CLM formatted netcdf files 
!and modifies them according to an input dataset

!could also adapt to just create a CLM formatted netcdf from scratch 
!and use the input dataset  


use netcdf

implicit none

logical leap_yr, ascii, hourly, verbose
integer NCID, RCODE, varid, dimid, dimlength
 character(10) dimname
integer i,y,m,z,md,ms,me,s,e,d_in_m(12),leap_yrs
 character(64) data_fname(3),time_unit,fname,opath,site
 character(10) fend1(3),fend2(3),fend3(3)
 character(128) data_path 
 character(4) y_c
 character(2) m_c

integer time, year, doy, i_steps, tstep
real lon, lat, hod, trash
real tair_f(1,1,1800)
real tair_h(1,1,48*(70*365+5)), rh_h(1,1,48*(70*365+5)), wind_h(1,1,48*(70*365+5))
real swdown_h(1,1,48*(70*365+5)), lwdown_h(1,1,48*(70*365+5))
real rainf_h(1,1,48*(70*365+5)), snowf_h(1,1,48*(70*365+5))
real wind_n_h(1,1,48*(70*365+5)), wind_e_h(1,1,48*(70*365+5))
real qair_h(1,1,48*(70*365+5)), paw_h(1,1,48*(70*365+5)), paws_h(1,1,48*(70*365+5))

real tair(1,1,24*(70*365+5)), rh(1,1,24*(70*365+5)), wind(1,1,24*(70*365+5))
real swdown(1,1,24*(70*365+5)), lwdown(1,1,24*(70*365+5))
real rainf(1,1,24*(70*365+5)), snowf(1,1,24*(70*365+5)) 

integer psurf_h_i(1,1,48*(70*365+5)), psurf_i(1,1,24*(70*365+5))
real    psurf_h_r(1,1,48*(70*365+5)), psurf_r(1,1,24*(70*365+5)) 
integer gmt_offset 

real zbot(1,1,24*(70*365+5))
 
!write details to screen
verbose=.FALSE.
!ascii or netdcf
ascii  = .FALSE.
!output halfhourly or hourly
hourly = .FALSE. 
if(hourly) then
 tstep = 24
else
 tstep = 48
endif

!measurement height
zbot(:,:,:) = 2.0
d_in_m = (/ 31,28,31,30,31,30,31,31,30,31,30,31 /)

!GMT offset in hours - not used, changed longitude instead
gmt_offset = 11
if(.not.hourly) gmt_offset = gmt_offset * 2

!z=0
!data file names & path
site = '1x1pt_AU-EuF'
data_fname = (/ 'EucFACE_forcing_1949-2008', &
                'EucFACE_forcing_2012-2023', &
                'EucFACE_forcing_2012-2023' /)
fend1 = (/ '', '_AMBAVG', '_AMBVAR' /)
fend2 = (/ '', '_CDF ', '_ALMA' /)
fend3 = (/ '.csv', '.nc', '.nc' /)

!loop through met data types
do md=1,3
!set start and end years
if(md.ge.2) then
 s=2012
 e=2023
 leap_yrs=3
else
 s=1949
 e=2008
 leap_yrs=15
endif

!set opath directory
if(md.eq.2) then 
 opath = '../'//trim(site)//'_AVG/'//trim(site)//'/'
else
 opath = './'  
endif

!number of input time steps
i_steps = tstep*((e-s+1)*365+leap_yrs)

if(ascii)then
!open ascii data file
data_path = './EucFACE_met_data/'//trim(data_fname(md))//trim(fend1(md))//trim(fend2(1))//trim(fend3(1))
open(50,file=data_path,action='READ',status='OLD')
read(50,*)

!read ascii file data 
do i=1,i_steps
 read(50,*) year, doy, hod, swdown_h(1,1,i), trash, lwdown_h(1,1,i), &
 	tair_h(1,1,i), rainf_h(1,1,i), snowf_h(1,1,i), trash, trash, &
	rh_h(1,1,i),  wind_h(1,1,i), psurf_h_r(1,1,i), trash, trash   
enddo

else
!open ALMA data file
data_path = './EucFACE_met_data/'//trim(data_fname(md))//trim(fend1(md))//trim(fend2(3))//trim(fend3(2))
RCODE = NF90_OPEN(trim(data_path), NF90_NOWRITE, NCID)
print*, ''
print*, 'read ',  data_path, data_fname(md)
call NCDF_ER(RCODE,'open')

!read ALMA file data
 if(md.eq.1) then
 RCODE = NF90_INQ_DIMID(NCID,'tstp',dimid)
 call NCDF_ER(RCODE,'tstp')
 RCODE = NF90_INQUIRE_DIMENSION(NCID, dimid, dimname, dimlength)
 call NCDF_ER(RCODE,'tstp')
 RCODE = NF90_INQ_VARID(NCID,'wind',varid)
 call NCDF_ER(RCODE,'wind')
 RCODE = NF90_GET_VAR(NCID, varid, wind_h,  start=(/ 1,1,1,1 /),count=(/ 1,1,1,i_steps /))
 call NCDF_ER(RCODE,'wind')
 RCODE = NF90_INQ_VARID(NCID,'Qair',varid)
 call NCDF_ER(RCODE,'Qair')
 RCODE = NF90_GET_VAR(NCID, varid, qair_h,  start=(/ 1,1,1,1 /),count=(/ 1,1,1,i_steps /))
 call NCDF_ER(RCODE,'Qair')
 RCODE = NF90_INQ_VARID(NCID,'PSurf',varid)
 call NCDF_ER(RCODE,'PSurf')
 RCODE = NF90_GET_VAR(NCID, varid, psurf_h_r, start=(/ 1,1,1,1 /),count=(/ 1,1,1,i_steps /))
 call NCDF_ER(RCODE,'PSurf')
 else
 RCODE= NF90_INQ_DIMID(NCID,'tstep',dimid)
 call NCDF_ER(RCODE,'tstep')
 RCODE = NF90_INQUIRE_DIMENSION(NCID, dimid, dimname, dimlength)
 call NCDF_ER(RCODE,'tstep')
 RCODE = NF90_INQ_VARID(NCID,'Wind_N',varid)
 call NCDF_ER(RCODE,'Wind_N')
 RCODE = NF90_GET_VAR(NCID, varid, wind_n_h,  start=(/ 1,1,1,1 /),count=(/ 1,1,1,i_steps /))
 call NCDF_ER(RCODE,'Wind_N')
 RCODE = NF90_INQ_VARID(NCID,'Wind_E',varid)
 call NCDF_ER(RCODE,'Wind_E')
 RCODE = NF90_GET_VAR(NCID, varid, wind_e_h,  start=(/ 1,1,1,1 /),count=(/ 1,1,1,i_steps /))
 call NCDF_ER(RCODE,'Wind_E')
 wind_h(1,1,:) = (wind_n_h(1,1,:)**2 + wind_e_h(1,1,:)**2)**0.5
 RCODE = NF90_INQ_VARID(NCID,'RH',varid)
 call NCDF_ER(RCODE,'RH')
 RCODE = NF90_GET_VAR(NCID, varid, rh_h,    start=(/ 1,1,1,1 /),count=(/ 1,1,1,i_steps /))
 call NCDF_ER(RCODE,'RH')
 RCODE = NF90_INQ_VARID(NCID,'PSurf',varid)
 call NCDF_ER(RCODE,'PSurf')
 RCODE = NF90_GET_VAR(NCID, varid, psurf_h_i, start=(/ 1,1,1,1 /),count=(/ 1,1,1,i_steps /))
 call NCDF_ER(RCODE,'PSurf')
 psurf_h_r = real(psurf_h_i)
 endif

print*,'here'
RCODE = NF90_INQ_VARID(NCID,'time',varid)
call NCDF_ER(RCODE,'time')
RCODE = NF90_GET_VAR(NCID, varid, time)
call NCDF_ER(RCODE,'time')
RCODE = NF90_INQ_VARID(NCID,'nav_lon',varid)
call NCDF_ER(RCODE,'nav_lon')
RCODE = NF90_GET_VAR(NCID, varid, lon)
call NCDF_ER(RCODE,'nav_lon')
RCODE = NF90_INQ_VARID(NCID,'nav_lat',varid)
call NCDF_ER(RCODE,'nav_lat')
RCODE = NF90_GET_VAR(NCID, varid, lat)
call NCDF_ER(RCODE,'nav_lat')
RCODE = NF90_INQ_VARID(NCID,'Tair',varid)
call NCDF_ER(RCODE,'Tair')
RCODE = NF90_GET_VAR(NCID, varid, tair_h,  start=(/ 1,1,1,1 /),count=(/ 1,1,1,i_steps /))
call NCDF_ER(RCODE,'Tair')
RCODE = NF90_INQ_VARID(NCID,'SWdown',varid)
call NCDF_ER(RCODE,'SWdown')
RCODE = NF90_GET_VAR(NCID, varid, swdown_h,start=(/ 1,1,1,1 /),count=(/ 1,1,1,i_steps /))
call NCDF_ER(RCODE,'SWdown')
RCODE = NF90_INQ_VARID(NCID,'LWdown',varid)
call NCDF_ER(RCODE,'LWdown')
RCODE = NF90_GET_VAR(NCID, varid, lwdown_h,start=(/ 1,1,1,1 /),count=(/ 1,1,1,i_steps /))
call NCDF_ER(RCODE,'LWdown')
RCODE = NF90_INQ_VARID(NCID,'Rainf',varid)
call NCDF_ER(RCODE,'Rainf')
RCODE = NF90_GET_VAR(NCID, varid, rainf_h, start=(/ 1,1,1,1 /),count=(/ 1,1,1,i_steps /))
call NCDF_ER(RCODE,'Rainf')

 if(md.eq.1) then
 !convert specific humidity to relative humidity
 !use Buck 1981 for sat vp
 paw_h  = psurf_h_r / (0.62198/qair_h + 1)
 paws_h = 6.1121 * exp(17.502*(tair_h-273.15) / (240.97 + tair_h - 273.15)) * 100
 rh_h   = paw_h/paws_h * 100 
 !print*, psurf_h_r(1,1,1),paw_h(1,1,1), paws_h(1,1,1),tair_h(1,1,1)
 end if

RCODE = NF90_CLOSE(NCID)
call NCDF_ER(RCODE,'close')
!ascii or netcdf endif
endif

!average half-hourly data to get hourly values
!this part of the code is not yet functional
!if(hourly_out) then
!do i=1,i_steps

! tair(1,1,i) = sum(tair_h(1,1,(i*2-1):i*2))/2
! rh(1,1,i) = sum(rh_h(1,1,(i*2-1):i*2))/2
! wind(1,1,i) = sum(wind_h(1,1,(i*2-1):i*2))/2
! swdown(1,1,i) = sum(swdown_h(1,1,(i*2-1):i*2))/2
! lwdown(1,1,i) = sum(lwdown_h(1,1,(i*2-1):i*2))/2
! psurf(1,1,i) = sum(psurf_h(1,1,(i*2-1):i*2))/2
! rainf(1,1,i) = sum(rainf_h(1,1,(i*2-1):i*2))/2

! if(i.lt.10) then
!  print*, tair_h(1,1,(i*2-1):i*2)
!  print*, tair(1,1,i)
! endif

!enddo
!endif


!apply GMT offset
if(gmt_offset.ne.0) then
 if(hourly) then
 tair(1,1,1:(i_steps-gmt_offset)) = tair(1,1,(gmt_offset+1):i_steps)
 tair(1,1,(i_steps-gmt_offset+1):i_steps) = tair(1,1,1:gmt_offset)
 rh(1,1,1:(i_steps-gmt_offset)) = rh(1,1,(gmt_offset+1):i_steps)
 rh(1,1,(i_steps-gmt_offset+1):i_steps) = rh(1,1,1:gmt_offset)
 wind(1,1,1:(i_steps-gmt_offset)) = wind(1,1,(gmt_offset+1):i_steps)
 wind(1,1,(i_steps-gmt_offset+1):i_steps) = wind(1,1,1:gmt_offset)
 swdown(1,1,1:(i_steps-gmt_offset)) = swdown(1,1,(gmt_offset+1):i_steps)
 swdown(1,1,(i_steps-gmt_offset+1):i_steps) = swdown(1,1,1:gmt_offset)
 lwdown(1,1,1:(i_steps-gmt_offset)) = lwdown(1,1,(gmt_offset+1):i_steps)
 lwdown(1,1,(i_steps-gmt_offset+1):i_steps) = lwdown(1,1,1:gmt_offset)
 psurf_r(1,1,1:(i_steps-gmt_offset)) = psurf_r(1,1,(gmt_offset+1):i_steps)
 psurf_r(1,1,(i_steps-gmt_offset+1):i_steps) = psurf_r(1,1,1:gmt_offset)
 rainf(1,1,1:(i_steps-gmt_offset)) = rainf(1,1,(gmt_offset+1):i_steps)
 rainf(1,1,(i_steps-gmt_offset+1):i_steps) = rainf(1,1,1:gmt_offset)
 else
 tair_h(1,1,1:(i_steps-gmt_offset)) = tair_h(1,1,(gmt_offset+1):i_steps)
 tair_h(1,1,(i_steps-gmt_offset+1):i_steps) = tair_h(1,1,1:gmt_offset)
 rh_h(1,1,1:(i_steps-gmt_offset)) = rh_h(1,1,(gmt_offset+1):i_steps)
 rh_h(1,1,(i_steps-gmt_offset+1):i_steps) = rh_h(1,1,1:gmt_offset)
 wind_h(1,1,1:(i_steps-gmt_offset)) = wind_h(1,1,(gmt_offset+1):i_steps)
 wind_h(1,1,(i_steps-gmt_offset+1):i_steps) = wind_h(1,1,1:gmt_offset)
 swdown_h(1,1,1:(i_steps-gmt_offset)) = swdown_h(1,1,(gmt_offset+1):i_steps)
 swdown_h(1,1,(i_steps-gmt_offset+1):i_steps) = swdown_h(1,1,1:gmt_offset)
 lwdown_h(1,1,1:(i_steps-gmt_offset)) = lwdown_h(1,1,(gmt_offset+1):i_steps)
 lwdown_h(1,1,(i_steps-gmt_offset+1):i_steps) = lwdown_h(1,1,1:gmt_offset)
 psurf_h_r(1,1,1:(i_steps-gmt_offset)) = psurf_h_r(1,1,(gmt_offset+1):i_steps)
 psurf_h_r(1,1,(i_steps-gmt_offset+1):i_steps) = psurf_h_r(1,1,1:gmt_offset)
 rainf_h(1,1,1:(i_steps-gmt_offset)) = rainf_h(1,1,(gmt_offset+1):i_steps)
 rainf_h(1,1,(i_steps-gmt_offset+1):i_steps) = rainf_h(1,1,1:gmt_offset)
 endif
endif


ms = 1
!loop through year sequence
do y=s,e
  write(y_c,'(i4)') y
  
  print*, opath, y

  if(mod(y,400).eq.0) then
   leap_yr = .TRUE.
  elseif(mod(y,100).eq.0) then 
   leap_yr = .FALSE.
  elseif(mod(y,4).eq.0) then 
   leap_yr = .TRUE.
  else
   leap_yr = .FALSE.
  endif  

!loop through months
  do m=1,12
!open netcdf
    if(m.lt.10)then
      write(m_c,'(2i1)') 0,m
    else
      write(m_c,'(i2)') m
    endif
    fname = y_c//'-'//m_c//'.nc'
    time_unit = 'days since '//y_c//'-'//m_c//'-01 00:00:00'
!    print*, fname,time_unit
!    print*, ''

    RCODE = NF90_OPEN(trim(opath)//trim(fname), NF90_WRITE, NCID)
    if(verbose)    print*, 'write ', fname
    if(verbose)    print*, nf90_strerror(RCODE)
    RCODE = NF90_INQ_DIMID(NCID,'time',dimid)
    RCODE = NF90_INQUIRE_DIMENSION(NCID, dimid, dimname, dimlength)
!    print*,RCODE
!    print*, dimname, dimlength

!change year stamp
    RCODE = NF90_INQ_VARID(NCID,'time',varid)
    RCODE = NF90_PUT_ATT(NCID, varid, 'units', trim(time_unit))

!find month end subscript for met var arrays
    me = ms + (d_in_m(m))*tstep - 1
    if(dimlength.ne.(me-ms+1)) then
     print*, 'ERROR: dimension calculation'
     print*, y, m 
     print*, 'ncdfdim', dimlength, 'calcdim', me-ms+1
     stop
    endif

!change metdata and attributes
if(hourly) then
    RCODE = NF90_INQ_VARID(NCID,'TBOT',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, tair(1,1,ms:me),start=(/ 1,1,1 /),count=(/ 1,1,dimlength /))
    if(verbose) print*, 'write TBOT ', fname
    if(verbose) print*,  nf90_strerror(RCODE)
!    RCODE = NF90_PUT_ATT(NCID, varid, 'long_name', 'temperature at the lowest atm level (TBOT)')
!    RCODE = NF90_PUT_ATT(NCID, varid, 'units', 'K')
	
    RCODE = NF90_INQ_VARID(NCID,'RH',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, rh(1,1,ms:me),start=(/ 1,1,1 /),count=(/ 1,1,dimlength /))	
!    RCODE = NF90_PUT_ATT(NCID, varid, 'long_name', 'relative humidity at the lowest atm level (RH)')
!    RCODE = NF90_PUT_ATT(NCID, varid, 'units', '%')
	
    RCODE = NF90_INQ_VARID(NCID,'WIND',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, wind(1,1,ms:me),start=(/ 1,1,1 /),count=(/ 1,1,dimlength /))	
!    RCODE = NF90_PUT_ATT(NCID, varid, 'long_name', 'wind at the lowest atm level (WIND)')
!    RCODE = NF90_PUT_ATT(NCID, varid, 'units', 'm/s')
	
    RCODE = NF90_INQ_VARID(NCID,'FSDS',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, SWdown(1,1,ms:me),start=(/ 1,1,1 /),count=(/ 1,1,dimlength /))	
!    RCODE = NF90_PUT_ATT(NCID, varid, 'long_name', 'incident solar (FSDS)')
!    RCODE = NF90_PUT_ATT(NCID, varid, 'units', 'K')
	
    RCODE = NF90_INQ_VARID(NCID,'FLDS',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, LWdown(1,1,ms:me),start=(/ 1,1,1 /),count=(/ 1,1,dimlength /))	
!    RCODE = NF90_PUT_ATT(NCID, varid, 'long_name', 'incident longwave (FLDS)')
!    RCODE = NF90_PUT_ATT(NCID, varid, 'units', 'K')
	
    RCODE = NF90_INQ_VARID(NCID,'PSRF',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, psurf_r(1,1,ms:me),start=(/ 1,1,1 /),count=(/ 1,1,dimlength /))	
!    RCODE = NF90_PUT_ATT(NCID, varid, 'long_name', 'pressure at the lowest atm level (TBOT)')
!    RCODE = NF90_PUT_ATT(NCID, varid, 'units', 'Pa')
	
    RCODE = NF90_INQ_VARID(NCID,'PRECTmms',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, rainf(1,1,ms:me),start=(/ 1,1,1 /),count=(/ 1,1,dimlength /))
!    RCODE = NF90_PUT_ATT(NCID, varid, 'long_name', 'precipitation (PRECTmms)')
!    RCODE = NF90_PUT_ATT(NCID, varid, 'units', 'mm/s')
else
    RCODE = NF90_INQ_VARID(NCID,'TBOT',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, tair_h(1,1,ms:me),start=(/ 1,1,1 /),count=(/ 1,1,dimlength /))
    if(verbose) print*, 'write TBOT ', fname
    if(verbose) print*, nf90_strerror(RCODE)
!    print*, nf90_strerror(RCODE)
!    print*, ms,me,me-ms+1,dimlength
!    RCODE = NF90_PUT_ATT(NCID, varid, 'long_name', 'temperature at the lowest atm level (TBOT)')
!    RCODE = NF90_PUT_ATT(NCID, varid, 'units', 'K')
	
    RCODE = NF90_INQ_VARID(NCID,'RH',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, rh_h(1,1,ms:me),start=(/ 1,1,1 /),count=(/ 1,1,dimlength /))	
!    RCODE = NF90_PUT_ATT(NCID, varid, 'long_name', 'relative humidity at the lowest atm level (RH)')
!    RCODE = NF90_PUT_ATT(NCID, varid, 'units', '%')
	
    RCODE = NF90_INQ_VARID(NCID,'WIND',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, wind_h(1,1,ms:me),start=(/ 1,1,1 /),count=(/ 1,1,dimlength /))	
!    RCODE = NF90_PUT_ATT(NCID, varid, 'long_name', 'wind at the lowest atm level (WIND)')
!    RCODE = NF90_PUT_ATT(NCID, varid, 'units', 'm/s')
	
    RCODE = NF90_INQ_VARID(NCID,'FSDS',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, SWdown_h(1,1,ms:me),start=(/ 1,1,1 /),count=(/ 1,1,dimlength /))	
!    RCODE = NF90_PUT_ATT(NCID, varid, 'long_name', 'incident solar (FSDS)')
!    RCODE = NF90_PUT_ATT(NCID, varid, 'units', 'K')
	
    RCODE = NF90_INQ_VARID(NCID,'FLDS',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, LWdown_h(1,1,ms:me),start=(/ 1,1,1 /),count=(/ 1,1,dimlength /))	
!    RCODE = NF90_PUT_ATT(NCID, varid, 'long_name', 'incident longwave (FLDS)')
!    RCODE = NF90_PUT_ATT(NCID, varid, 'units', 'K')
	
    RCODE = NF90_INQ_VARID(NCID,'PSRF',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, psurf_h_r(1,1,ms:me),start=(/ 1,1,1 /),count=(/ 1,1,dimlength /))	
!    RCODE = NF90_PUT_ATT(NCID, varid, 'long_name', 'pressure at the lowest atm level (TBOT)')
!    RCODE = NF90_PUT_ATT(NCID, varid, 'units', 'Pa')
    if(verbose) print*, 'write PSRF ', psurf_h_r(1,1,ms)
    if(verbose) print*, nf90_strerror(RCODE)
	
    RCODE = NF90_INQ_VARID(NCID,'PRECTmms',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, rainf_h(1,1,ms:me),start=(/ 1,1,1 /),count=(/ 1,1,dimlength /))
!    RCODE = NF90_PUT_ATT(NCID, varid, 'long_name', 'precipitation (PRECTmms)')
!    RCODE = NF90_PUT_ATT(NCID, varid, 'units', 'mm/s')
endif	
	
    RCODE = NF90_INQ_VARID(NCID,'LONGXY',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, lon)	
!    RCODE = NF90_PUT_ATT(NCID, varid, 'long_name', 'longitude')
!    RCODE = NF90_PUT_ATT(NCID, varid, 'units', 'degrees E')
	
    RCODE = NF90_INQ_VARID(NCID,'LATIXY',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, lat)	
!    RCODE = NF90_PUT_ATT(NCID, varid, 'long_name', 'latitude')
!    RCODE = NF90_PUT_ATT(NCID, varid, 'units', 'degrees N')
	
    RCODE = NF90_INQ_VARID(NCID,'EDGEW',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, lon-0.1)	
    RCODE = NF90_INQ_VARID(NCID,'EDGEE',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, lon+0.1)	
    RCODE = NF90_INQ_VARID(NCID,'EDGES',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, lat-0.1)	
    RCODE = NF90_INQ_VARID(NCID,'EDGEN',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, lat+0.1)	
    RCODE = NF90_INQ_VARID(NCID,'ZBOT',varid)
    RCODE = NF90_PUT_VAR(NCID, varid, zbot(1,1,ms:me))	

!close netcdf
    RCODE = NF90_CLOSE(NCID)

!find month start subscript for met var arrays and account for leap years in the input dataset
    ms = me + 1
    if(leap_yr.and.(m.eq.2)) ms = ms + tstep 

!end month
  enddo
!end year
enddo

 close(50)
!end met data type
enddo

end program


subroutine NCDF_ER(RCODE,MSG)

use netcdf
IMPLICIT NONE

INTEGER       RCODE
CHARACTER*5  MSG

if(RCODE.ne.0) print*, nf90_strerror(RCODE), trim(MSG)

end subroutine


 
