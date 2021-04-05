#!/bin/bash

brew install portaudio

pip3 install pyaudio

python3 record.py -k ../../../key.json

git add vids/*

git add tables/*

git commit -mvids

git push
