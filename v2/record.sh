#!/bin/bash

pip3 install wheel

xcode-select --install

brew install portaudio

pip3 install pyaudio

pip3 install oauth2client

pip3 install google-api-python-client

python3 record.py

git add vids/*

git add tables/*

git commit -mvids

git push
