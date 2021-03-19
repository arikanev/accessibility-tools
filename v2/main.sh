#!/bin/bash

declare -a vids=([1]="https://drive.google.com/uc?id=1kBnA2wt9AmZlSUp223pF2SQ7MApoWIkp" \
                 [2]="https://drive.google.com/uc?id=1XD6c2ztaaNMlysbRmFP1Yb0Vo2p7xJdl" \
                 [3]="https://drive.google.com/uc?id=1ayv9-37x6qzAj4J-kty2gKaFSDtK9shm" \
                 [4]="https://drive.google.com/uc?id=15wn7d8MwHINE9APhVQLCm31oJgHvYLoJ" \
                 [5]="https://drive.google.com/uc?id=1ZbkQ-FMgKTmj7eNThpEcE7urXlJOQ3Cy" \
                 [6]="https://drive.google.com/uc?id=1RMpFxyQgRZ86TTi5IpietBjXLcGzxL6C" \
                 [7]="https://drive.google.com/uc?id=1eKW5sNKEqRtUcBvyrMK1YF8b9PtNBqT8" \
                 [8]="https://drive.google.com/uc?id=1cQeaZg-EhfBHX-QVHhaao9XJ-I-jQiQI" \
                 [9]="https://drive.google.com/uc?id=1h6jaTee3Bdj0Rs6_dWNVONyxXv0xo67P")

# Old links
# 1 https://drive.google.com/uc?id=1_YWTi4gTOS6e5AKuGXWopAMUPDFU3IRl
# 2 https://drive.google.com/uc?id=13H07C201T7gAYH-4UTXd-6uN7yDrHhiU
# 3 https://drive.google.com/uc?id=1h77J61FKkux1-KuxEGFw6Mz21E2MhHEV
# 4 https://drive.google.com/uc?id=1OW_mjLYXVOURqQJBj-nXZNnk6NyPAYzs
# 5 https://drive.google.com/uc?id=1H2zq6jYM2Q8p0Clrj6zKmNhOdsbi3sjG
# 6 https://drive.google.com/uc?id=1z3AZZMvCLOypx8jLsYJ7rTOlCqQxXU0Q

for vid in "${!vids[@]}"; do 

    if test -f ./vids/$vid".MOV"; then
        
        echo $vid".MOV exists, skipping download."

        find ./vids -maxdepth 1 -name $vid'.MOV' -exec echo $vid {} >> tables/reference.table \;

    else
        
        gdown "${vids[$vid]}"
        
        find . -maxdepth 1 -name '*.MOV' -exec echo $vid {} >> tables/reference.table \;
        
        find . -maxdepth 1 -name '*.MOV' -exec mv {} ./vids/$vid".MOV" \;

    fi

done

declare -A tables=([W22]="https://drive.google.com/uc?id=1LuXZuAsODEJYZAFAP8OgDDH6rydwVhq6")

 for table in "${!tables[@]}"; do

    echo $table

    if test -f ./tables/$table".table"; then

        echo $table".table exists, skipping download."

    else

        gdown "${tables[$table]}"

        find . -maxdepth 1 -name '*.table' -exec mv {} ./tables/$table".table" \;

    fi

done

mkdir segments

python3 create_tables.py

declare -a vid2table=([1]=1 [2]=2 [3]=3 [4]=4 [5]=5 [6]=6 [7]=7 [8]=8 [9]=9)

for vt in "${!vid2table[@]}"; do

    python3 create_segs.py -f ./vids/$vt".MOV" -t ./tables/${vid2table[$vt]}".table"

done
