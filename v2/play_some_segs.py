import argparse
import os
from random import shuffle
import subprocess, sys
import tkinter as tk
from tkinter import simpledialog

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


'''
rand_list = []
for i in range(args.range[0], args.range[1]):
    rand_list.append(i)
shuffle(rand_list)
'''

idxs = []
for i in range(args.range[0], args.range[1]):
    idxs.append(i)

ROOT = tk.Tk()

ROOT.withdraw()

padding = 50 * " "

segs = []
preds = []
for root,dirs,video_segments in os.walk('./segments/'):
    for i in idxs:
            # subprocess.call([opener, 'segments/IMG_4654-{}-subs.mp4'.format(i)])
        segs.append('segments/IMG_4654-{}-subs.mp4'.format(i))
    # subprocess.call(["mpv", '--fs', '--loop-file=inf'] + segs)    

    for i in idxs:
        subprocess.call(["mpv", '--fs', '--sid=no'] + ['segments/IMG_4654-{}-subs.mp4'.format(i)])
        inp = simpledialog.askstring(title="Enter word guess for segment {}: \n".format(i), prompt="What did Sara just say?" + padding)
        with open('segments/IMG_4654-seg-{}.srt'.format(i)) as f:
            contents = f.read()
            print(contents)
            if inp and not inp.isspace() and (inp in contents or inp.lower() in contents or inp.capitalize() in contents):
                preds.append(1)
            else:
                preds.append(0)
print(preds)
# calculate and print WER
print("WER (% of correctly guessed words): {}".format(len([i for i in preds if i == 1]) / len(preds)))
