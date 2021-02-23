# accessibility-tools

## dependencies 

mac OSX

`brew install ffmpeg`
`brew install portaudio`
`pip3 install pyaudio`

linux

`sudo apt-get install python-pyaudio python3-pyaudio`
`sudo apt install ffmpeg`

general downloads

`pip3 install SpeechRecognition`
`pip3 install gdown`

# v1 (from youtube video source)

## run 

`bash main.sh`


# v2 (from local video source, (and arguably better interface for playback))

## run

`bash main.sh`

`bash lipread_test.sh startrangeint endrangeint`

## run (speech recognition version)

`bash main.sh`

`python3 play_some_segs_sr.py -r startrangeint endrangeint`

# Future Steps!

- Lets get youtube sourcing from first version (pytube lib), interfacing with the code in the second version, for increased funcitionality of second version. 
- Can simply add youtube link to CLI args embedded in bash script, and add arg for youtube link in v2/split_vid.py. The code for downloading youtube vid is in v1/rand_seg.py
- Speech recognition for writing SRT files.https://medium.com/searce/generate-srt-file-subtitles-using-google-clouds-speech-to-text-api-402b2f1da3bd
- Find someone to pay for LFS storage, or just get test video to use from: https://drive.google.com/file/d/1_YWTi4gTOS6e5AKuGXWopAMUPDFU3IRl/view?usp=sharing
- Display speech recognition interface (basically make it easier to capture user speech at correct moments) in dialog/popup boxes
  - dig into SpeechRecognition api, eventually use some sort of more customizable alternative, parratron, live transcribe, something for HOH speech to be understood
- MPV player should remain open as popup for user input appears after each vid. Try increasing CPU threads to 2 and/or running parallel process.
- Haptic isolation training tool - decrease brightness over time of videos.
- editing user inputs in case of typos


- add TooLoud interface of some sort. We want it on phones or haptics.
