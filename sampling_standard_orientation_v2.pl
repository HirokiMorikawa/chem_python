#!/usr/bin/perl

use utf8;
use open ":utf8";

my $filename=$ARGV[0];
print "$filename\n";
open my $file, "<", $filename or die "error open file";

my $optimized_check=0;
my $orientation_check=0;
my $start=0;
my $end=0;
while (my $line = <$file>) {
    if($start == 2 and $end < 1) {
        if($line =~ /-.+-/) {
            $end += 1;
            last;
        }
        print $line;
    }
    if($orientation_check and $start < 2 and $line =~ /-.+-/) {
        $start = $start + 1;
    }
    if($optimized_check and $line =~ /Standard orientation/) {
        $orientation_check=1;
    }
    if($line =~ /Optimized Parameters/) {
        $optimized_check=1;
    }
}
