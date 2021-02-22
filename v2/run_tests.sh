#!/bin/bash

bash buzz_test.sh 0 21
bash buzz_test.sh 21 42
rm running_WER.log
bash haptic_test.sh 0 21
bash haptic_test.sh 21 42
rm running_WER.log
bash lipread_test.sh 0 21
bash lipread_test.sh 21 42
rm running_WER.log
