import argparse
import os
from random import randrange
import subprocess, sys

parser = argparse.ArgumentParser(description='Process range.')
parser.add_argument('--range', '-r', type=int, nargs=2,
                    help='start and end integer range of videos to select. In form start end')

args = parser.parse_args()

num_segs = len([name for name in os.listdir('./segments/') if os.path.isfile(os.path.join('./segments/', name))])

opener ="open" if sys.platform == "darwin" else "xdg-open"

for root,dirs,video_segments in os.walk('./segments/'):
        while input("press enter in command line to cycle videos, any other key to exit:") == '':
             for i in range(args.range[0], args.range[1]):
                 subprocess.call([opener, 'segments/jolly_phonics-{}.mp4'.format(i)])
