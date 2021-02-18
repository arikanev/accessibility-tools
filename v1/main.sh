#!/bin/bash

mkdir segments
# python3 rand_seg.py
python3 split_vid.py -f jolly_phonics.mp4 -s 5
python3 play_rand.py
