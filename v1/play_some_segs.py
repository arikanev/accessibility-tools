import argparse
import os
from random import shuffle
import subprocess, sys

parser = argparse.ArgumentParser(description='Process range.')
parser.add_argument('--range', '-r', type=int, nargs=2,
                    help='start and end integer range of videos to select. In form start end')

args = parser.parse_args()

# num_segs = len([name for name in os.listdir('./segments/') if os.path.isfile(os.path.join('./segments/', name))])

opener ="open" if sys.platform == "darwin" else "xdg-open"

closer ="close" if sys.platform == "darwin" else "xdg-close"

'''
rand_list = []
for i in range(5):
    rand_list.append(randrange(num_segs))
'''

rand_list = []
for i in range(args.range[0], args.range[1]):
    rand_list.append(i)
shuffle(rand_list)

for root,dirs,video_segments in os.walk('./segments/'):
    while input("press enter in command line to shuffle videos, any other key to exit:") == '':
        shuffle(rand_list)
        for i in rand_list:
            subprocess.call([opener, 'segments/jolly_phonics-{}.mp4'.format(i)])
      
