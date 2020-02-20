#!/bin/bash

# first argument filename of smiles type(.smiles): パス付きファイル名 拡張子は.smiles 絶対!!
# Gaussian/inputにsmilesから生成した分子のxyz座標で記述されたインプットファイルを出力
# Gaussian/outputにGaussian16で構造最適化した結果ファイルを出力する

filename=$1
# dir=$2
# dir = ./Gaussian/output
dir=$2
# input_dir="./g20191017/input"
# output_dir="./g20191017/output"
input_dir="${dir}/input"
output_dir="${dir}/output"

# When gaussian optimize, used based function.

# base_function="b3lyp/6-311+g(d,p)"
base_function=$3


# 計算対象のsmilesから初期座標を生成して，Gausianのinput_fileを生成する
# その後，構造最適化のプログラムを実行し，最適化後の分子をxyz形式で取り出す．

###########################################################################################

# 1. Input file for Gaussian generate from smiles

# ./gaussian.sh python g16_input_file_maker.py -source $filename -calc_type opt -calc_func $base_function -desc $input_dir
python g16_input_file_maker.py -source $filename -calc_type opt -calc_func $base_function -desc $input_dir

# 2. Molculer coordinates is optimized by Gaussian.

filename=${filename##*/} # パス除去
filename=${filename:0:-7} # .smiles拡張子除去
./optimize_chemical_molecular.sh "${input_dir}/${filename}_GS.com" $output_dir

# 3. Output file in output directory transfor file of xyz structure in input directory.

#filename=${filename##*/} # パス除去
#filename=${filename:0:-4} # 拡張子除去
# ./gaussian.sh obabel -i g09 "${output_dir}/${filename}_GS.log" -o xyz -O "${input_dir}/${filename}.xyz"
# echo $filename
obabel -i g09 "${output_dir}/${filename}_GS.log" -o xyz -O "${input_dir}/${filename}.xyz"
