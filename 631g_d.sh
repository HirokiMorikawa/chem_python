#!/bin/bash

# smilesName="C13H10-フルオレン"
smilesName=$2
dir_name=$1

base_function3="b3lyp/6-31+g(d)"
base_function4="cam-b3lyp/6-31+g(d)/auto"

echo "smileName=${smilesName}"

./optimization.sh "./smiles/${smilesName}.smiles" $dir_name $base_function3
./td.sh "./${dir_name}/input/${smilesName}.xyz" $dir_name $base_function4
