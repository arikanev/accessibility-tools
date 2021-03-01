#!/bin/bash

bash buzz_test.sh 0 21 buzz
bash buzz_test.sh 21 42 buzz
rm running_WER.log

bash haptic_test.sh 0 21 haptic
bash haptic_test.sh 21 42 haptic
rm running_WER.log

bash lipread_test.sh 0 21 lipread
bash lipread_test.sh 21 42 lipread
rm running_WER.log

bash gen_diff.sh # generate differences summary across all devices

bash refresh_stats.sh # remove old log files and create new log file for computing acummulative accuracy
