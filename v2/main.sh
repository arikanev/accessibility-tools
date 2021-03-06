#!/bin/bash

declare -a vids=([1]="https://drive.google.com/uc?id=1_YWTi4gTOS6e5AKuGXWopAMUPDFU3IRl" \
                 [2]="https://drive.google.com/uc?id=13H07C201T7gAYH-4UTXd-6uN7yDrHhiU" \
                 [3]="https://drive.google.com/uc?id=1h77J61FKkux1-KuxEGFw6Mz21E2MhHEV" \
                 [4]="https://drive.google.com/uc?id=1OW_mjLYXVOURqQJBj-nXZNnk6NyPAYzs" \
                 [5]="https://drive.google.com/uc?id=1H2zq6jYM2Q8p0Clrj6zKmNhOdsbi3sjG" \
                 [6]="https://drive.google.com/uc?id=1z3AZZMvCLOypx8jLsYJ7rTOlCqQxXU0Q")

for vid in "${!vids[@]}"; do 

    if test -f ./vids/$vid".MOV"; then
        
        echo $vid".MOV exists, skipping download."

    else
        
        gdown "${vids[$vid]}"
        
        find . -maxdepth 1 -name '*.MOV' -exec echo $vid {} >> tables/reference.table \;
        
        find . -maxdepth 1 -name '*.MOV' -exec mv {} ./vids/$vid".MOV" \;

    fi

done


mkdir segments


python3 create_tables.py

declare -a vid2table=([1]=1 [2]=2 [3]=3 [4]=4 [5]=5 [6]=6)

for vt in "${!vid2table[@]}"; do

    python3 create_segs.py -f ./vids/$vt".MOV" -t ./tables/${vid2table[$vt]}".table"

done

