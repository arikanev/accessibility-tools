#!/bin/bash


if test -f "IMG_4654.MOV"; then
    echo "IMG_4654.MOV exists, skipping download."
else
    gdown https://drive.google.com/uc?id=1_YWTi4gTOS6e5AKuGXWopAMUPDFU3IRl
fi
mkdir segments
# python3 rand_seg.py
python3 split_vid.py -f IMG_4654.MOV -t vibrotablecp.txt
# python3 play_rand.py
