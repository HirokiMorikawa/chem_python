#!/bin/bash

filename=$1
filename=${filename##*/}
filename=${filename:0:-4}
echo "$filename"

formchk "$filename.chk" "$filename.fchk"
