#!/bin/bash

python3 record.py

cd ./tables/

num=$(ls -1 | wc -l)

cd ..

python3 create_segs.py -f "./vids/${num// /}.MOV" -t "./tables/${num// /}.table"
