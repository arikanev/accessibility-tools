#!/bin/bash

git config --global user.name "arikanev"

git config --global user.password "Aribenjamin1997!"

python3 record.py -k ../../../key.json

git add vids/*

git add tables/*

git commit -mvids

git push
