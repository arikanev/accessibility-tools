# accessibility-tools

# Overview
Accessibility-tools is aimed at assisting deaf and hard-of-hearing individuals in learning to read lips, in an isolated setting or in conjunction with other assistive modalities (haptic device, cochlear implant, hearing aid).

# Help with videos
We encourage anyone that is considering helping, to add to our training data by sending a video of themselves reciting a **column** of words from the confusable pairs [list](https://docs.google.com/document/d/1RfgYMfz1IBhVNNRd84miKrfkIJbT7OiZ_k-w_hcaF0A/edit?usp=sharing). Please send either the video or a downloadable link to it, to arikanevsky@gmail.com.

[Current video archive](https://drive.google.com/drive/folders/1ALMMmjeSFkHpLxhxc-r0llzCmVpYWe4O?usp=sharing)

# CLI Install / Setup

### mac OSX

`brew install ffmpeg portaudio`

`pip3 install pyaudio`

### linux

`sudo apt-get install python-pyaudio python3-pyaudio`

`sudo apt install ffmpeg`

### general requirements (OSX, linux, etc.)

`pip3 install SpeechRecognition gdown pyspellchecker`

## v2 quick start

### Download hosted videos, create tables, create segments

`bash main.sh`

### Run a basic session (training, then testing, on specified video segments.)

`python3 play_some_segs.py -i segment0 segment7 segment34 -tr -t -v videoname`


# Documentation

### Training `(--train)`

User is presented each selected video segment, with no "quiz" between videos to determine users ability and understanding what the speaker has just said.

This mode is purely for the user to get familiar with the corpus.

### Modified training `(--trainm)`

User is presented each selected video segment twice in succession (First, without captions, second with captions), with no "quiz" between videos to determine users ability and understanding what the speaker has just said.

This mode is purely for the user to gauge their own skill/ability.

### Modified training with correct `(--trainm --wcor)`

User is presented video segments in the same style as **Modified Training**, but the command line will optionally take user input on whether or not they correctly determined the word spoken in the current video segment.

A score is tabulated at the end.

This mode enables some extra pressure, a sort of warm-up for testing.

### Testing `(--test)`

User is presented each selected video segment as many times as specified in `--numreps NUMREPS` (default is 1), without captions. After each segment a dialog box will ask the user to type in their best guess as to what word was just spoken.

Results are calculated at the end of testing.

We would like there to be additional modes for testing to reduce the scope/difficulty/number of potential answers, specifically a multiple choice mode and a confusable pair mode, to be more isolating/conducive to an experimental environment to test efficacy of alternative modalities for deaf and hard of hearing.

### CLI options

`--range RANGE RANGE, -r RANGE RANGE`
                        start and end integer range of video segments to select.
                   
`--train, -tr `         enables training mode.

`--trainm, -trm `       enables modified training mode.

`--test, -t `           enables testing mode.

`--numreps NUMREPS, -nr NUMREPS`
                        number of times a video segments is repeated during training.
                        
`--shuffle, -s`         shuffle selected segments randomly.

`--vname VNAME, -v VNAME`
                        name of video file to pull segments from.
                        
`--fname FNAME, -f FNAME`
                        name of results file.
                        
`--idxs IDXS [IDXS ...], -i IDXS [IDXS ...]`
                        indices of specific video segments to select. If used, overrides range argument.
                        
`--wcor, -wc `          modified training mode will now include some testing features (warm up).

**still needs implementing:**

`--vidxs VIDXS, -vi VIDXS`
                        indices of specific video segments to select across all video files specified. (Key-generator).



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
