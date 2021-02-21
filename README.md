# accessibility-tools

## dependencies 

`brew install ffmpeg`


# v1 (from youtube video source)

## run 

`bash main.sh`


# v2 (from local video source, (and arguably better interface for playback))

## run

`bash main.sh`

`python3 play_some_segs.py -r startrangeint endrangeint`

## run (speech recognition version)

`bash main.sh`

`python3 play_some_segs_sr.py -r startrangeint endrangeint`

# Future Steps!

- Lets get youtube sourcing from first version (pytube lib), interfacing with the code in the second version, for increased funcitionality of second version. 
- Can simply add youtube link to CLI args embedded in bash script, and add arg for youtube link in v2/split_vid.py. The code for downloading youtube vid is in v1/rand_seg.py
- Speech recognition for writing SRT files.
