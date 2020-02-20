#!/bin/bash

# smilesName="C13H10-フルオレン"
smilesName="C16H10S2"
dir_name="g20191017"

base_function1="b3lyp/6-311+g(d,p)"
base_function2="cam-b3lyp/6-311+g(d,p)/auto"

./optimization.sh "./mol/${smilesName}.smiles" $dir_name $base_function1
./td.sh "./${dir_name}/input/${smilesName}.xyz" $dir_name $base_function2

mv "${dir_name}/output/C16H10S2_ExS.log" "${dir_name}/output/C16H10S2_1.log"

base_function3="b3lyp/6-31+g(d)"
base_function4="cam-b3lyp/6-31+g(d)/auto"

./optimization.sh "./mol/${smilesName}.smiles" $dir_name $base_function3
./td.sh "./${dir_name}/input/${smilesName}.xyz" $dir_name $base_function4

mv "${dir_name}/output/C16H10S2_ExS.log" "${dir_name}/output/C16H10S2_2.log"
