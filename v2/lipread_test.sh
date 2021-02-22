#!/bin/bash

if test -f "running_WER.log"; then
    echo "running WER exists, this must be continuation testing of the same device"
else
    echo "running WER not found, we must be starting testing on a new device"
    touch running_WER.log
fi

python3 play_some_segs.py -r $1 $2 -s -f lipread
