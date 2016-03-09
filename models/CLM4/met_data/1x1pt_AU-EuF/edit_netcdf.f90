program edit_netcdf

use netcdf

implicit none

integer NCID,RCODE,varid,dimid
integer y,m,z,p,i,dimlength
 character(64) fname,time_unit,path(3),dimname 
 character(4) y_c
 character(2) m_c

real replace(1,1,2000)

z=0
path = (/ '.' , 'AVG' , 'VAR' /)

do i=1,2000
 replace(1,1,i) = 10
enddo

!loop through weather directories
do p=1,1
!loop through year sequence
do y=1850,1850
  write(y_c,'(i4)') y

!loop through months
  do m=1,12
!open netcdf
    if(m.lt.10)then
      write(m_c,'(2i1)') z,m
    else
      write(m_c,'(i2)') m
    endif
    fname = y_c//'-'//m_c//'.nc'
!    time_unit = 'days since '//y_c//'-'//m_c//'-01 00:00:00'
!    print*, fname,time_unit
    print*, ''

    RCODE = NF90_OPEN(trim(path(p))//'/'//trim(fname), NF90_WRITE, NCID)
    print*, trim(path(p))//'/'//trim(fname), nf90_strerror(RCODE)

!inquire time dimension
    RCODE = NF90_INQ_DIMID(NCID,'time',dimid)
    print*, nf90_strerror(RCODE)
    RCODE = NF90_INQUIRE_DIMENSION(NCID, dimid, dimname, dimlength)
    print*, dimlength, nf90_strerror(RCODE)

!change ZBOT
    RCODE = NF90_INQ_VARID(NCID,'ZBOT',varid)
    print*, nf90_strerror(RCODE)
    RCODE = NF90_PUT_VAR(NCID, varid, replace(1,1,1:dimlength),start=(/ 1,1,1 /),count=(/ 1,1,dimlength /))
    print*, nf90_strerror(RCODE)
!close netcdf
    RCODE = NF90_CLOSE(NCID)
!end month
  enddo
!end year
enddo
enddo

end program 
