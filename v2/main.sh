#!/bin/bash

declare -a vids=([1]="https://drive.google.com/uc?id=1_YWTi4gTOS6e5AKuGXWopAMUPDFU3IRl" \
                 [2]="https://drive.google.com/uc?id=13H07C201T7gAYH-4UTXd-6uN7yDrHhiU" \
                 [3]="https://drive.google.com/uc?id=1h77J61FKkux1-KuxEGFw6Mz21E2MhHEV" \
                 [4]="https://drive.google.com/uc?id=1OW_mjLYXVOURqQJBj-nXZNnk6NyPAYzs" \
                 [5]="https://drive.google.com/uc?id=1H2zq6jYM2Q8p0Clrj6zKmNhOdsbi3sjG" \
                 [6]="https://drive.google.com/uc?id=1z3AZZMvCLOypx8jLsYJ7rTOlCqQxXU0Q")

for vid in "${!vids[@]}"; do 

    if test -f vid+".MOV"; then
        
        echo vid+".MOV exists, skipping download."

    else
        
        gdown "${vids[$vid]}"
    
    fi

done


#if test -f "IMG_4654.MOV"; then
#    echo "IMG_4654.MOV exists, skipping download."
#else
#    gdown https://drive.google.com/uc?id=1_YWTi4gTOS6e5AKuGXWopAMUPDFU3IRl
#fi

#if test -f "vid.MOV"; then
#    echo "vid.MOV exists, skipping download."
#else
#    gdown https://drive.google.com/uc?id=13H07C201T7gAYH-4UTXd-6uN7yDrHhiU
#fi


mkdir segments


python3 create_segs.py -f IMG_4654.MOV -t vibrotablecp.txt

python3 create_segs.py -f vid.MOV -t vibrotablecp_2.txt

