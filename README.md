# accessibility-tools

# Overview
Accessibility-tools is aimed at assisting deaf and hard-of-hearing individuals in learning to read lips, in an isolated setting or in conjunction with other assistive modalities (haptic device, cochlear implant, hearing aid).

# Help with videos
[record a video](https://github.com/arikanev/accessibility-tools/blob/main/README.md#Recording-videos), and send it to arikanevsky@gmail.com

[Current video archive](https://drive.google.com/drive/folders/1ALMMmjeSFkHpLxhxc-r0llzCmVpYWe4O?usp=sharing)

# CLI Install / Setup

`git clone https://github.com/arikanev/accessibility-tools.git`

## mac OSX

`brew install ffmpeg portaudio`

`pip3 install pyaudio`

## linux

`sudo apt-get install python-pyaudio python3-pyaudio`

`sudo apt install ffmpeg`

## general requirements (OSX, linux, etc.)

`pip3 install SpeechRecognition gdown pyspellchecker`

# v2 quick start

`cd accessibility-tools/`

## Download hosted videos, create tables, create segments.

`bash main.sh`

## Recording videos

`bash record.sh`

User is presented a prompt to speak, and is recorded speaking words of their choosing (preferably from a confusable minimal pairs word list). 

User should wait a few seconds until the camera is activated for recording (green light for my mac OSX), then follow the prompt in the terminal.

When the prompt is finished press `q` in terminal, the video capture stops.

Segmentation and captioning is then done automatically, and playback is through the `play_some_segs.py` CLI tool, usage detailed below. 

The below GIF shows the recording process, and the second playback method from [example 3](https://github.com/arikanev/accessibility-tools/blob/main/README.md#example-3)

<p align="center"> <img src="https://github.com/arikanev/accessibility-tools/blob/main/v2/assets/recording.gif"></p>

## Run a basic session.

### Example 1

`python3 play_some_segs.py -i 1 26 13 -tr -t -v 1`

`-i` specifies:

segment indices 1, 26, 13

`-tr` specifies:

[training](https://github.com/arikanev/accessibility-tools/blob/main/README.md#training---train)

`-t` specifies:

[testing](https://github.com/arikanev/accessibility-tools/blob/main/README.md#testing---test)

`-v` specifies:

[video 1](https://drive.google.com/file/d/1kBnA2wt9AmZlSUp223pF2SQ7MApoWIkp/view?usp=sharing)

### Example 2

`python3 play_some_segs.py -tr -t -vi v1s2s4s35s42v4s1s3s38s29v7s0`

`-vi` specifies:

[video 1](https://drive.google.com/file/d/1kBnA2wt9AmZlSUp223pF2SQ7MApoWIkp/view?usp=sharing), segments 2, 4, 35, 42

[video 4](https://drive.google.com/file/d/15wn7d8MwHINE9APhVQLCm31oJgHvYLoJ/view?usp=sharing), segments 1, 3, 38, 29

[video 7](https://drive.google.com/file/d/1eKW5sNKEqRtUcBvyrMK1YF8b9PtNBqT8/view?usp=sharing), segment 0

### Example 3

The following command will run training through all video segments of all available videos:

`python3 play_some_segs.py -tr`

The following command will run training through all video segments of specified video (in this case, 3):

`python3 play_some_segs.py -v 3 -tr`

# Documentation

## Training `(--train)`

`(-tr)`

User is presented each selected video segment, with no "quiz" between videos to determine users ability and understanding what the speaker has just said.

This mode is purely for the user to get familiar with the corpus.

![alt text](https://github.com/arikanev/accessibility-tools/blob/main/v2/assets/tr.gif)

## Modified training `(--train --trainm)`

`(-tr -trm)`

User is presented each selected video segment twice in succession (First, without captions, second with captions), with no "quiz" between videos to determine users ability and understanding what the speaker has just said.

This mode is purely for the user to gauge their own skill/ability.

![alt text](https://github.com/arikanev/accessibility-tools/blob/main/v2/assets/trtrm.gif)

## Modified training with correct `(--train --trainm --wcor)`

`(-tr -trm -wc)`

User is presented video segments in the same style as **Modified Training**, but the command line will **optionally** take user input on whether or not they correctly determined the word spoken in the current video segment.

A score is tabulated at the end.

This mode enables some extra pressure, a sort of warm-up for testing.

![alt text](https://github.com/arikanev/accessibility-tools/blob/main/v2/assets/trtrmwc.gif)

## Testing `(--test)`

`(-t)`

User is presented each selected video segment as many times as specified in `--numreps NUMREPS` (default is 1), without captions. After each segment a dialog box will ask the user to type in their best guess as to what word was just spoken.

Results are calculated at the end of testing.

We would like there to be additional modes for testing to reduce the scope/difficulty/number of potential answers, specifically a multiple choice mode and a confusable pair mode, to be more isolating/conducive to an experimental environment to test efficacy of alternative modalities for deaf and hard of hearing.

![alt text](https://github.com/arikanev/accessibility-tools/blob/main/v2/assets/t.gif)


## CLI options

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

`--vidxs VIDXS, -vi VIDXS`
                        indices of specific video segments to select across all video files specified. If used, overrides idxs argument. (Key-generator).


Huge credits for a lot of the core brain of this project goes to [`ffmpeg`](https://github.com/FFmpeg/FFmpeg), [`mpv`](https://github.com/mpv-player/mpv), and google cloud speech api.
