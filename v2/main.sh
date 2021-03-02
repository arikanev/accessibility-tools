#!/bin/bash

if test -f "IMG_4654.MOV"; then
    echo "IMG_4654.MOV exists, skipping download."
else
    gdown https://drive.google.com/uc?id=1_YWTi4gTOS6e5AKuGXWopAMUPDFU3IRl
fi

if test -f "vid.MOV"; then
    echo "vid.MOV exists, skipping download."
else
    gdown https://drive.google.com/uc?id=13H07C201T7gAYH-4UTXd-6uN7yDrHhiU
fi


mkdir segments


python3 create_segs.py -f IMG_4654.MOV -t vibrotablecp.txt

python3 create_segs.py -f vid.MOV -t vibrotablecp_2.txt

