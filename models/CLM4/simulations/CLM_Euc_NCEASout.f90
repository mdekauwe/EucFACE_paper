!program to covert CLM daily output into a single file required for the NCEAS projects

module ARRAYS

real,allocatable		:: BUFF(:,:),OUT(:,:),SATVP(:),VPD(:)
real,allocatable		:: SWCALC(:),SWC_MM(:),PA_SWC_MM(:),conv_cond(:)
 character*12,allocatable	:: OUTC(:,:)
 character*14,allocatable	:: OUTCCSV(:,:)
 character*32,allocatable	:: otags(:)
endmodule



program NCEAS

use netcdf
use ARRAYS

implicit none

integer, parameter :: OUT_VARS = 88, NFILES = 150

 character	:: SITE_S 
 character*3	:: SITE_AB(4),SIM
 character*10	:: SITE(4),RUN(4), RUNC(4), RUNCI, read_var, get_var,sblank
 character*36	:: IFILE,OFILE,CO2FILE,fmat
 character*36	:: PATH
 character*44	:: PATHF
 character*10	:: OUTVAR(OUT_VARS)
 character*12	:: OUTVARCSV(OUT_VARS)

logical		:: LPYR, owrite
integer		:: STYR_O(4),ENDYR_O(4),STYR(4),ENDYR(4),YEAR,COL,YR,NA,IERR
integer         :: S1,S2,SPYRS,i,y,j,r,d,s,y_i,l,layers,nr,DAYS,D_ARRAY(365)
real		:: ATM_P,LAT,LONG,LMA
real		:: FC(2),WP(2),DEPTH(2),sand,clay
real            :: LAYER_DEPTH(15),theta_satmin(15),psi_satmin(15),beta_min(15)
real            :: theta_sat(15),psi_sat(15),beta(15),theta_wp(15),fom(15)
real            :: conv_C_to_K, conv_pS_to_pD

!functions
real            :: CLM_soil_nd


!netcdf variables
double precision NCDFBUFF(1,1,365),SOIL_WATER(1,1,15,365)

integer NCID, RCODE, varid, RCODE_SW
 character(64) fname_stem,path_stem,fname,RPATH 
 character(4)  endyr_c,y_c

!netcdf error messages
sblank   = '          '
read_var = 'read var'
get_var  = 'get var id'

!program to read CLM netcdf and convert to NCEAS format

!!!WARNING :: BUFF subscripts are otags subscripts + 2 :: WARNING!!!

!write output
owrite = .TRUE.

!allocate space for variable names that are read from the CLM netcdf files
allocate(otags(NFILES))
write(fmat,'(a,i2,a)') "(",OUT_VARS,"(A14))" 

!unit conversions
conv_C_to_K   = 273.15
conv_pS_to_pD = 60*60*24 

!!input section
path = '/home/alp/models/clm4_ornl/run/'

!set simulations to be read 
SITE     = (/ 'AU-EuF','NA','NA','NA' /)
SITE_AB  = (/ 'EUC','NA','NA','NA' /)

RUN      = (/ 'N         ','N_eCO2    ','N_avg     ','N_eCO2_avg' /)
RUNC     = (/ 'AMBVAR','ELEVAR','AMBAVG','ELEAVG' /)

!years needed for input
STYR   = (/ 2012, 2012, 2012, 2012 /)
ENDYR  = (/ 2023, 2023, 2023, 2023 /)

!years needed for output
STYR_O   = STYR
ENDYR_O  = ENDYR

DO d = 1,365
 D_ARRAY(d) = d
ENDDO

!CLM soil
!number of soil layers to include in soil water output calculation
! 6 is down to 0.49 m
! 8 is down to 1.38 m 
! 9 is down to 2.29 m
! 15 is down to 42 m
layers = 9

!EucFACE site specific values
sand   = 80
 clay  = 11
fom    = (/ 0.122,0.127,0.094,0.063,0.041, &
 0.025,0.016,0.010,0.0,0.0,0.0,0.0,0.0,0.0,0.0 /) 

theta_satmin = 0.489 - 0.00126 * sand
psi_satmin   = -10 * ( 10**(1.88 - 0.0131*sand) )
beta_min     = 2.91 + 0.159*clay
theta_sat(:) = (1-fom(:))*theta_satmin + 0.9*fom(:) 
psi_sat(:)   = (1-fom(:))*psi_satmin   - 10.3*fom(:) 
beta(:)      = (1-fom(:))*beta_min     + 2.7*fom(:) 

!SWC at wilting point for each soil layer - the -255000 is water pot (mm) when
!stomata are fully closed in CLM
theta_wp(:)  = theta_sat(:) * (psi_sat(:)/-255000)**(1/beta(:))

!calculate soil layer depths
do l=1,15
 if(l.eq.1)then
  LAYER_DEPTH(l) = 0.5*(CLM_soil_nd(1)+CLM_soil_nd(2))
 elseif(l.eq.15) then
  LAYER_DEPTH(l) = CLM_soil_nd(l)-CLM_soil_nd(l-1)
 else
  LAYER_DEPTH(l) = 0.5*(CLM_soil_nd(l+1)-CLM_soil_nd(l-1))
 endif
enddo

NA     = -9999
ATM_P  = 101300

!chose sites to run
S1 = 1
S2 = 1

!list output variables
OUTVAR(1) = '      YEAR'		
OUTVAR(2) = '       DOY'		
OUTVAR(3) = '       CO2'		
OUTVAR(4) = '       PPT'		
OUTVAR(5) = '       PAR'		
OUTVAR(6) = '        AT'		
OUTVAR(7) = '        ST'		
OUTVAR(8) = '       VPD'		
OUTVAR(9) = '        SW'		
OUTVAR(10) = '      NDEP'		
OUTVAR(11) = '       NEP'		
OUTVAR(12) = '       GPP'		
OUTVAR(13) = '       NPP'		
OUTVAR(14) = '       CEX'		
OUTVAR(15) = '      CVOC'		
OUTVAR(16) = '      RECO'		
OUTVAR(17) = '     RAUTO'		
OUTVAR(18) = '     RLEAF'		
OUTVAR(19) = '     RWOOD'		
OUTVAR(20) = '     RROOT'		
OUTVAR(21) = '     RGROW'
OUTVAR(22) = '      RHET'
OUTVAR(23) = '     RSOIL'
OUTVAR(24) = '        ET'
OUTVAR(25) = '         T'
OUTVAR(26) = '        ES'
OUTVAR(27) = '        EC'
OUTVAR(28) = '        RO'
OUTVAR(29) = '     DRAIN'
OUTVAR(30) = '        LE'
OUTVAR(31) = '        SH'		
OUTVAR(32) = '        CL'		
OUTVAR(33) = '        CW'		
OUTVAR(34) = '       CCR'		
OUTVAR(35) = '       CFR'		
OUTVAR(36) = '       TNC'		
OUTVAR(37) = '     CFLIT'		
OUTVAR(38) = '    CFLITA'		
OUTVAR(39) = '    CFLITB'		
OUTVAR(40) = '    CCLITB'		
OUTVAR(41) = '     CSOIL'		
OUTVAR(42) = '        GL'		
OUTVAR(43) = '        GW'		
OUTVAR(44) = '       GCR'		
OUTVAR(45) = '        GR'		
OUTVAR(46) = '     GREPR'
OUTVAR(47) = '   CLLFALL'		
OUTVAR(48) = '    CCRLIN'
OUTVAR(49) = '    CFRLIN'
OUTVAR(50) = '      CWIN'		
OUTVAR(51) = '       LAI'		
OUTVAR(52) = '       LMA'		
OUTVAR(53) = '      NCON'		
OUTVAR(54) = '      NCAN'		
OUTVAR(55) = '     NWOOD'		
OUTVAR(56) = '       NCR'		
OUTVAR(57) = '       NFR'		
OUTVAR(58) = '     NSTOR'		
OUTVAR(59) = '      NLIT'	
OUTVAR(60) = '     NRLIT'		
OUTVAR(61) = '       NDW'	
OUTVAR(62) = '     NSOIL'		
OUTVAR(63) = '    NPOOLM'		
OUTVAR(64) = '    NPOOLO'		
OUTVAR(65) = '      NFIX'		
OUTVAR(66) = '    NLITIN'		
OUTVAR(67) = '     NWLIN'
OUTVAR(68) = '    NCRLIN'
OUTVAR(69) = '    NFRLIN'
OUTVAR(70) = '       NUP'		
OUTVAR(71) = '     NGMIN'		
OUTVAR(72) = '      NMIN'		
OUTVAR(73) = '      NVOL'		
OUTVAR(74) = '    NLEACH'		
OUTVAR(75) = '       NGL'		
OUTVAR(76) = '       NGW'		
OUTVAR(77) = '      NGCR'		
OUTVAR(78) = '       NGR'
OUTVAR(79) = '     APARd'
OUTVAR(80) = '       GCd'
OUTVAR(81) = '       GAd'
OUTVAR(82) = '       GBd'
OUTVAR(83) = '     Betad'
OUTVAR(84) = ' NLRETRANS'
OUTVAR(85) = ' NWRETRANS'
OUTVAR(86) = 'NCRRETRANS'
OUTVAR(87) = 'NFRRETRANS'
OUTVAR(88) = '    PotGPP'

!list netcdf names for each variable - add 2 to get subscript in BUFF array
otags(1)  = 'PCO2'
otags(2)  = 'RAINATM'
otags(3)  = 'SNOWATM'
otags(4)  = 'FSDS'    
otags(5)  = 'TSA'
otags(6)  = 'TSOI_10CM'
otags(7)  = 'PSurf'
otags(8)  = 'RH2M'
otags(9)  = 'SMOIST'  !top 30cm 
otags(10) = 'H2OSOI'
otags(11) = 'NDEP_TO_SMINN'
otags(12) = 'NEP'
otags(13) = 'GPP'
otags(14) = 'NPP'
otags(15) = 'VOCFLXT'
otags(16) = 'ER'
otags(17) = 'AR'
otags(18) = 'LEAF_MR'
otags(19) = 'LIVESTEM_MR'
otags(20) = 'LIVECROOT_MR'
otags(21) = 'GR'
otags(22) = 'HR'
otags(23) = 'SR'
otags(24) = 'QVEGE'
otags(25) = 'QVEGT'
otags(26) = 'QSOIL'
otags(27) = 'QRUNOFF'
otags(28) = 'QSNWCPICE'
otags(29) = 'QDRAI'
otags(30) = 'FCTR'
otags(31) = 'FCEV'
otags(32) = 'FSH'
otags(33) = 'LEAFC'
otags(34) = 'LIVESTEMC'
otags(35) = 'DEADSTEMC'
otags(36) = 'LIVECROOTC'
otags(37) = 'DEADCROOTC'
otags(38) = 'FROOTC'
otags(39) = 'CPOOL'
otags(40) = 'XSMRPOOL'      !is this the negative pool?
otags(41) = 'GRESP_STORAGE' !all the tissue storage pools!!
otags(42) = 'LITTERC'
otags(43) = 'LITR1C'
otags(44) = 'LITR2C'
otags(45) = 'LITR3C'
otags(46) = 'CWDC'
otags(47) = 'SOILC'
otags(48) = 'LEAFC_ALLOC'
otags(49) = 'WOODC_ALLOC'
otags(50) = 'FROOTC_ALLOC'
otags(51) = 'LEAFC_LOSS'
otags(52) = 'FROOTC_LOSS'
otags(53) = 'WOODC_LOSS'
otags(54) = 'TLAI'
otags(55) = 'SLASUN'
otags(56) = 'SLASHA'
otags(57) = 'LEAFN'
otags(58) = 'LIVESTEMN'
otags(59) = 'DEADSTEMN'
otags(60) = 'LIVECROOTN'
otags(61) = 'DEADCROOTN'
otags(62) = 'FROOTN'
otags(63) = 'NPOOL'
otags(64) = 'RETRANSN'
otags(65) = 'LITR1N'
otags(66) = 'LITR2N'
otags(67) = 'LITR3N'
otags(68) = 'CWDN'
otags(69) = 'SMINN'        !total, output requested for top 30 cm only
otags(70) = 'SOIL1N'
otags(71) = 'SOIL2N'
otags(72) = 'SOIL3N'
otags(73) = 'SOIL4N'
otags(74) = 'NFIX_TO_SMINN'
otags(75) = 'LEAFN_TO_LITTER' !shouldn't this be loss?
otags(76) = 'FROOTN_TO_LITTER'
otags(77) = 'SMINN_TO_PLANT'
otags(78) = 'GROSS_NMIN'
otags(79) = 'NET_NMIN'
otags(80) = 'DENIT'
otags(81) = 'SMINN_LEACHED'
otags(82) = 'NPOOL_TO_LEAFN'
otags(83) = 'NPOOL_TO_LIVESTEMN'
otags(84) = 'NPOOL_TO_DEADSTEMN'
otags(85) = 'NPOOL_TO_LIVECROOTN'
otags(86) = 'NPOOL_TO_DEADCROOTN'
otags(87) = 'PARSUN'          !multiplied by LAISUN
otags(88) = 'PARSHA'          !ditto
otags(89) = 'LAISUN'
otags(90) = 'LAISHA'
otags(91) = 'FGEV'
otags(92) = 'LEAFC_XFER_TO_LEAFC'
otags(93) = 'FROOTC_XFER_TO_FROOTC'
otags(94) = 'LIVESTEMC_XFER_TO_LIVESTEMC'
otags(95) = 'DEADSTEMC_XFER_TO_DEADSTEMC'
otags(96) = 'LIVECROOTC_XFER_TO_LIVECROOTC'
otags(97) = 'DEADCROOTC_XFER_TO_DEADCROOTC'
otags(98) = 'LEAFN_XFER_TO_LEAFN'
otags(99) = 'FROOTN_XFER_TO_FROOTN'
otags(100) = 'LIVESTEMN_XFER_TO_LIVESTEMN'
otags(101) = 'DEADSTEMN_XFER_TO_DEADSTEMN'
otags(102) = 'LIVECROOTN_XFER_TO_LIVECROOTN'
otags(103) = 'DEADCROOTN_XFER_TO_DEADCROOTN'
otags(104) = 'RSSUN'
otags(105) = 'RSSHA'
otags(106) = 'RAM1'
otags(107) = 'BTRAN'
otags(108) = 'RB1'
otags(109) = 'FPSN'
otags(110) = 'LEAFC_XFER'
otags(111) = 'FROOTC_XFER'
otags(112) = 'LIVESTEMC_XFER'
otags(113) = 'DEADSTEMC_XFER'
otags(114) = 'LIVECROOTC_XFER'
otags(115) = 'DEADCROOTC_XFER'
otags(116) = 'LEAFN_XFER'
otags(117) = 'FROOTN_XFER'
otags(118) = 'LIVESTEMN_XFER'
otags(119) = 'DEADSTEMN_XFER'
otags(120) = 'LIVECROOTN_XFER'
otags(121) = 'DEADCROOTN_XFER'
otags(122) = 'LEAFC_STORAGE'
otags(123) = 'FROOTC_STORAGE'
otags(124) = 'LIVESTEMC_STORAGE'
otags(125) = 'DEADSTEMC_STORAGE'
otags(126) = 'LIVECROOTC_STORAGE'
otags(127) = 'DEADCROOTC_STORAGE'
otags(128) = 'LEAFN_STORAGE'
otags(129) = 'FROOTN_STORAGE'
otags(130) = 'LIVESTEMN_STORAGE'
otags(131) = 'DEADSTEMN_STORAGE'
otags(132) = 'LIVECROOTN_STORAGE'
otags(133) = 'DEADCROOTN_STORAGE'
otags(134) = 'NPOOL_TO_FROOTN'
otags(135) = 'CPOOL_TO_LEAFC'
otags(136) = 'CPOOL_TO_FROOTC'
otags(137) = 'CPOOL_TO_LIVESTEMC'
otags(138) = 'CPOOL_TO_DEADSTEMC'
otags(139) = 'CPOOL_TO_LIVECROOTC'
otags(140) = 'CPOOL_TO_DEADCROOTC'
otags(141) = 'LEAFN_TO_RETRANSN'
otags(142) = 'LIVESTEMN_TO_RETRANSN'
otags(143) = 'LIVECROOTN_TO_RETRANSN'
otags(144) = 'FROOT_MR'
otags(145) = 'CROOTC_LOSS'
otags(146) = 'STEMC_LOSS'
otags(147) = 'CROOTN_TO_LITTER'
otags(148) = 'STEMN_TO_LITTER'
otags(149) = 'M_LEAFN_TO_LITTER' 
otags(150) = 'M_FROOTN_TO_LITTER'

OUTVARCSV(:)  = OUTVAR(:)//' ,'

!site loop
do s = S1,S2

print*, ''
print*, SITE(s)

days = (endyr(s)-styr(s)+1)*365
print*, 'days in simulation', days
print*, ''


!run loop
do r = 1,4
print*, RUN(r)

!allocate arrays
allocate(BUFF(DAYS,NFILES+2))
BUFF(:,:) = NA
allocate(SWCALC(DAYS))
SWCALC(:) = 0.0d0
allocate(SWC_MM(DAYS))
SWC_MM(:) = 0.0d0
allocate(PA_SWC_MM(DAYS))
PA_SWC_MM(:) = 0.0d0
allocate(SATVP(DAYS))

allocate(VPD(DAYS))
allocate(OUT(DAYS,OUT_VARS))
allocate(OUTC(DAYS,OUT_VARS))
allocate(OUTCCSV(DAYS,OUT_VARS))
allocate(conv_cond(DAYS))



path_stem  = '/'//trim(SITE(s))//'_I20TRC'//trim(RUN(r))
RPATH=trim(PATH)//trim(path_stem)//'/run/'
RPATH='.'//trim(path_stem)//'/run/'
RUNCI=RUNC(r)
print*, RUN(r), RUNCI
OFILE   = 'D1CLM4'//SITE_AB(s)//trim(RUNCI)//'.csv'
print*, RPATH, OFILE

if(owrite) then
open(30,file=trim(RPATH)//OFILE,status="replace",action="write")
write(30,fmat) (OUTVARCSV(i),i=1,OUT_VARS)
endif

SOIL_WATER = NA

!year loop
y_i = 0
do y = STYR(s),ENDYR(s)
y_i = y_i + 1

print*,  y

!write time data
BUFF(((y_i-1)*365)+1:(y_i*365),1) = STYR_O(s) + y_i - 1
BUFF(((y_i-1)*365)+1:(y_i*365),2) = d_array(:)

!open CLM netdcdf file
write(y_c,'(I4)') y
fname = trim(site(s))//'_I20TRC'//trim(run(r))//'.clm2.h0.'//y_c//'-01-01-00000.nc'
RCODE = NF90_OPEN(trim(rpath)//trim(fname), NF90_WRITE, NCID)
 call netdcf_error(RCODE,trim(fname),sblank)

!access each variable and add to the buffer array
        do i = 3,NFILES+2
        !get variable
        RCODE = NF90_INQ_VARID(NCID,trim(otags(i-2)),varid)
        if(RCODE.ne.0) varid = NA
        if(y.eq.STYR(s)) call netdcf_error_warning(RCODE,fname,trim(otags(i-2)),get_var)
                !if otags(10) i.e. H2OSOI
                if(i.eq.12)then
                RCODE = NF90_GET_VAR(NCID, varid, SOIL_WATER,start=(/ 1,1,1,1 /),count=(/ 1,1,15,365 /))
                if(y.eq.STYR(s)) call netdcf_error_warning(RCODE,fname,trim(otags(i-2)),read_var)
                RCODE_SW = RCODE
                        do l = 1,layers
                        !calculate the mean soil water content up to layer 'layers' weighted by layer depth 
                        SWCALC((((y_i-1)*365)+1):(y_i*365)) = SWCALC((((y_i-1)*365)+1):(y_i*365)) &
 + SOIL_WATER(1,1,l,:)*LAYER_DEPTH(l)/sum(LAYER_DEPTH(1:layers))
                        !calculate total soil water  
                        SWC_MM((((y_i-1)*365)+1):(y_i*365)) = SWC_MM((((y_i-1)*365)+1):(y_i*365)) &
 + SOIL_WATER(1,1,l,:)*LAYER_DEPTH(l)*1000
                        !calculate plant available soil water  
                        PA_SWC_MM((((y_i-1)*365)+1):(y_i*365)) = PA_SWC_MM((((y_i-1)*365)+1):(y_i*365)) &
 + (SOIL_WATER(1,1,l,:) - theta_wp(l))*LAYER_DEPTH(l)*1000
                        enddo
                BUFF((((y_i-1)*365)+1):(y_i*365),i) = SWCALC(:) 
                else
                RCODE = NF90_GET_VAR(NCID, varid, NCDFBUFF)
                if(y.eq.STYR(s)) call netdcf_error_warning(RCODE,fname,trim(otags(i-2)),read_var)
                BUFF((((y_i-1)*365)+1):(y_i*365),i) = NCDFBUFF(1,1,:) 
                endif       
        enddo
RCODE = NF90_CLOSE(NCID)
 call netdcf_error_warning(RCODE,trim(fname),sblank,sblank)

!output soil water data and calculations
if(y.eq.STYR(s)) then 
print*, trim(otags(12-2)), RCODE_SW 
print*, SOIL_WATER(1,1,:,1)
print*, 'SWC = ', SWCALC(1), 'SW_mm = ', SWC_MM(1), 'plant avaialble SW_mm = ',&
PA_SWC_MM(1)
print*, 'total layer depth = ', sum(LAYER_DEPTH(1:layers))
print*, LAYER_DEPTH(1:layers)
endif

!year loop
enddo	
print*, ''
 
!convert CLM data to NCEAS units and variables for output
!BUFF variable subscripts are the otags subscrips + 2

!convert RH to mean VPD over 24 hours using Flatau et al 1992 equation
SATVP(:) = (6.11213476+                               &
  4.44007856*10**-1   * (BUFF(:,7)- conv_C_to_K)+     &
  1.43064234*10**-2   * (BUFF(:,7)- conv_C_to_K)**2+  &
  2.64461437*10**-4   * (BUFF(:,7)- conv_C_to_K)**3+  &
  3.05903558*10**-6   * (BUFF(:,7)- conv_C_to_K)**4+  &
  1.96237241*10**-8   * (BUFF(:,7)- conv_C_to_K)**5+  &
  8.92344772*10**-11  * (BUFF(:,7)- conv_C_to_K)**6+  &
  -3.73208410*10**-13 * (BUFF(:,7)- conv_C_to_K)**7+  &
  2.09339997*10**-16  * (BUFF(:,7)- conv_C_to_K)**8   &
  )/10

VPD(:)   = SATVP(:)*(1-(BUFF(:,10)/100))

!time vars
OUT(:,1) = BUFF(:,1)
OUT(:,2) = BUFF(:,2)
!driving/environmental vars	
OUT(:,3) = BUFF(:,3)/BUFF(:,9)*1000000               !can change to actual pressure when accessed                                           	
OUT(:,4) = (BUFF(:,4)+BUFF(:,5)) * conv_pS_to_pD
OUT(:,5) = BUFF(:,6) * 2.3 * conv_pS_to_pD * 1e-6     !PAR conversion:: w/m-2 to molm-2d-1                          		
OUT(:,6) = BUFF(:,7) - conv_C_to_K
OUT(:,7) = BUFF(:,8) - conv_C_to_K
OUT(:,8) = VPD(:)
!OUT(:,9) = (BUFF(:,12)-WP(s)*DEPTH(s))/(FC(s)*DEPTH(s)-WP(s)*DEPTH(s))*100	!soil water as a percentage of field capacity - wilting point	
!OUT(:,9)  = SWC_MM(:)	               !total soil water in soil layers 1:layers (mm)	
OUT(:,9)  = PA_SWC_MM(:)      !plant available soil water in soil layers 1:layers (mm)	
OUT(:,10) = BUFF(:,13) * conv_pS_to_pD
!productivity
OUT(:,11) = BUFF(:,14) * conv_pS_to_pD 
OUT(:,12) = BUFF(:,15) * conv_pS_to_pD 
OUT(:,13) = BUFF(:,16) * conv_pS_to_pD 
OUT(:,14) = NA           
!OUT(:,15) = BUFF(:,17) * 24 / 1e6 !coverts from ug m-2 h-1
OUT(:,15) = NA 
!respiration fluxes			
OUT(:,16) = BUFF(:,18) * conv_pS_to_pD
OUT(:,17) = BUFF(:,19) * conv_pS_to_pD
OUT(:,18) = BUFF(:,20) * conv_pS_to_pD
OUT(:,19) = (BUFF(:,21) + BUFF(:,22)) * conv_pS_to_pD ! wood and croot respiration
OUT(:,20) = BUFF(:,146) * conv_pS_to_pD
OUT(:,21) = BUFF(:,23) * conv_pS_to_pD
OUT(:,22) = BUFF(:,24) * conv_pS_to_pD
OUT(:,23) = BUFF(:,25) * conv_pS_to_pD
!water fluxes
OUT(:,24) = (BUFF(:,26)+BUFF(:,27)+BUFF(:,28)) * conv_pS_to_pD 
OUT(:,25) = BUFF(:,27) * conv_pS_to_pD
OUT(:,26) = BUFF(:,28) * conv_pS_to_pD
OUT(:,27) = BUFF(:,26) * conv_pS_to_pD
OUT(:,28) = (BUFF(:,29)+BUFF(:,30)-BUFF(:,31)) * conv_pS_to_pD
OUT(:,29) = BUFF(:,31) * conv_pS_to_pD
OUT(:,30) = (BUFF(:,32)+BUFF(:,33)+BUFF(:,93)) * conv_pS_to_pD / 1000000 !in CLM output file these vars are scaled by urbanf which probably means they are only urban variables?
OUT(:,31) = BUFF(:,34) * conv_pS_to_pD / 1000000
!carbon pools		
OUT(:,32) = BUFF(:,35) 
OUT(:,33) = BUFF(:,36)+BUFF(:,37)
OUT(:,34) = BUFF(:,38)+BUFF(:,39)
OUT(:,35) = BUFF(:,40)
OUT(:,36) = BUFF(:,41)+BUFF(:,42)+BUFF(:,43)+ &
!            BUFF(:,124)+BUFF(:,125)+BUFF(:,126)+BUFF(:,127)+BUFF(:,128)+BUFF(:,129)+ &
            BUFF(:,112)+BUFF(:,113)+BUFF(:,114)+BUFF(:,115)+BUFF(:,116)+BUFF(:,117)
OUT(:,37) = BUFF(:,44)                       !does this include wood litter C? 		
OUT(:,38) = NA
OUT(:,39) = BUFF(:,45)+BUFF(:,46)+BUFF(:,47)
OUT(:,40) = BUFF(:,48)
OUT(:,41) = BUFF(:,49)
!tissue specific carbon fluxes	
OUT(:,42) = (BUFF(:,137) + BUFF(:,94)) * conv_pS_to_pD
OUT(:,43) = (BUFF(:,139) + BUFF(:,140) + BUFF(:,96) + BUFF(:,97)) * conv_pS_to_pD
OUT(:,44) = (BUFF(:,141) + BUFF(:,142) + BUFF(:,98) + BUFF(:,99)) * conv_pS_to_pD
OUT(:,45) = (BUFF(:,138) + BUFF(:,95)) * conv_pS_to_pD
!OUT(:,42) = BUFF(:,50) * conv_pS_to_pD       		
!OUT(:,43) = BUFF(:,51) * conv_pS_to_pD       !wood and coarse root allocation
!OUT(:,44) = NA                               !coarse root allocation is included in wood allocation		
!OUT(:,45) = BUFF(:,52) * conv_pS_to_pD       
OUT(:,46) = NA 
OUT(:,47) = BUFF(:,53)  * conv_pS_to_pD
OUT(:,48) = BUFF(:,147) * conv_pS_to_pD
OUT(:,49) = BUFF(:,54)  * conv_pS_to_pD
OUT(:,50) = BUFF(:,148) * conv_pS_to_pD     !wood litter
!LAI etc
OUT(:,51) = BUFF(:,56)
OUT(:,52) = BUFF(:,35)/BUFF(:,56)                                  !LEAFC/TLAI
OUT(:,53) = BUFF(:,59)/BUFF(:,35)
!nitrogen pools		
OUT(:,54) = BUFF(:,59)
OUT(:,55) = BUFF(:,60)+BUFF(:,61)
OUT(:,56) = BUFF(:,62)+BUFF(:,63)
OUT(:,57) = BUFF(:,64)
OUT(:,58) = BUFF(:,65)+BUFF(:,66) + &
            BUFF(:,130)+BUFF(:,131)+BUFF(:,132)+BUFF(:,133)+BUFF(:,134)+BUFF(:,135)+ &
            BUFF(:,118)+BUFF(:,119)+BUFF(:,120)+BUFF(:,121)+BUFF(:,122)+BUFF(:,123)
OUT(:,59) = NA
OUT(:,60) = BUFF(:,67)+BUFF(:,68)+BUFF(:,69)
OUT(:,61) = BUFF(:,70)
OUT(:,62) = BUFF(:,71)+BUFF(:,72)+BUFF(:,73)+BUFF(:,74)+BUFF(:,75) !supposed to be top 30 cm of the soil only
OUT(:,63) = BUFF(:,71) !ditto
OUT(:,64) = BUFF(:,72)+BUFF(:,73)+BUFF(:,74)+BUFF(:,75) !ditto		
!nitrogen fluxes
OUT(:,65) = BUFF(:,76) * conv_pS_to_pD
OUT(:,66) = (BUFF(:,77)+BUFF(:,151)) * conv_pS_to_pD   ! leaf litter N - may neglect fire and perhaps mortality losses?
OUT(:,67) = BUFF(:,150) * conv_pS_to_pD               ! wood litter N
OUT(:,68) = BUFF(:,149) * conv_pS_to_pD               ! croot litter N
OUT(:,69) = (BUFF(:,78)+BUFF(:,152)) * conv_pS_to_pD  ! froot litter N
OUT(:,70) = BUFF(:,79) * conv_pS_to_pD
OUT(:,71) = BUFF(:,80) * conv_pS_to_pD
OUT(:,72) = BUFF(:,81) * conv_pS_to_pD
OUT(:,73) = BUFF(:,82) * conv_pS_to_pD
OUT(:,74) = BUFF(:,83) * conv_pS_to_pD
OUT(:,75) = (BUFF(:,84) + BUFF(:,100)) * conv_pS_to_pD
OUT(:,76) = (BUFF(:,85) + BUFF(:,86) + BUFF(:,102) + BUFF(:,103)) * conv_pS_to_pD
OUT(:,77) = (BUFF(:,87) + BUFF(:,88) + BUFF(:,104) + BUFF(:,105)) * conv_pS_to_pD
OUT(:,78) = (BUFF(:,136) + BUFF(:,101)) * conv_pS_to_pD
!APAR & conductances   
!conversion factor for ms-1 to molm-2s-1
conv_cond(:) = BUFF(:,9) / (8.314*BUFF(:,7)) 
OUT(:,79) = ( BUFF(:,89)*BUFF(:,91)+BUFF(:,90)*BUFF(:,92) ) * 2.3 * conv_pS_to_pD * 1e-6
OUT(:,80) = (BUFF(:,91)/BUFF(:,106) + BUFF(:,92)/BUFF(:,107)) * conv_cond(:)
OUT(:,81) = (1/BUFF(:,108)) * conv_cond(:)
OUT(:,82) = (1/BUFF(:,110)) * conv_cond(:)
OUT(:,83) = BUFF(:,109)
OUT(:,84) = BUFF(:,143) * conv_pS_to_pD
OUT(:,85) = BUFF(:,144) * conv_pS_to_pD
OUT(:,86) = BUFF(:,145) * conv_pS_to_pD
OUT(:,87) = NA 
OUT(:,88) = BUFF(:,111) * 12e-6 * conv_pS_to_pD  !convert umolm-2s-1 to gm-2d-1

!write output
write(OUTC(:,:),'(f12.6)') OUT(:,:)
OUTCCSV = OUTC//' ,'

if(owrite) then
do d=1,days
  write(30,fmat) OUTCCSV(d,:)
enddo
endif 

deallocate(BUFF)
deallocate(OUT)
deallocate(OUTC)
deallocate(OUTCCSV)
deallocate(SATVP)
deallocate(VPD)
deallocate(conv_cond)
deallocate(SWCALC)
deallocate(SWC_MM)
deallocate(PA_SWC_MM)

 close(30)

!run loop
enddo

!site loop
enddo

!the number of repeats in these formats should equal OUT_VARS		
!100 format (fmat)
!101 format (fmat)

end program



subroutine LPYEAR(YEAR,LPYR)

implicit none

integer :: YEAR
logical :: LPYR

if(mod(YEAR,4).ne.0) then
LPYR = .FALSE.
else
LPYR = .TRUE.
endif

if(mod(YEAR,100).eq.0) LPYR = .FALSE.
if(mod(YEAR,400).eq.0) LPYR = .TRUE.

end subroutine


subroutine netdcf_error(RCODE,fname,statement)

use netcdf

implicit none

integer RCODE
 character(64) fname,statement

if(RCODE.ne.0) then
 print*, 'ERROR:: on ', fname
 print*, nf90_strerror(RCODE)
 print*, statement
 print*, 'FORTRAN stop'
 stop
endif

end subroutine


subroutine netdcf_error_warning(RCODE,char1,char2,char3)

use netcdf

implicit none

integer RCODE
 character(64) char1
 character(10) char2,char3

if(RCODE.ne.0) then
 print*, 'ERROR:: on ' , char1
 print*, nf90_strerror(RCODE)
 print*, char2 , char3
endif

 char2 = '          '
 char3 = '          '

end subroutine


function CLM_soil_nd(layer)

implicit none

real CLM_soil_nd
integer layer

 CLM_soil_nd = 0.025*(exp(0.5*(layer-0.5))-1)

end function



 
