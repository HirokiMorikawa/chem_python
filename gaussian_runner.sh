#!/bin/bash

# input fileを渡したら，gaussianを実行するプログラム

filename=$1
input_file="${filename}"

filename=${filename##*/}
filename=${filename:0:-4}
# extention=${filename##*.}

out_dir=$2

# export GAUSS_CDEF="0-11"

# input_file="${filename}.com"
output_file="${filename}.log"
# check_file="${filename}.chk"

echo $input_file
#echo "${out_dir}"
#echo "${output_file}"
# echo $check_file
# echo ${out_dir}/${output_file}

g16 $input_file "${out_dir}/${output_file}"

# ./chk_to_fchk.sh $check_file

