#!/bin/bash

pip3 install wheel

xcode-select --install

brew install portaudio

pip3 install pyaudio

pip3 install oauth2client

pip3 install google-api-python-client

pip3 install speechrecognition

file=$(python3 -c "import speech_recognition as _; print(_.__file__)")

sed -i '' 's/            speech_config["speechContexts"] = {"phrases": preferred_phrases}/            speech_config["speechContexts"] = {"phrases": preferred_phrases}/' "${file}"

python3 record.py

git add vids/*

git add tables/*

git commit -mvids

git push
