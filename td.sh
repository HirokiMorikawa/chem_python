#!/bin/bash

filename=$1
dir=$2
# input_dir="./g20191017/input"
# output_dir="./g20191017/output"
input_dir="${dir}/input"
output_dir="${dir}/output"
base_function="cam-b3lyp/6-311+g(d,p)/auto"

# base_function=cam-b3lyp/6-311+g(d,p)/auto
base_function=$3

# ./gaussian.sh python g16_input_file_maker.py -source $filename -calc_type td -calc_func $base_function -desc $input_dir
python g16_input_file_maker.py -source $filename -calc_type td -calc_func $base_function -desc $input_dir


filename=${filename##*/} # パス除去
filename=${filename:0:-4} # .smxyz拡張子除去
./gaussian_runner.sh "${input_dir}/${filename}_ExS.com" $output_dir

