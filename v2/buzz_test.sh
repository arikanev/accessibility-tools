#!/bin/bash

if test -f "running_WER.log"; then
    rm running_WER.log
else
    touch running_WER.log
fi

python3 play_some_segs.py -r $1 $2 -s -f buzz
