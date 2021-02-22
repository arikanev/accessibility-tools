#!/bin/bash

if test -f "running_WER.log"; then
    rm running_WER.log
else
    touch running_WER.log
fi
