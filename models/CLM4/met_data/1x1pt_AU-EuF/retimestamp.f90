program retimestamp_metdata

use netcdf

implicit none

integer NCID, RCODE, varid
integer y,m,z,p
 character(64) fname,time_unit,path(3) 
 character(4) y_c
 character(2) m_c

z=0
path = (/ '.' , 'AVG' , 'VAR' /)

!loop through weather directories
do p=1,1
!loop through year sequence
do y=1850,2011
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
    time_unit = 'days since '//y_c//'-'//m_c//'-01 00:00:00'
    print*, fname,time_unit
    print*, ''

    RCODE = NF90_OPEN(trim(path(p))//'/'//trim(fname), NF90_WRITE, NCID)

!change year stamp
    RCODE = NF90_INQ_VARID(NCID,'time',varid)
    RCODE = NF90_PUT_ATT(NCID, varid, 'units', trim(time_unit))
!close netcdf
    RCODE = NF90_CLOSE(NCID)
!end month
  enddo
!end year
enddo
enddo

end program 
