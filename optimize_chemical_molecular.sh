#!/bin/bash

filename=$1
filename=${filename##*/}
filename=${filename:0:-4}
extention=${filename##*.}

export GAUSS_CDEF="0-11"

input_file="${filename}.com"
check_file="${filename}.chk"

echo $input_file
echo $check_file

g16 $input_file

./chk_to_fchk.sh $check_file

