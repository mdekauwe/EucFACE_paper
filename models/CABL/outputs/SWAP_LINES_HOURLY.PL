#!/usr/bin/perl -w

# The CABLE header is written in a really tricky way to read as the units come
# after the column headers, making it hard to just skip them

# Solution is to swap these lines around
@line = <>;
( $line[4], $line[5] ) = ( $line[5], $line[4] );
print @line;