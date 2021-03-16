# accessibility-tools

# Overview
Accessibility-tools is aimed at assisting deaf and hard-of-hearing individuals in learning to read lips, in an isolated setting or in conjunction with other assistive modalities (haptic device, cochlear implant, hearing aid)

# Help with videos
We encourage anyone that is considering helping, to aid to our training data by sending a video of themselves reciting a row of words from the confusable pairs [list](https://docs.google.com/document/d/13GpoYdtYY1n3ucPsyx_2zyGxcx2v8TzOoKCesnsnOow/edit?usp=sharing&resourcekey=0-cTmlGdjAmKiQDlsEhAJNVg). Please send either the video or a downloadable link to it, to accessibility.software@gmail.com

# CLI Install / Setup
## dependencies 

### mac OSX

`brew install ffmpeg portaudio`

`pip3 install pyaudio`

### linux

`sudo apt-get install python-pyaudio python3-pyaudio`

`sudo apt install ffmpeg`

### general requirements (OSX, linux, etc.)

`pip3 install SpeechRecognition gdown pyspellchecker`

# v2

## Download hosted videos, create tables, create segments

`bash main.sh`

## Run a basic session (training, then testing, on specified video segments.)

`python3 play_some_segs.py -i segment0 segment7 segment34 -tr -t -v videoname`

## Documentation (CLI options)

`
  --range RANGE RANGE, -r RANGE RANGE
                        start and end integer range of video segments to select.
                   
  --train, -tr          enables training mode.
  --trainm, -trm        enables modified training mode.
  --test, -t            enables testing mode.
  --numreps NUMREPS, -nr NUMREPS
                        number of times a video segments is repeated during training.
  --shuffle, -s         shuffle selected segments randomly.
  --vname VNAME, -v VNAME
                        name of video file to pull segments from.
  --fname FNAME, -f FNAME
                        name of results file.
  --idxs IDXS [IDXS ...], -i IDXS [IDXS ...]
                        indices of specific video segments to select. If used, overrides range argument.
  --vidxs VIDXS, -vi VIDXS
                        indices of specific video segments to select across all video files specified. (Key-generator).
  --wcor, -wc           modified training mode will now include some testing features (warm up).
`


### Future Steps!

- Lets get youtube sourcing from first version (pytube lib), interfacing with the code in the second version, for increased funcitionality of second version. 
  - Can simply add youtube link to CLI args embedded in bash script, and add arg for youtube link in v2/split_vid.py. The code for downloading youtube vid is in v1/rand_seg.py

- Display speech recognition interface (basically make it easier to capture user speech at correct moments) in dialog/popup boxes
  - dig into SpeechRecognition api, eventually use some sort of more customizable alternative, parratron, live transcribe, something for HOH speech to be understood
  -  https://github.com/speechbrain/speechbrain 
  -  https://speechbrain.github.io

- MPV player should remain open as popup for user input appears after each vid. Try increasing CPU threads to 2 and/or running parallel process.

- Haptic isolation training tool - decrease brightness over time of videos.

- add speech rec as alternative option to text boxes, argparse

### - separate accessibility tool project: TooLoud interface of some sort. (phones or haptics?)
