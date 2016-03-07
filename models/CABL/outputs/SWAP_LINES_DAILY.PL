#!/usr/bin/perl -w

# The CABLE header is written in a really tricky way to read as the units come
# after the column headers, making it hard to just skip them

# Solution is to swap these lines around
@line = <>;
( $line[6], $line[7] ) = ( $line[7], $line[6] );
print @line;