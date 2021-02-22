#!/bin/bash

cat *summary* >> diff_summary.log # generate differences summary across all devices

bash refresh_stats.sh # remove old log files and create new log file for computing acummulative WER
