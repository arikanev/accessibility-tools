#!/bin/bash

mkdir segments
# python3 rand_seg.py
python3 split_vid.py -f IMG_4654.MOV -t vibrotablecp.txt
# python3 play_rand.py
